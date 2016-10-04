# encoding=utf-8
from flask import Flask
from blog import settings

# 创建Flask，第一个参数是应用模块或者包的名称，单一模块使用‘__name__’
app = Flask('blog')

# from_object() 方法，并传递一个模块的导入名作为参数。Flask 会从这个模块初始化变量。 注意，只有名称全为大写字母的变量才会被采用。
app.config.from_object('blog.config')

# Settings对象要放在开始创建，因为它初始化添加了很多属性，如PAGE_SIZE
settingsClass = settings.Settings(app.config)

import blog.post_view

