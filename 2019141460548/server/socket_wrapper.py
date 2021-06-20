import json


class ClientSockerWrapper(object):
    # 包装client套接字

    def __init__(self, sock):
        self.sock = sock

    def recv_data(self):
        """接受json数据并解码"""
        try:
            json_string = self.sock.recv(1024)
            return json.loads(json_string)
        except:
            return ""

    def send_data(self, dict):
        """接受字典数据，并转换为json数据发送"""
        data = json.dumps(dict)
        return self.sock.send(data.encode('utf-8'))

    def close(self):
        """关闭套接字"""
        self.sock.close()

