# encoding=utf-8
import re
from flask import render_template, redirect, url_for, session, request, flash
from blog import user
from blog import app

userClass = user.User(app.config)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    error_msg = "form not fill out completely!"
    if request.method == 'GET':
        print('i am in get.')
        if session.get('user'):
            return redirect(url_for('index'))
    else:
        print ('i am in post')
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            error = True
        else:
            user_info = userClass.login(username.lower(), password)
            if user_info['error']:
                error = True
                error_msg = user_info['error']
            else:
                userClass.create_session(user_info['data'])
                flash("you are logged in!", 'success')
                return redirect(url_for('index'))
    print('im going')
    return render_template('login.html', error=error, error_msg=error_msg)


@app.route('/logout')
def logout():
    if userClass.logout():
        flash('You are logged out!', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    error = False
    if request.method == 'POST':
            post_data = {
                '_id': request.form.get('username', None),
                'email': request.form.get('email', None),
                'password': request.form.get('password', None),
                'confirmpass': request.form.get('confirmpass', None)
            }
            error_msg = validate_form(post_data)
            if len(error_msg) < 1:
                user = userClass.add_user(post_data)
                if user['error']:
                    error_msg['syserror'] = user['error']
                    error = True
                else:
                    flash('register succeed!', 'success')
                    return redirect(url_for('login'))
            error = True
            return render_template('regist.html', error=error, error_msg=error_msg)
    else:
        return render_template('regist.html')


def validate_form(post_data):   # 校验表单
    error_msg = {}

    if post_data['_id'] is None:
        error_msg['username'] = 'username not fill out!'
    elif userClass.is_id_used(post_data['_id']):
        error_msg['username'] = 'this username is used!'

    if post_data['email'] is None:
        error_msg['email'] = 'email not fill out!'
    elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", post_data['email']):
        error_msg['email'] = 'invalid email!'
    elif userClass.is_email_userd(post_data['email']):
        error_msg['error'] = 'this email is used!'

    if post_data['password'] is None:
        error_msg['password'] = 'password not fill out!'

    if post_data['confirmpass'] is None:
        error_msg['confirmpass'] = 'confirmpass not fill out!'
    elif post_data['password'] != post_data['confirmpass']:
        error_msg['confirmpass'] = 'not matched to password!'

    return error_msg