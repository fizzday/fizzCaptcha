#!/usr/bin/python
# -*- coding: utf-8 -*-

config = {
        "chars": [
            "char_number",  # 数字
            "char_lower",   # 小写字母
            "char_upper",   # 大写字母
            "char_chinese"  # 一级汉字
        ],
        "chars_repeat":False,   # 是否可能会有重复字符(AA2c这种)
        "chars_num": 4,  # 验证码字符数
        "width": 160,  # 验证码宽度
        "height": 60,  # 验证码高度
        "bg_color": (255, 255, 255),  # 验证码背景色(rgba)
        "font":{
            # "path":"/Users/fizz/www/fonts/MonacoYahei.ttf",
            "path":"",
            "size":32,
            "color":"",
            "name":"",
            # "geo":[(10,10),(50,10),(90,10),(130,10)],   # 字符坐标
        },
        "point": False,  # 是否启用噪点, 默认不启用. 启用后, 则启用 point_param 相关参数配置
        "point_num": 0,  # 噪点个数, 如果为0, 则随机个数(100 ~ 200个)
        "point_color": (0, 0, 0, 0), # 噪点颜色, 如果没有值, 则随机颜色

        "line": False,  # 是否启用干扰线, 默认不启用. 启用后, 则启用 line_param 相关参数配置
        "line_num": 8,  # 噪点个数, 如果为0, 则随机个数(100 ~ 300个)
        "line_width": 0, # 线款
        "line_color": (0, 0, 0, 0),  # 干扰线颜色, 如果没有值, 则随机颜色

        "tilt": True,  # 是否倾斜
        "tilt_angle": 0,  # 倾斜角度, 多少个字符, 则给定多少个值, 没有对应值就随机
    }