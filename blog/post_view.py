# encoding=utf-8
import cgi


import datetime
from flask import abort, render_template, request, session
from flask import flash
from flask import redirect
from flask import url_for

from blog import post
from blog import pager
from blog import app
from blog.utils import extract_tags, login_required

postClass = post.Post(app.config)


@app.template_filter('formatdate')
def format_datetime_filter(input_value, format_="%a, %d %b %Y"):
    return input_value.strftime(format_)


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    skip = int(app.config['PAGE_SIZE']) * (page - 1)
    posts = postClass.get_posts(int(app.config['PAGE_SIZE']), skip)
    count = postClass.get_total_count()
    print('count' + str(count))
    pag = pager.Pagination(page, int(app.config['PAGE_SIZE']), count)
    print('  pages:' + str(pag.pages) + '_'+ str(app.config['PAGE_SIZE']))
    return render_template('index.html', posts=posts['data'], pager=pag)


@app.route('/tag/<tag>', defaults={'page': 1})
@app.route('/tag/<tag>/page-<int:page>')
def posts_by_tag(tag, page):
    skip = int(app.config['PAGE_SIZE']) * (page - 1)
    posts = postClass.get_posts(int(app.config['PAGE_SIZE']), skip, tag=tag)
    count = postClass.get_total_count(tag=tag)
    pag = pager.Pagination(page, int(app.config['PAGE_SIZE']), count)
    if not posts['data']:
        abort(404)
    return render_template('index.html', posts=posts['data'], pager=pag)


@app.route('/post/<id>')
def show_post(id):
    post = postClass.get_post_by_id(id)
    if not post['data']:
        flash(post['error'], 'error')
        print('im here')
        abort(404)
    return render_template('one_post.html', post=post['data'])


@app.route('/new_post', methods=['POST', 'GET'])
@login_required()
def new_post():
    error = False
    error_msg = 'form is not fill out completely!'
    if request.method == 'POST':
        title = request.form.get('title', None)
        preview = request.form.get('short-text', None)
        body = request.form.get('full-text', None)

        if not title or not preview or not body:
            error = True
        else:
            tags = cgi.escape(request.form.get('tags'))
            tag_array = extract_tags(tags)

            post_data = {
                'title': title,
                'preview': preview,
                'body': body,
                'author': session['user'],
                'date': datetime.datetime.utcnow(),
                'tags': tag_array
            }
            post_id = request.form.get('post-id')
            if post_id:     # 修改
                post = postClass.update_post(post_data, post_id)
                post['data'] = post_id
            else:   # 添加
                post = postClass.add_new_post(post_data)
            if post['error']:
                error = True
                error_msg = post['error']
            else:
                print(post['data'])
                return redirect(url_for('show_post', id=post['data']))

    return render_template('new_post.html', error=error, error_msg=error_msg)


@app.route('/edit_post', methods=['GET'])
@login_required()
def edit_post():
    post_id = request.args.get('post_id')
    if not post_id:
        abort(404)
    post = postClass.get_post_by_id(post_id)
    if post['error']:
        error = True
        error_msg = post['error']
        render_template('error.html', error=error, error_msg=error_msg)
    return render_template('edit_post.html', post=post['data'])


@app.route('/s/<query>', defaults={'page': 1})
@app.route('/s/<query>/page-<int:page>')
def search_by_post(page, query):
    if not query:
        redirect(url_for('index'))

    skip = int(app.config['PAGE_SIZE']) * (page - 1)
    posts = postClass.get_posts(int(app.config['PAGE_SIZE']), skip, search=query)
    count = postClass.get_total_count(search=query)
    pag = pager.Pagination(page, app.config['PAGE_SIZE'], count)

    return render_template('search_result.html', posts=posts['data'], query=query,
                           pager=pag, meta_title='Search results'+query)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method != 'POST':
        return redirect(url_for("index"))
    query = request.form.get('q', None)
    if query:
        return redirect(url_for('search_by_post', query=query))
    else:
        return redirect(url_for('index'))


@app.before_request
def set_globals():
    app.jinja_env.globals['hot_tags'] = postClass.get_tags()['data']
    app.jinja_env.globals['recent_posts'] = postClass.get_posts(10, 0)['data']
