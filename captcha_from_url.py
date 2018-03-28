import requests
# 从网上扒取图片
from PIL import Image

def captcha_from_url(urr="", save_path=""):
    # 下载图片
    r = requests.get(url, stream=True)

    im = Image.open(r.raw)

    # 保存图片
    if save_path:
        im.save(save_path)

    # 返回 流
    return im


if __name__=="__main__":
    save_path = "./images/down.jpg"
    url = "https://www.yongedai.com/plugins/index.php?q=imgcode"

    im = captcha_from_url(url, save_path=save_path)

    im.show()