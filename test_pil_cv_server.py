# -*- coding: utf-8 -*-

"""TCP Server Sample"""

import gevent
from gevent.server import StreamServer
from delay import timeout_partial

import cv2
import numpy as np

class TCPManager(gevent.Greenlet):
    
    def __init__(self, port):
        self.port = port
        gevent.Greenlet.__init__(self)

    def _connection_handler(self, sock, addr):
        print("New Connection From {0}:{1}".format(addr, sock.getsockname()))
        data = b''
        exit = 0
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
                    img = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
                    # cv2.imshow(addr[0], img) # 正常来说一个 ip 只有一个窗口，所以只会同步到一个窗口上
                    cv2.imshow(str(addr), img) # 多例测试，方便做接收压力测试
                    cv2.waitKey(10)
                    #if jpeg_bytes[6:10] in (b'JFIF', b'Exif'): # 个别jpg编码文件不规范，会导致解码失败
                        #img = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
                        # cv2.imshow(addr[0], img) # 正常来说一个 ip 只有一个窗口，所以只会同步到一个窗口上
                        #cv2.imshow(str(addr), img) # 多例测试，方便做接收压力测试
                        #cv2.waitKey(10)
                elif len(data) > 1024*1024: # 过大都没有收到尾部则放弃这个buffer
                    data = b''
            # except ConnectionResetError as e:
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                break

    def _run(self):
        print("TCP server Listen at port {0}".format(self.port))
        server = StreamServer(('0.0.0.0', self.port), self._connection_handler)
        server.serve_forever()


if __name__ == "__main__":
    ob = TCPManager(7000) # 这个是通过协程执行的,所以下面需要wait等待
    ob.start()
    gevent.wait()
    