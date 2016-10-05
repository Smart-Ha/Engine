# encoding=utf-8
import datetime
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


class User:
    """
    用户，_id 为用户名 不可重复
    """
    def __init__(self, default_config):
        self.collection = default_config['USER_COLLECTION']
        self.username = None
        self.email = None
        self.password = None
        self.avatar = 'https://pic4.zhimg.com/f3365e7cf35be39fe008552059b7dcc3_m.jpg'
        self.session_key = 'user'

        self.response = {'error': None, 'data': None}
        self.debug_mode = default_config['DEBUG']

    def login(self, username, password):
        self.response['error'] = None
        try:
            user = self.collection.find_one({'_id': username})
            if user:
                if self.check_password(user['password'], password):
                    self.username = user['_id']
                    self.email = user['email']
                    if 'avatar' in user:
                        self.avatar = user['avatar']
                else:
                    self.response['error'] = 'password not match!'
            else:
                self.response['error'] = 'user not existed!'
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'system error...'

        self.response['data'] = {'username': self.username, 'email': self.email, 'avatar': self.avatar}
        return self.response

    def create_session(self, obj):
        session[self.session_key] = obj
        return True

    def add_user(self, user_data):
        self.response['error'] = None
        password_hash = generate_password_hash(user_data['password'], method='pbkdf2:sha256')
        user = {
            '_id': user_data['_id'],
            'email': user_data['email'],
            'password': password_hash,
            'date': datetime.datetime.utcnow()
        }
        try:
            self.collection.insert(user)
            self.response['data'] = True
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Create user error..'
        return self.response

    def is_id_used(self, user_id):
        count = self.collection.find_one({'_id': user_id}).count()
        return count > 0

    def is_email_used(self, email):
        count = self.collection.find_one({'email': email}).count()
        return count > 0

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def print_debug_info(msg, show=False):
        if show:
            import sys
            import os

            error_color = '\033[32m'
            error_end = '\033[0m'

            error = {'type': sys.exc_info()[0].__name__,
                     'file': os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
                     'line': sys.exc_info()[2].tb_lineno,
                     'details': str(msg)}

            print error_color
            print '\n\n---\nError type: %s in file: %s on line: %s\nError details: %s\n---\n\n' \
                  % (error['type'], error['file'], error['line'], error['details'])
            print error_end
