
import time
import io
from PIL import Image, ImageDraw, UnidentifiedImageError
import cv2
import numpy as np
import socket

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

def test_jpeg(bytes):
    """JPEG data in JFIF or Exif format"""
    result = None
    # if bytes[6:10] in (b'JFIF', b'Exif'):
    #     return 'jpeg'
    if bytes.startswith(b'\xff\xd8') and bytes.endswith(b'\xff\xd9'):
        result = 'jpeg'
    return result
    
def test_send_jpg(sock, jpg_bytes):
    # jpg_bytes.seek(0) # test bad jpeg
    # jpg_bytes.write(b'\xee')
    if test_jpeg(jpg_bytes.getvalue()) == "jpeg":
        sock.send(jpg_bytes.getvalue())

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(('127.0.0.0', 7000))
    # test_send_jpg(sock, test_data_jpg())
    while True:
        try:
            sock.connect(('127.0.0.1', 7000))
            while True:
                # test_send_jpg(sock, test_data_jpg())
                sock.send('hello'.encode())
                print(time.time())
        except ConnectionRefusedError:
            print("ConnectionRefusedError")
            time.sleep(1)
        except BrokenPipeError:
            print("BrokenPipeError")
            time.sleep(1)
        print(time.time())
