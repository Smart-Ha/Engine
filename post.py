# encoding=utf-8


class Post:
    '''
    blog detail
    '''

    def __init__(self, default_config):
        self.collection = default_config['POST_COLLECTION']
        self.response = {'error': None, 'data': None}
        self.debug_mode = default_config['DEBUG']

    def get_posts(self, limit, skip, tag=None, search=None):
        self.response['error'] = None

        try:
            condition = {}
            # TODO tag & search

            cursor = self.collection.find().sort(
                'date', direction=-1).skip(skip).limit(limit)
            self.response['data'] = []
            for post in cursor:
                if 'preview' not in post:
                    post['preview'] = ''
                if 'tags' not in post:
                    post['tags'] = []
                if 'comments' not in post:
                    post['comments'] = []

                self.response['data'].append({
                    'id': post['_id'],
                    'title': post['title'],
                    'preview': post['preview'],
                    'body': post['body'],
                    'date': post['date'],
                    'author': post['author'],
                    'tags': post['tags'],
                    'comments': post['comments']
                })
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found...'

        return self.response

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





