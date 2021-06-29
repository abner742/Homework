import socket
from config import *
import json


class ClientSocket(socket.socket):
    """客户端套接字的封装"""

    def __init__(self):
        # 设置为TCP套接字
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        """自动连接到服务器"""
        super(ClientSocket, self).connect((SERVER_IP, SERVER_PORT))

    def recv_data(self):
        """接收json数据，并解码"""
        try:
            json_string = self.recv(512)
            return json.loads(json_string)
        except:
            return ""

    def send_data(self, dict):
        """接收字典数据，并转换为json数据发送"""
        data = json.dumps(dict)
        return self.send(data.encode('utf-8'))