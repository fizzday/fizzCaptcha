#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 2018/3/26 10:14
# @Author  : fizzday<fizzday@yeah.net>
# @File    : hust_login.py
#
# 刷华中科技大学教务系统登录次数
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from fizzCaptcha.example import hust

from flask import Flask,request
import flask_cors

app = Flask(__name__)

flask_cors.CORS(app, supports_credentials=True)

@app.route('/')
def hello_world():
    return "hello world!"

@app.route('/login')
def login():
    # return "sdf"
    username = request.args.get("username")
    password = request.args.get('password')

    if not username or not password:
        return "用户名或密码不能为空..."

    # return username+password
    res = hust.login(username,password)
    return res

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()

# if __name__ == "__main__":
#     # try:
#     #     res = login()
#     #     print(res)
#     # except IOError:
#     #     print("登录失败~~~")
#     # else:
#     #     print("执行完毕~~~")
#     pass
