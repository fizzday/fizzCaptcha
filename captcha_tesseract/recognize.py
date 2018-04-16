# 验证码识别主程序
from pytesseract import pytesseract
from fizzCaptcha import config,image_operation
from PIL import Image

# tesseract 识别
def recognize(image=""):
    '''
    使用tesseract识别
    :param image: PIL流
    :param clear: 二值化并去噪点(默认True执行, False不执行)
    :param threshold: 二值化临界值(默认140,可以根据图片字符的rgb颜色来测试设定)
    :return: 
    '''
    res = ""
    if config.mode == "tesseract":
        res = pytesseract.image_to_string(image)

    elif config.mode == "tensorflow":
        pass

    return res.replace(" ","")

if __name__=="__main__":
    img_path = "../example/test2.png"

    im = Image.open(img_path)

    # 二值化并去噪点
    im = image_operation.get_clear_bin_image(im)
    # 识别
    res = recognize(im)

    im.show()

    print(res)
