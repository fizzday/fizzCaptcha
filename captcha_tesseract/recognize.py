# 验证码识别主程序
from pytesseract import pytesseract
from fizzCaptcha import config,image_operation,captcha_from_path
from PIL import Image

# tesseract 识别
def recognize(image="", lang="chi_sim"):
    '''
    使用tesseract识别
    :param image: PIL流
    :param clear: 二值化并去噪点(默认True执行, False不执行)
    :param threshold: 二值化临界值(默认140,可以根据图片字符的rgb颜色来测试设定)
    :return: 
    '''
    res = ""
    if config.mode == "tesseract":
        res = pytesseract.image_to_string(image, lang=lang)

    elif config.mode == "tensorflow":
        pass

    return res.replace(" ","")

if __name__=="__main__":
    # img_path = "../example/test2.png"
    # img_path = "/Users/fizz/Desktop/11.jpg"
    # img_path = "/Users/fizz/Desktop/22.png"
    # img_path = "/Users/fizz/Downloads/测试/13771302714&2.jpg"
    image_path = "./images/"
    img_list = captcha_from_path.gen_list(image_path)

    with open("./result.txt", "a+") as f:
        for item in img_list:
            im = Image.open(image_path+item)

            # 二值化并去噪点
            im = image_operation.get_clear_bin_image(im)
            # 识别汉字
            res1 = recognize(im)
            text_ch = res1[:3]
            # 识别数字
            res2 = recognize(im, lang="eng")
            text_alarm = res2.split(":")[1]
            print(text_ch,text_alarm)
            #
            # im.show()

            f.write(text_ch+":"+text_alarm+"\n")

        f.close()