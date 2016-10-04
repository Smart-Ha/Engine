# encoding=utf-8
import datetime
import pymongo
from bson.objectid import ObjectId

# 创建连接
conn = pymongo.MongoClient("mongodb://localhost")
# 连接数据库
db = conn.db_engine_blog
# 打印所有聚集名称，连接聚集
print u'所有聚集:', db.collection_names()

post = db.post
# print post.find_one({'likes': {'$gt': 90}})

'''
# 删除集合
# post.drop()
post.insert([{
    'title': '我是第2个标题',
    'preview': '哈哈哈',
    'body': '哈哈，这是我的第2篇文。',
    'date': datetime.datetime.utcnow(),
    'author': 'my',
    'tags': ['java', 'php'],
    'comments': []
}, {'title': '我是第3个标题',
    'preview': '哈哈哈',
    'body': '哈哈，这是我的第3篇文。',
    'date': datetime.datetime.utcnow(),
    'author': 'my',
    'tags': ['java', 'php5'],
    'comments': []
   }])
'''
for p in post.find():
    print p['_id'], p['title']
for p in post.find({'_id': ObjectId('57f268e82551733966a27987')}):
    print p['_id'], p['title']

