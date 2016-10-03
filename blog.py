# encoding=utf-8
import os
import sqlite3
import settings
import post
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask('EngineBlog')
# from_object() 方法，并传递一个模块的导入名作为参数。Flask 会从这个模块初始化变量。 注意，只有名称全为大写字母的变量才会被采用。
app.config.from_object('config')

'''
Settings对象要放在最开始创建，因为它初始化添加了很多属性，如PAGE_SIZE
'''
settingsClass = settings.Settings(app.config)
postClass = post.Post(app.config)
# userClass = user.User(app.config)


@app.template_filter('formatdate')
def format_datetime_filter(input_value, format_="%a, %d %b %Y"):
    return input_value.strftime(format_)


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    skip = int(app.config['PAGE_SIZE']) * (page - 1)
    posts = postClass.get_posts(int(app.config['PAGE_SIZE']), skip)
    return render_template('index.html', posts=posts['data'])


@app.route('/tag/<tag>', defaults={'page': 1})
@app.route('/tag/<tag>/<int:page>')
def posts_by_tag(tag, page):
    pass


@app.route('/post/<id>')
def show_post(id):
    pass


@app.route('/s/<query>', defaults={'page': 1})
@app.route('/s/<query>/<int:page>')
def search(query,page):
    pass

if __name__ == '__main__':
    app.run()
