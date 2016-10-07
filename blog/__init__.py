# encoding=utf-8
from datetime import timedelta
from flask import Flask, session
from flask import render_template

from blog import settings
from blog.utils import url_for_other_page

# 创建Flask，第一个参数是应用模块或者包的名称，单一模块使用‘__name__’

app = Flask('blog')

# from_object() 方法，并传递一个模块的导入名作为参数。Flask 会从这个模块初始化变量。 注意，只有名称全为大写字母的变量才会被采用。
app.config.from_object('blog.config')


@app.before_request
def make_session_permanent():
    session.permanent = True
# 开启session的生命周期管理模式
app.permanent_session_lifetime = timedelta(minutes=20)

# Settings对象要放在开始创建，因为它初始化添加了很多属性，如PAGE_SIZE
settingsClass = settings.Settings(app.config)


# 设置一个在页面中能够使用的方法 获取分页的链接
app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['meta_description'] = app.config['BLOG_DESCRIPTION']

@app.errorhandler(404)  # 错误处理器 关联abort函数，当错误发生时，错误被当做参数传进来
def page_not_found(e):
    return render_template('404.html'), 404

import blog.post_view
import blog.user_view

