# encoding=utf-8
from blog import app
'''
启动app
Flask 程序对象的创建必须在 __init__.py 文件里完成，
这样我们就可以安全的导入每个模块，而 __name__ 变量将会被分配给正确的包。
所有（上面有 route() 装饰器的那些）视图函数必须导入到 __init__.py 文件。
请通过模块而不是对象本身作为路径导入这些视图函数。必须在应用对象创建之后 导入视图模块
'''
app.run()
