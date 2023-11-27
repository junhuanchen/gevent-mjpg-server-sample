# get-started

## 配置环境 

pipenv shell

pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

主要就 gevent opencv-python Pillow 模块

## 使用方法

### 回环测试

`python test_pil_cv.py`



### 打开服务端

`python test_pil_cv_server.py`

```python
while True:
    try:
        ret = timeout_partial(30, sock.recv, 1024)
        if isinstance(ret, BaseException):
            exit += 1
            if exit > 3:
                break
        elif len(ret) == 0:
            break
        else:
            exit = 0
            data += ret
        if data.startswith(b'\xff\xd8') and b'\xff\xd9' in data:
            # 表示存在一张 jpeg 图像则切开它
            jpeg_end = data.find(b'\xff\xd9')
            jpeg_bytes = data[:jpeg_end+2]
            data = data[jpeg_end+2:]
            # print("jpeg_bytes: ", jpeg_bytes)
            if jpeg_bytes[6:10] in (b'JFIF', b'Exif'):
                img = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
                # cv2.imshow(addr[0], img) # 正常来说一个 ip 只有一个窗口，所以只会同步到一个窗口上
                cv2.imshow(str(addr), img) # 多例测试，方便做接收压力测试
                cv2.waitKey(10)
        elif len(data) > 1024*1024: # 过大都没有收到尾部则放弃这个buffer
            data = b''
    # except ConnectionResetError as e:
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        break

```

### 打开客户端

`python test_pil_cv_client.py`

就会自动连接本地的 ip 地址进行回环测试，板子 tcp 连接只需要循环发送 mjpg 图像到服务端即可。

关键代码：

```python
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
    except error as msg:
        print('client rec msg catch error({} - {})'.format(error, msg))
        self.tcp_client.close()
        self.tcp_client = None
        self.wait_tcp_connect()
        msg_buffer = ''
```
