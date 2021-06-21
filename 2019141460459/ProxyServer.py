from socket import *
import threading
import os
import sys
# 未引第三方库，环境配置文档为空

def communicate(sock1, sock2):
    # 循环将sock1发来的消息转发给sock2
    try:
        while True:
            data = sock1.recv(1024)
            sock2.sendall(data)
    except:
        pass


def proxy(server_socket, addre):
    try:
        while True:
            message = server_socket.recv(4096)
            method = message.split()[0].decode()

            # 处理经由http connect 进行的http隧道
            # 此时不存在缓存功能，单纯在客户端与远程服务器之间转发报文
            if method == 'CONNECT':
                # 建立与远程服务器的连接，并设置超时，超时会断开连接
                server_socket.settimeout(60)
                client_socket = socket(AF_INET, SOCK_STREAM)
                client_socket.settimeout(60)

                # 对请求进行解析，得到远程服务器地址和端口，如未指定端口则与80端口进行通讯
                host = message.split()[4].decode().split('/')[0].partition(":")[0]
                port = message.split()[4].decode().split('/')[0].partition(":")[2]
                if port == '':
                    client_socket.connect((host, 80))
                else:
                    client_socket.connect((host, int(port)))

                # 与成功建立连接后发给客户端200 ok
                server_socket.sendall("HTTP/1.0 200 Connection established\r\n\r\n".encode())

                # 新建线程，与本线程共同处理来自客户端和远程服务器的通讯
                threading.Thread(target=communicate, args=(server_socket, client_socket)).start()
                communicate(client_socket, server_socket)
                break

            # 处理http get请求
            if method == 'GET':
                # 设置超时，超时会断开连接
                server_socket.settimeout(1)

                # 对请求进行解析，得到远程服务器地址和端口，如未指定端口则与80端口进行通讯
                hosturl = message.split()[1].decode().partition("//")[2]
                if len(hosturl) == 0:
                    server_socket.send("HTTP/1.0 404 Not Found\r\n".encode())
                    continue
                host = message.split()[4].decode().split('/')[0].partition(":")[0]
                port = message.split()[4].decode().split('/')[0].partition(":")[2]

                # 构建缓存文件所在路径
                path = (os.getcwd() + '\\cache\\' + host)[0:250]
                if not os.path.exists(path):
                    os.makedirs(path)
                filename = ("./cache/" + host + "/" + hosturl.replace('/', '_').replace('?', '_') + ".cache")[0:250]

                try:
                    # 尝试读取缓存，如果存在则直接从文件中读取发给客户端
                    with open(filename, "rb") as f:
                        while 1:
                            tmp = f.read(2048)
                            if not tmp:
                                break
                            server_socket.send(tmp)
                        print('Read from cache')
                except IOError:
                    # 抛出IOError证明不存在缓存文件或缓存文件读取出错，则向远程服务器请求
                    client_socket = socket(AF_INET, SOCK_STREAM)
                    client_socket.settimeout(1)
                    if port == '':
                        client_socket.connect((host, 80))
                    else:
                        client_socket.connect((host, int(port)))
                    # 建立连接并向远程服务器发出消息
                    client_socket.send(message)

                    # 新建缓存文件并进行写入
                    cache_file = open(filename, "wb")
                    try:
                        while 1:
                            tmp = client_socket.recv(4096)
                            server_socket.send(tmp)
                            cache_file.write(tmp)
                        cache_file.close()
                    # 发生超时时连接会自动关闭，但文件关闭需要在错误处理中进行
                    except timeout:
                        cache_file.close()

            # 处理http post请求
            # 此时不进行缓存
            if method == 'POST':
                # 设置超时，超时会断开连接
                server_socket.settimeout(1)

                # 对请求进行解析，得到远程服务器地址和端口，如未指定端口则与80端口进行通讯
                hosturl = message.split()[1].decode().partition("//")[2]
                if len(hosturl) == 0:
                    server_socket.send("HTTP/1.0 404 Not Found\r\n".encode())
                    continue
                host = message.split()[4].decode().split('/')[0].partition(":")[0]
                port = message.split()[4].decode().split('/')[0].partition(":")[2]

                client_socket = socket(AF_INET, SOCK_STREAM)
                client_socket.settimeout(1)
                if port == '':
                    client_socket.connect((host, 80))
                else:
                    client_socket.connect((host, int(port)))
                # 建立连接并向远程服务器发出消息
                client_socket.send(message)
                threading.Thread(target=communicate, args=(server_socket, client_socket)).start()
                communicate(client_socket, server_socket)
    except :
        pass
    server_socket.close()
    return


if __name__ == '__main__':
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    # 可根据参数选择接口 默认跑在10800端口上
    if len(sys.argv) > 1:
        tcpSerSock.bind(('', int(sys.argv[1])))
    else:
        tcpSerSock.bind(('', 8080))

    tcpSerSock.listen(100)
    # 缓存保存目录在python文件所在目录的cache文件夹下
    path = os.getcwd() + '\\cache\\'
    if not os.path.exists(path):
        os.makedirs(path)
    print('Ready to serve...')
    # 将连接分配给新建的线程进行处理
    while True:
        tcpCliSock, addr = tcpSerSock.accept()
        threading.Thread(target=proxy, args=(tcpCliSock, addr)).start()
