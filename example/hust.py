
import random
import hashlib
import requests
from PIL import Image
from bs4 import BeautifulSoup
from fizzCaptcha import recognize


def test():
    return "333"
def md5(pwd):
    m = hashlib.md5()
    # 参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
    m.update(pwd.encode(encoding='utf-8'))
    return m.hexdigest()

login_params = {
    "loginId": "W201714333123456",
    "passwd": md5("42032119901203"),
    "auto": "false",
    "info": "0",
    "authCode": ""
}

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
# whatyVerify
url_whatyVerify_post = "http://cas.hust-snde.com/whatyVerify"
whatyVerify_params = {
    "username": login_params["loginId"],
    "password": login_params["passwd"],
    "service": "http://sns.hust-snde.com/learning/sso/login_webTrnLogin.action?ssoUser.loginId=" + login_params[
        "loginId"] + "&siteCode=code62"
}
# login_webTrnLogin
url_login_webTrnLogin_get = "http://sns.hust-snde.com/learning/sso/login_webTrnLogin.action?ssoUser.loginId=" + \
                            login_params[
                                "loginId"] + "&siteCode=code62"
# login
url_login_get = "http://cas.hust-snde.com/login?service=http://sns.hust-snde.com/learning/sso/login_webTrnLogin.action?ssoUser.loginId=" + \
                login_params[
                    "loginId"] + "&siteCode=code62&loginpage=http://sns.hust-snde.com:80/learning/html/error_login.jsp"
# home
url_home_get = "http://sns.hust-snde.com/learning/entity/student/student_index.action"

def login(username,password):
    global login_params
    # 设置用户名和密码
    login_params["loginId"] = username
    login_params["passwd"] = md5(password)

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
    session.post(url_login_post, headers=headers)

    # 各种中转访问
    session.get(url_login_centerLogin_get, headers=dict(headers, **url_login_centerLogin_get_header))
    session.get(url_loginSuccess_get, headers=dict(headers, **url_login_centerLogin_get_header))
    session.post(url_whatyVerify_post, data=whatyVerify_params,
                 headers=dict(headers, **url_login_centerLogin_get_header))
    session.get(url_login_webTrnLogin_get, headers=dict(headers, **url_login_centerLogin_get_header))
    html = session.get(url_login_get, headers=dict(headers, **url_login_centerLogin_get_header),
                       allow_redirects=False)
    url_new_get = html.headers['Location']
    html2 = session.get(url_new_get, headers=dict(headers, **url_login_centerLogin_get_header),
                        allow_redirects=False)
    url_new_get2 = html2.headers['Location']
    session.get(url_new_get2, headers=dict(headers, **url_login_centerLogin_get_header))
    session.get(url_login_webTrnLogin_get, headers=dict(headers, **url_login_centerLogin_get_header))
    r = session.get(url_home_get, headers=dict(headers, **url_login_centerLogin_get_header))

    # 查看登录次数
    soup = BeautifulSoup(r.text, "html5lib")
    res = soup.select("#announcement")[0].get_text()

    return res