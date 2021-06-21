import socket
import sys
from threading import Thread
import time

server_socket = None
clients = []
clients_name_ip = {}


# 关闭资源
def close_client(client, address):
    clients.remove(client)
    client.close()

    print(clients_name_ip[address] + "已经离开")
    for c in clients:
        c.send((clients_name_ip[address] + "已经离开").encode())


# 进行所有客户端信息处理
def get_msg(client, address):
    # 接收客户端发来的昵称
    name = client.recv(1024).decode()
    print("来自以下地址的连接, name: " + name)
    # 昵称与IP绑定
    clients_name_ip[address] = name
    client.send(("你的昵称是: " + name).encode())
    # 循环监听客户端信息
    while True:
        # 获取所有客户发送的信息
        try:
            rec_data = client.recv(1024).decode()
        except Exception as e:
            close_client(client, address)
            break
        # 如果用户退出，输入Q
        if rec_data.upper() == "Q":
            close_client(client, address)
            break
        for c in clients:
            # 谁在什么时候发送信息
            details = " " + time.strftime("%x") + " " + clients_name_ip[address] + ": " + rec_data
            c.send(details.encode())
            print(details)


# 监听客户端连接
def get_conn():
    while True:
        # 获取连接客户端信息
        client, address = server_socket.accept()
        print("来自以下地址的连接, client: ", client)
        print("来自以下地址的连接, address: ", address)
        data = "与服务器连接成功！\n请输入昵称"
        # server与client通信 send（）
        client.send(data.encode())
        # 连接的用户添加到服务器的用户列表中
        clients.append(client)
        # 服务器启动多个线程处理每个客户端的消息
        Thread(target=get_msg, args=(client, address)).start()


def main(addr_ip, addr_port):
    global server_socket
    server_socket = socket.socket()
    server_socket.bind((addr_ip, int(addr_port)))
    server_socket.listen(5)
    get_conn()


if __name__ == '__main__':
    # main(input("ip"), input("port"))
    print(sys.argv[1])
    print(sys.argv[2])
    main(sys.argv[1], sys.argv[2])
