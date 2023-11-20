
import time
from PIL import Image, ImageDraw
import cv2

def test_show_jpg():
    img = Image.new('RGB', (200, 100), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.line((0, 0) + img.size, fill=128)
    draw.rectangle((50, 25, 150, 75), fill=0)
    draw.text((50, 25), str(time.time()), fill=(255, 255, 255))
    img.save('/tmp/test.jpg')

    img = cv2.imread('/tmp/test.jpg')
    cv2.imshow('test1', img)
    cv2.imshow('test2', img)
    cv2.waitKey(1)

while True:
    test_show_jpg()
    print(time.time())
