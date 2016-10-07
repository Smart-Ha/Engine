# encoding=utf-8
import datetime
from bson import ObjectId


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
            if tag is not None:
                condition = {'tags': tag}
            elif search is not None:
                condition = {'$or': [
                    {'title': {'$regex': search, '$options': 'i'}},  # $regex 表示模糊查询，$options是$regex的参数 i表示不区分大小写
                    {'body': {'$regex': search, '$options': 'i'}},
                    {'preview': {'$regex': search, '$options': 'i'}}
                ]}

            cursor = self.collection.find(condition).sort(
                'date', direction=-1).skip(skip).limit(limit)
            self.response['data'] = []
            for post in cursor:
                if 'preview' not in post:
                    post['preview'] = ''
                if 'tags' not in post:
                    post['tags'] = []
                if 'comments' not in post:
                    post['comments'] = []
                if 'date' not in post:
                    post['date'] = datetime.datetime.utcnow()
                self.response['data'].append({
                    'id': post['_id'],
                    'title': post['title'],
                    'preview': post['preview'],
                    'body': post['body'],
                    'author': post['author'],
                    'date': post['date'],
                    'tags': post['tags'],
                    'comments': post['comments']
                })

        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found...'

        return self.response

    def get_post_by_id(self, id):
        self.response['data'] = True
        try:

            post = self.collection.find_one({'_id': ObjectId(id)})
            if not post:
                self.response['data'] = False
                self.response['error'] = 'Post not found...'
                return self.response
            if 'preview' not in post:
                post['preview'] = ''
            if 'tags' not in post:
                post['tags'] = []
            if 'comments' not in post:
                post['comments'] = []
            self.response['data'] = {
                'id': post['_id'],
                'title': post['title'],
                'preview': post['preview'],
                'body': post['body'],
                'author': post['author'],
                'date': post['date'],
                'tags': post['tags'],
                'comments': post['comments']
            }
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['data'] = False
            self.response['error'] = 'Post not found'

        return self.response

    def add_new_post(self, post):
        self.response['error'] = None
        try:
            self.collection.insert(post)
            self.response['data'] = post['_id']
        except Exception, e:
            self.response['error'] = 'system error ...'
            self.print_debug_info(e, self.debug_mode)

        return self.response

    def update_post(self, post, post_id):
        self.response['error'] = None
        try:
            self.collection.update({'_id': ObjectId(post_id)},
                                   {'$set': post}, upsert=False)
            self.response['data'] = True
        except Exception, e:
            self.response['error'] = 'system error...'
            self.print_debug_info(e, self.debug_mode)

        return self.response

    def get_tags(self):
        self.response['error'] = None
        try:
            self.response['data'] = list(self.collection.aggregate([
                {'$unwind': '$tags'},  # 将文档中的某一个数组类型字段拆分成多条，每条包含数组中的一个值
                {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},  # 将集合中的文档分组，可用于统计结果。
                {'$sort': {'count': -1}},  # 按count大小排序
                {'$limit': 10},
                {'$project': {'title': '$_id', 'count': 1, '_id': 0}}
                # project 修改输入文档的结构,用来重命名、增加或删除域,title值为_id,保留count，不保留id
            ]))
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Get tags error..'

        return self.response

    def get_total_count(self, tag=None, search=None):
        condition = {}
        if tag is not None:
            condition = {'tags': tag}
        elif search is not None:
            condition = {'$or': [
                {'title': {'$regex': search, '$options': 'i'}},  # $regex 表示模糊查询，$options是$regex的参数 i表示不区分大小写
                {'body': {'$regex': search, '$options': 'i'}},
                {'preview': {'$regex': search, '$options': 'i'}}
            ]}

        return self.collection.find(condition).count()

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
