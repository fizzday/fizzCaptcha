import random
import hashlib
import requests
from PIL import Image
from bs4 import BeautifulSoup
from fizzCaptcha import recognize

def md5(pwd):
    m = hashlib.md5()
    # 参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
    m.update(pwd.encode(encoding='utf-8'))
    return m.hexdigest()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
}
# 验证码
url_captcha_get = "http://www.hust-snde.com/center/sso/authimg?" + str(random.random())
# 登录页
url_index_get = "http://www.hust-snde.com/cms/"
# 执行登录
url_login_post = "http://www.hust-snde.com/center/center/login_login.action"
# login_centerLogin
url_login_centerLogin_get = "http://www.hust-snde.com/sso/login_centerLogin.action"
url_login_centerLogin_get_header = {"Upgrade-Insecure-Requests": "1"}
# loginSuccess
url_loginSuccess_get = "http://www.hust-snde.com/web/loginSuccess.jsp"
# whatyVerify 302
url_whatyVerify_post = "http://cas.hust-snde.com/whatyVerify"


# home
# url_home_get = "http://sns.hust-snde.com/learning/entity/student/student_index.action"

def login(username, password):
    # 设置用户名和密码
    login_params = {
        # "loginId": "W201714333123456",
        # "passwd": md5("42032119901203"),
        "loginId": username,
        "passwd": md5(password),
        "auto": "false",
        "info": "0",
        "authCode": ""
    }
    # 认证跳转参数
    whatyVerify_params = {
        "username": login_params["loginId"],
        "password": login_params["passwd"],
        "service": "http://sns.hust-snde.com/learning/sso/login_webTrnLogin.action?ssoUser.loginId=" +
                   login_params["loginId"] + "&siteCode=code62"
    }

    session = requests.Session()

    # 打开登录页
    session.get(url_index_get, headers=headers)
    # 刷新验证码
    im = Image.open(session.get(url_captcha_get, stream=True).raw)
    # 识别验证码
    code = recognize.recognize(im)
    # im.save("./images/" + code + ".jpg")
    login_params["authCode"] = code
    # print(code)
    # 执行登录
    session.post(url_login_post, data=login_params, headers=headers)

    # 各种中转访问
    headers302 = dict(headers, **url_login_centerLogin_get_header)

    session.get(url_login_centerLogin_get, headers=headers302)
    session.get(url_loginSuccess_get, headers=headers302)
    # 各种 302
    html1 = session.post(url_whatyVerify_post, data=whatyVerify_params, headers=headers302, allow_redirects=False)
    # login_webTrnLogin 302 得到
    html2 = session.get(html1.headers['Location'], headers=headers302, allow_redirects=False)
    # error_login 302 得到
    html3 = session.get(html2.headers['Location'], headers=headers302, allow_redirects=False)
    # login_webTrnLogin 302 得到
    html4 = session.get(html3.headers['Location'], headers=headers302, allow_redirects=False)
    # login_webTrnLogin 302 得到
    html5 = session.get(html4.headers['Location'], headers=headers302, allow_redirects=False)
    # student_index 302 得到
    r = session.get(html5.headers['Location'], headers=headers302)

    # 查看登录次数
    soup = BeautifulSoup(r.text, "html5lib")
    res = soup.select("#announcement")[0].get_text()

    return res


if __name__ == "__main__":
    username = "W201714333"
    password = "420321199012032411"

    res = login(username, password)

    print(res)
