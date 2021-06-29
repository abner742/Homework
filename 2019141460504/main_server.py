from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import glob
import os
import sys

#默认设置
HOST = "127.0.0.1"
PORT = 8080
PATH_DEFAULT = "./index.html"


# 处理客户端需求
class HandleRequest(BaseHTTPRequestHandler):
    def do_GET(self):
        print("\n~~~~~~~~~~~~~Connected~~~~~~~~~~~~~\n")
        print("Client Port Number: " + str(self.client_address[1]))
        print("Client IP Address: " + self.address_string())
        print("Socket Family: " + str(self.connection.family))
        print("Socket Type: " + str(self.connection.type))
        print("Socket Address: " + str(self.connection.getsockname()))
        print("Socket Protocol: " + str(self.connection.proto))
        print("Peer Name: " + str(self.connection.getpeername()))

        path_file = check_file(self.path)

        # 如果在
        if path_file is not None:
            self.send_response(200)
            self.end_headers()

            with open(path_file, 'rb') as upload:
                file = upload.read()
                self.wfile.write(file)
        # 如果没在
        else:
            self.send_response(200)
            self.end_headers()

            with open("./wrong.html", 'rb') as upload:
                file = upload.read()
                self.wfile.write(file)
        print("\n~~~~~~~~~~~~~Processed~~~~~~~~~~~~~\n")
        return


class MultiThreadedHTTP(ThreadingMixIn, HTTPServer):
    """
    处理httpserver线程的class
    """

# 检查文件路径是否合法
def check_file(name_file):
    if name_file == '/':
        return PATH_DEFAULT
    # 文件路径是否合法
    else:
        track = glob.glob("." + name_file)
        if not track:  # 如果不存在这样的道路
            return None
        else:
            for path in track:
                if os.path.isfile(path):
                    return path  # 找到了
            return None


if __name__ == '__main__':
    if len(sys.argv) == 2:
        portSettedNumber = int(sys.argv[1])
        PORT = portSettedNumber
    else:
        print("默认端口号为8080")

    try:
        server = MultiThreadedHTTP((HOST, PORT), HandleRequest)
        print("等待请求....\n")
        server.serve_forever()
    except:
        server.server_close()  # 关闭服务器