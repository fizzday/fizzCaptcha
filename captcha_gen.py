# coding:utf-8
import random
import numpy as np
from PIL import Image
from captcha.image import ImageCaptcha

import os

NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LOW_CASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
UP_CASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']
CAPTCHA_LIST = NUMBER + LOW_CASE + UP_CASE
CAPTCHA_LEN = 4
CAPTCHA_HEIGHT = 60
CAPTCHA_WIDTH = 160


def random_captcha_text(char_set=CAPTCHA_LIST, captcha_size=CAPTCHA_LEN):
    '''
    随机生成验证码文本
    :param char_set:
    :param captcha_size:
    :return:
    '''
    captcha_text = [random.choice(char_set) for _ in range(captcha_size)]
    return ''.join(captcha_text)


def gen_captcha_text_and_image(width=CAPTCHA_WIDTH, height=CAPTCHA_HEIGHT,save=None):
    '''
    生成随机验证码
    :param width:
    :param height:
    :param save:
    :return: np数组
    '''
    image = ImageCaptcha(width=width, height=height)
    # 验证码文本
    captcha_text = random_captcha_text()
    captcha = image.generate(captcha_text)
    # 保存
    if save: image.write(captcha_text, './images2/'+captcha_text + '.jpg')
    captcha_image = Image.open(captcha)
    # 转化为np数组
    captcha_image = np.array(captcha_image)
    return captcha_text, captcha_image

def gen_list(root_dir):
    img_list = []
    for parent, dirnames, filenames in os.walk(root_dir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            img_list.append(filename.replace(".jpeg",""))
            # print("parent is:" + parent)
            # print("filename is:" + filename)
            # print("the full name of the file is:" + os.path.join(parent, filename))  # 输出文件路径信息
    return img_list

# 生成字符对应的验证码
def gen_captcha_text_and_image2(imageNo=1):
    root_dir = "./images/"
    captcha = gen_list(root_dir)

    captcha_text = captcha[imageNo%100]
    captcha_file = root_dir+captcha_text+".jpeg"

    captcha_image = Image.open(captcha_file)
    captcha_image = np.array(captcha_image)
    # print(captcha_text, captcha_image)
    return captcha_text, captcha_image

def gen_captcha_text_and_image3():
    img_list = []
    for parent, dirnames, filenames in os.walk(root_dir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            img_list.append(filename.replace(".jpeg", ""))
            # print("parent is:" + parent)
            # print("filename is:" + filename)
            # print("the full name of the file is:" + os.path.join(parent, filename))  # 输出文件路径信息
    return img_list

if __name__ == '__main__':
    t, im = gen_captcha_text_and_image()
    print(t, im)


