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

@app.route('/', methods=["GET", "POST"])
def hello_world():
    return "hello world!"

@app.route('/login', methods=["GET", "POST"])
def login():
    # return "sdf"
    username, password, loginnum = "","",5

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get('password')
        loginnum = request.form.get('loginnum') if True else loginnum
    elif request.method == "GET":
        username = request.args.get("username")
        password = request.args.get('password')
        loginnum = request.args.get('loginnum') if True else loginnum
        pass

    if not username or not password:
        return "用户名或密码不能为空..."

    # return username+password
    res = ""
    for i in range(int(loginnum)):
        res = hust.login(username,password)
    return res

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True)

# if __name__ == "__main__":
#     # try:
#     #     res = login()
#     #     print(res)
#     # except IOError:
#     #     print("登录失败~~~")
#     # else:
#     #     print("执行完毕~~~")
#     pass
