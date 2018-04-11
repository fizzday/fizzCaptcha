from PIL import Image
from PIL import ImageFont, ImageDraw, ImageOps

from fizzCaptcha.captcha_generate import config
from matplotlib import pyplot as plt

# im=Image.open("a.png")
# imnew=Image.new("RGB", (config["width"], config["height"]), config["bg_color"] if config["bg_color"] else 0)
# imnew.show()
# exit()
f = ImageFont.load_default()
txt=Image.new('L', (40,50))
d = ImageDraw.Draw(txt)
d.text( (0, 0), "Someplace Near Boulder",  font=f, fill=255)
w=txt.rotate(17.5,  expand=1)
w.show()
#
# # im.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), (0,0),  w)
# # im = Image.open(imnew)
# imnew.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), (0,10), w)
#
# plt.imshow(imnew)
# plt.show()
