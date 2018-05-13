import os

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

STATIC_APP_DIR = os.path.join(settings.STATIC_ROOT, 'ryanair_app/assets')


def banner1(destination, price):
    im = Image.open(f"{STATIC_APP_DIR}/banner1.png")
    draw = ImageDraw.Draw(im)
    draw.text((180, 20), "Flights to ",
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-LightSemiExt.otf", size=30), fill=0x964016)
    draw.text((310, 20), destination,
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-Bold_0.otf", size=30), fill=0x964016)
    draw.text((240, 50), "starts from ",
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-LightSemiExt.otf", size=30), fill=0x964016)
    draw.text((390, 50), str(price),
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-Bold_0.otf", size=30), fill=0x964016)
    del draw
    return save_image(im, destination, price, 1)

def banner2(destination, price):
    im = Image.open(f"{STATIC_APP_DIR}/banner2.png")
    draw = ImageDraw.Draw(im)
    draw.text((105, 25), "Flights to",
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-LightSemiExt.otf", size=30), fill=0x964016)
    w, h = draw.textsize(destination,
                         font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-Bold_0.otf", size=60))
    draw.text(((336-w)/2, 65), destination,
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-Bold_0.otf", size=60), fill=0x964016)
    draw.text((70, 130), "starts from",
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-LightSemiExt.otf", size=30), fill=0x964016)
    draw.text((220, 125), str(price),
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-Bold_0.otf", size=40), fill=0x964016)
    del draw
    return save_image(im, destination, price, 2)


def save_image(im, destination, price, index):
    fname = f'{destination}_for_{price}__{index}.png'.lower()
    image_path = os.path.join(settings.BANNERS_ROOT, fname)
    im.save(image_path)
    return f'{settings.MEDIA_URL}banners/{fname}'
