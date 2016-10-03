# encoding = utf-8
import pymongo

CONNECTION_STRING = 'mongodb://localhost'
CONNECTION = pymongo.MongoClient(CONNECTION_STRING)

'''
database and tables
'''
DATABASE = CONNECTION.db_engine_blog
POST_COLLECTION = DATABASE.post
TAG_COLLECTION = DATABASE.tag
USER_COLLECTION = DATABASE.user
SETTINGS_COLLECTION = DATABASE.settings

SECRET_KEY = 'WANGYONG'

LOG_FILE = 'app.log'

DEBUG = True


