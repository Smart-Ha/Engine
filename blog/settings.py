# encoding=utf-8


class Settings:
    '''
    project configuration
    '''
    def __init__(self, default_config):
        self.collection = default_config['SETTINGS_COLLECTION']
        self.config = default_config    # 传递的是引用，指向同一个对象（地址）
        self.config['PAGE_SIZE'] = 10
        self.config['SEARCH'] = False
        self.config['BLOG_TITLE'] = 'ENGINE BLOG'
        self.config['BLOG_DESCRIPTION'] = 'WITH YOU'

        self.response = {'error': None, 'data': None}
        self.debug_mode = default_config['DEBUG']

    def get_config(self):
        try:
            cursor = self.collection.find_one()
            if cursor:
                self.config['PAGE_SIZE'] = cursor.get('page_size', self.config['PAGE_SIZE'])

        except Exception, e:
            self.print_debug_info(e, self.debug_mode)

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
