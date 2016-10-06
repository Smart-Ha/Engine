import datetime

from blog import app
from blog.post import Post

postClass = Post(app.config)

post = {
    'title': '123',
    'preview': 'asdasd',
    'body': 'asda',
    'author': { "username" : "ha" , "avatar" : "http://d.hiphotos.baidu.com/baike/w%3D268%3Bg%3D0/sign=86917ad6d139b6004dce08b1d16b5217/962bd40735fae6cde8d6d2540bb30f2442a70fa0.jpg" , "email" : "123@qq.com"},
    'date': datetime.datetime.utcnow(),
    'tags': ['haha']
}

id = postClass.add_new_post(post)

print(id)
