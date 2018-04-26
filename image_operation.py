from PIL import Image
# from matplotlib import pyplot as plt

# 图片的背景颜色, 缩放图片, 填充背景色时会用到
BG_COLOR = None

# 图片缩放
def image_resize(image, size=(160, 60), fill_color=None):
    """
    缩放图片不变形, 并填充空白处为指定颜色,默认为黑色
    实现思路:
    1.比对目标图片和原始图片的长宽比,如果相同,则直接缩放,如果不同,则以目标的长宽比做一个画布
    2.比对长和宽,做等比缩放
    3.缩放后的图片粘贴到画布上,根据缺失部分,计算2分处填充
    :param image: 图片, pil图片流
    :param size: 尺寸
    :param fill: 是否填充缩放, 默认是
    :param fill_color: 填充颜色, 默认黑色
    :return: 新的图片流
    """
    if fill_color == 'auto':
        if BG_COLOR is not None:
            fill_color = BG_COLOR
        else:
            fill_color = (255, 255, 255, 0)
    # 源文件长宽
    src_width, src_height = image.size
    src_ratio = float(src_width) / float(src_height)
    # 目标文件长宽
    dst_width, dst_height = size[0], size[1]
    dst_ratio = float(dst_width) / float(dst_height)

    # 比例相同, 或者不需要填充缩放, 就直接缩放并返回
    if dst_ratio == src_ratio or fill_color is None:
        print(dst_ratio, src_ratio)
        return image.resize((dst_width, dst_height), Image.ANTIALIAS)

    if dst_ratio < src_ratio:
        # 缩放尺寸
        resize_width = dst_width
        resize_height = resize_width / src_ratio
        # 层叠图片坐标
        x_offset = 0
        y_offset = float(dst_height - resize_height) / 2
    else:
        # 缩放尺寸
        resize_height = dst_height
        resize_width = resize_height * src_ratio
        # 层叠图片坐标
        x_offset = float(dst_width - resize_width) / 2
        y_offset = 0
    # img = img.crop((x_offset, y_offset, x_offset + int(crop_width), y_offset + int(crop_height)))
    # 开始缩放
    img_resize = image.resize((int(round(resize_width)), int(round(resize_height))), Image.ANTIALIAS)

    # 创建一个画布放于底层
    img_canvas = Image.new('RGBA', (dst_width, dst_height), fill_color)
    img_canvas.paste(img_resize, (int(round(x_offset)), int(round(y_offset))))
    return img_canvas


# 获取灰度转二值的映射table
def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    color_black = 0
    color_white = 0
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
            color_black += 1
        else:
            table.append(1)
            color_white += 1

    global BG_COLOR
    if (color_black > color_white):
        BG_COLOR = (255, 255, 255, 255)
    else:
        BG_COLOR = (0, 0, 0, 255)

    return table


# 9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
    :param img: Image
    :param x:
    :param y:
    :return:
    """
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum


# 根据噪点的位置信息，消除二值图片的黑点噪声
def remove_noise_pixel(img, noise_point_list):
    """
    根据噪点的位置信息，消除二值图片的黑点噪声
    :type img:Image
    :param img:
    :param noise_point_list:
    :return:
    """
    for item in noise_point_list:
        img.putpixel((item[0], item[1]), 1)


# 获取干净的二值化去噪点后的图片
def get_clear_bin_image(image, threshold=140):
    """
    获取干净的二值化的图片。
    图像的预处理：
    1. 先转化为灰度
    2. 再二值化
    3. 然后清除噪点
    参考:http://python.jobbole.com/84625/
    :type img:Image
    :return:
    """
    imgry = image.convert('L')  # 转化为灰度图

    table = get_bin_table(threshold)
    out = imgry.point(table, '1')  # 变成二值图片:0表示黑色,1表示白色

    # noise_point_list = []  # 通过算法找出噪声点,第一步比较严格,可能会有些误删除的噪点
    # for x in range(out.width):
    #     for y in range(out.height):
    #         res_9 = sum_9_region(out, x, y)
    #         if (0 < res_9 < 3) and out.getpixel((x, y)) == 0:  # 找到孤立点
    #             pos = (x, y)  #
    #             noise_point_list.append(pos)
    # remove_noise_pixel(out, noise_point_list)
    return out


if __name__ == "__main__":
    # img_path = "./images/test2.png"
    img_path = "/Users/fizz/www/tmp/cache/index.jpeg"
    # img_path = requests.get("http://www.hust-snde.com/center/sso/authimg?"+str(random.random()))
    # print(Image.open(img_path.content))
    # exit()
    im = Image.open(img_path)

    # 二值去噪
    im = get_clear_bin_image(im)

    # plt.imshow(im)
    # plt.show()

    # # resize 缩放
    # size = (100, 100)
    # im = image_resize(im, size, (255, 255, 255, 100))
    #
    im.show()

    # # 保存
    # modified_path = "./images/test2.png"
    # im.save(modified_path)
