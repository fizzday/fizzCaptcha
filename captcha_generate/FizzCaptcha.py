import random

from fizzCaptcha.captcha_generate import config
from PIL import Image, ImageDraw, ImageFont, ImageOps
from matplotlib import pyplot as plt


class FizzCaptcha(object):
    def __init__(self):
        # self.text = ""
        # self.config = dict()
        # self.image = ""
        pass

    # 获取字符
    def getText(self):
        config = self.config
        text = list()
        # 获取text类型
        letter = ""
        for item in config["chars"]:
            letter += config[item]

        # 获取具体字符
        if config["chars_repeat"]:  # 有重复字符, 一次从字符列表中获取一个, 可能有重复字符
            for i in range(config["chars_num"]):
                text = text+(random.sample(letter, 1))
        else:  # 一次获取指定个数, 不会有重复字符
            text = random.sample(letter, config["chars_num"])

        return text

    # 获取坐标
    def _getPos(self):
        config = self.config
        if config["font"]["geo"]:
            return config["font"]["geo"]

        # 随机坐标
        pos = []
        gap = 5  # 间隔
        start = 0  # 起始坐标
        for i in range(0, config["chars_num"]):
            x = start + self.config["font"]["size"] * i + random.randint(0, gap) + gap * i
            y = random.randint(-5, 5)
            pos.append((x, y))

        return pos

    # 设置配置
    def setConfig(self, config):
        self.config = config
        return self


    def randRGB(self):
        return (random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))

    def randPoint(self):
        (width, height) = self.config["width"],self.config["height"]
        return (random.randint(0, width), random.randint(0, height))

    # 画干扰线
    def drawLine(self):
        config = self.config
        # 线条数
        num = config["line_num"] if config["line_num"] else random.randint(1,2)

        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            fill = random.sample(self.config["line_color"],1)[0] if self.config["line_color"] else None
            draw.line((self.randPoint(),self.randPoint()), fill=fill, width=self.config["line_width"])
        del draw

    # 画噪点
    def drawPoint(self):
        config = self.config
        # 噪点数
        num = config["point_num"] if config["point_num"] else random.randint(100,200)

        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            fill = random.sample(self.config["point_color"],1)[0] if self.config["point_color"] else None
            draw.point(self.randPoint(), fill=fill)
        del draw

    def rotate(self):
        self.image.rotate(random.randint(-45, 45), expand=1)

    # 画板上写字
    def drawText(self):
        # 获取随机字符
        self.text = self.getText()

        # 获取字体坐标
        pos = self._getPos()
        # 获取字体
        fontPath = self.config["font"]["path"] if self.config["font"]["path"] else None
        # 设置大小
        font = ImageFont.truetype(font=fontPath, size=self.config["font"]["size"])

        # 倾斜


        # 开启写字模式
        # draw = ImageDraw.Draw(self.image)

        # 根据坐标写字
        for item in pos:
            index = pos.index(item)
            text = self.text[index]
            # # 获取字体颜色
            fill = self.config["font"]["color"][index] if self.config["font"]["color"] else self.randRGB()
            # draw.text(item, text, fill=fill, font=font)
            width, height = font.getsize(text)
            image2 = Image.new('RGBA', (width, height))
            draw2 = ImageDraw.Draw(image2)
            draw2.text((0, 0), text=text, font=font, fill=fill)
            image2 = image2.rotate(random.randint(-45,45), expand=1)
            self.image.paste(image2, item, image2)
            del draw2
            # # # f = ImageFont.load_default()
            # txt = Image.new('RGBA', (40, 60), (0, 0, 128, 92))
            # d = ImageDraw.Draw(txt)
            # d.text((0, 0), text=text, font=font, fill=fill)
            # w = txt.rotate(17.5, expand=1)
            # # # plt.imshow(txt)
            # # # plt.show()
            # # # exit()
            # # #
            # # # self.image.paste(ImageOps.colorize(w, (0, 0, 0), (255, 255, 84)), (100, 60), w)
            # self.image.paste(w, (100, 60), w)

            # self.rotate()

        # del draw

    # 获取验证码
    def getCaptcha(self, save=""):
        config = self.config
        # 创建画布
        self.image = Image.new("RGB", (config["width"], config["height"]), config["bg_color"] if config["bg_color"] else 0)

        # 画干扰线
        self.drawLine()

        # 画噪点
        self.drawPoint()

        # 写字
        self.drawText()

        # 保存
        if save:
            self.image.save(save)

        return self.image, self.text


if __name__ == '__main__':

    conf = config.config

    fc = FizzCaptcha().setConfig(conf)

    image, text = fc.getCaptcha(save="./a.png")

    print(text)

    plt.imshow(image)

    plt.show()
