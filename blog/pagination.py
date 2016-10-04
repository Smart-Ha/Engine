# encoding=utf-8
from math import ceil


class Pagination(object):
    '''
    分页
    '''
    def __init__(self, page, page_size, total_count):
        self.page = page
        self.page_size = page_size
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count/self.page_size))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2):
        pass
