
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
        
    import threading
    from socket import *
    import time
    from typing import Optional
    
    class DataRec(threading.Thread):
        tcp_client: Optional[socket]
    
        def __init__(self, ip, port):
            threading.Thread.__init__(self, name="data rec")
            self.ip = ip
            self.port = port
            self.tcp_client = None
    
        def wait_tcp_connect(self):
            while self.tcp_client is None:
                time.sleep(1)
                self.tcp_client = socket(AF_INET, SOCK_STREAM)
                try:
                    print('try to init client {}:{}'.format(self.ip, self.port))
                    self.tcp_client.connect((self.ip, self.port))
                    print('client inited!')
                except Exception as e:
                    self.tcp_client = None
                    print("client init failed, waiting for server!")
    
        def run(self):
            self.wait_tcp_connect()
            msg_buffer = ''
            while True:
                try:
                    time.sleep(0.05) # 20fps
                    from PIL import Image, ImageDraw
                    img = Image.new('RGB', (640, 480), (255, 255, 255))
                    draw = ImageDraw.Draw(img)
                    tmp = Image.effect_noise(size=(640, 480), sigma=32)
                    img.paste(tmp, (0, 0))
                    draw.line((0, 0) + img.size, fill=128)
                    draw.rectangle((50, 25, 300, 375), fill=0)
                    draw.text((50, 25), str(time.time()), fill=(255, 255, 255))
                    jpg_bytes = io.BytesIO()
                    img.save(jpg_bytes, format='JPEG')
                    jpg_bytes.seek(0)
                    self.tcp_client.send(jpg_bytes.getvalue())
                    print('loop send jpg')
                    
                    # self.tcp_client.send('hello from client'.encode('utf-8'))
                    # msg_bits = self.tcp_client.recv(1024*8)
                    # if not msg_bits:
                    #     continue
    
                    # msg_str = msg_bits.decode('utf-8')
    
                    # print("rec: {}".format(msg_str))
    
                except error as msg:
                    print('client rec msg catch error({} - {})'.format(error, msg))
                    self.tcp_client.close()
                    self.tcp_client = None
                    self.wait_tcp_connect()
                    msg_buffer = ''
                # except Exception as e:
                #     print("client cat other error({})".format(e))

    data_rec = DataRec('0.0.0.0', 7000)
    data_rec.start()
    while data_rec.is_alive():
        time.sleep(1)

