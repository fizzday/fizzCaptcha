# 从文件夹中读取验证码
import os

def gen_list(root_dir):
    img_list = []
    for parent, dirnames, filenames in os.walk(root_dir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            img_list.append(filename.replace(".jpeg",""))
            # print("parent is:" + parent)
            # print("filename is:" + filename)
            # print("the full name of the file is:" + os.path.join(parent, filename))  # 输出文件路径信息
    return img_list