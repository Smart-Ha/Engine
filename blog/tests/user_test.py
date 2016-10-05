# encoding=utf-8
import blog
from blog import user

userClass = user.User(blog.app.config)

user = {
    '_id': 'ha',
    'email': '123@qq.com',
    'password': '123123'
}

resp = userClass.add_user(user)
if resp['data']:
    print('success')
