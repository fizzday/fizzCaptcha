# 识别模式
mode = "tesseract"
'''
可选的识别模式有:
tesseract: 无须训练, 直接识别, 可用于识别简单清晰的图片  
tensorflow: 训练识别, 识别之前, 需要先执行 cnn 训练, 生成训练model后, 方可使用
'''
tesseract = {
    '''
    验证码的字体语言, 默认英语(包括数字字母), 可选的有:
    eng: 英语
    ch_sim: 简体中文
    eng+ch_sim: 英语+简体中文
    '''
    "lang": "eng",
}
tensorflow = {
    "width": "160",  # 验证码宽度
    "height": "60",  # 验证码高度
    "chars": "4",  # 验证码字母个数
}

# 字典集合
dictionary = [
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "1234567890"
]
