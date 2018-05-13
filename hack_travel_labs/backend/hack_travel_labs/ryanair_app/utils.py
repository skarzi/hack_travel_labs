import os

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

STATIC_APP_DIR = os.path.join(settings.STATICFILES_DIRS[0], 'ryanair_app/assets')


def banner1(destination, price):
    im = Image.open(f"{STATIC_APP_DIR}/banner1.png")
    draw = ImageDraw.Draw(im)
    draw.text((180, 20), "Flights to ",
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-LightSemiExt.otf", size=30), fill=0x964016)
    draw.text((310, 20), destination,
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-Bold_0.otf", size=30), fill=0x964016)
    draw.text((240, 50), "starts from ",
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-LightSemiExt.otf", size=30), fill=0x964016)
    draw.text((390, 50), price,
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-Bold_0.otf", size=30), fill=0x964016)
    del draw
    return im

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
    draw.text((220, 125), price,
              font=ImageFont.truetype(f"{STATIC_APP_DIR}/MyriadPro-Bold_0.otf", size=40), fill=0x964016)
    del draw
    return im
