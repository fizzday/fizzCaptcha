#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 2018/3/26 10:14
# @Author  : fizzday<fizzday@yeah.net>
# @File    : hust_login.py
#
# 刷华中科技大学教务系统登录次数
import base64
import json
import sys, os, io

import requests

from fizzCaptcha import recognize

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from fizzCaptcha.example import hust

from flask import Flask, request, send_file
import flask_cors
from PIL import Image

app = Flask(__name__)

flask_cors.CORS(app, supports_credentials=True)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    return "hello world!"

# 验证码识别
@app.route('/recognize_tesseract', methods=["GET", "POST"])
def recognizeTesseract():
    if request.method == "GET":
        url = request.args.get("url")
        # return url
        file = requests.get(url, stream=True).raw
    else:
        file = request.files['file']
        # file.save("/Users/fizz/www/python/fizzCaptcha/example/"+file.filename)

    # 识别验证码
    im = Image.open(file)
    code = recognize.recognize(im)

    return code




# 验证码生成
@app.route('/getCaptcha', methods=["GET", "POST"])
def getCaptcha():
    # return "sf"
    from fizzCaptcha.captcha_generate.FizzCaptcha import FizzCaptcha

    config_json = request.form.get("config")

    fc = FizzCaptcha()

    if config_json:
        config = json.loads(config_json)
        # 处理字体
        # config["font"]["path"] = "../captcha_generate/"+config["font"]["name"]+".ttf"
        # 处理是否噪点等
        config["point"] = eval(config["point"])
        config["line"] = eval(config["line"])
        config["tilt"] = eval(config["tilt"])

        # print(config)
        # return json.dumps(config)
        fc.setConfig(config)

    image, text = fc.getCaptcha()

    byte_io = io.BytesIO()
    image.save(byte_io, 'PNG')
    # base64
    return u"data:image/png;base64," + base64.b64encode(byte_io.getvalue()).decode('ascii')
    # flask 返回
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')

# 华科大模拟登录
@app.route('/login', methods=["GET", "POST"])
def login():
    # return "sdf"
    username, password, loginnum = "", "", 5

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
        return "用户名和密码不能为空..."

    # return username+password
    res = ""
    loginnumInt = int(loginnum)
    if loginnumInt > 10:
        return "请一次请求1保持在10次以内!!!"
    for i in range(loginnumInt):
        res = hust.login(username, password)
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
