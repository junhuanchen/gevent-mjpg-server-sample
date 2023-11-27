
import time
import io
from PIL import Image, ImageDraw, UnidentifiedImageError
import cv2
import numpy as np

def test_data_jpg():
    img = Image.new('RGB', (200, 100), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.line((0, 0) + img.size, fill=128)
    draw.rectangle((50, 25, 150, 75), fill=0)
    draw.text((50, 25), str(time.time()), fill=(255, 255, 255))
    jpg_bytes = io.BytesIO()
    img.save(jpg_bytes, format='JPEG')
    jpg_bytes.seek(0)
    return jpg_bytes

def test_tcp_jpg(tcp_bytes):
    jpg_bytes = io.BytesIO()
    jpg_bytes.write(tcp_bytes)
    return jpg_bytes

def test_jpeg(bytes):
    """JPEG data in JFIF or Exif format"""
    result = None
    if bytes.startswith(b'\xff\xd8') and bytes.endswith(b'\xff\xd9') and bytes[6:10] in (b'JFIF', b'Exif'):
        result = 'jpeg'
    return result
    
def test_show_jpg(jpg_bytes):
    # jpg_bytes.seek(0) # test bad jpeg
    # jpg_bytes.write(b'\xee')
    if test_jpeg(jpg_bytes.getvalue()) == "jpeg":
        img = cv2.imdecode(np.frombuffer(jpg_bytes.getvalue(), np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('test1', img)
        cv2.imshow('test2', img)
        cv2.waitKey(10)

test_show_jpg(test_data_jpg())

if __name__ == '__main__':
    while True:
        test_show_jpg(test_data_jpg())
        print(time.time())
