import socket
from config import *


class ServerSoket(socket.socket):

    def __init__(self):
        # 初始化
        super(ServerSoket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定ip地址和端口号
        self.bind((SERVER_IP, SERVER_PORT))
        # 设置监听数量
        self.listen(128)


