# 聊天室项目开发

# 所需要导入的包

# 套接字编程包导入
import socket
# 线程包导入
from threading import Thread
# 时间包导入
import time



class server:

    # 初始方法
    def __init__(self):
        # 无参数默认ipv4，tcp协议
        self.server = socket.socket()
        # 绑定ip,bind((ip地址,端口号))
        self.server.bind(("127.0.0.1",8989))
        # 设置最大挂起数量
        self.server.listen(5)
        # 设置所有的客户端
        self.clients=[]
        # 使用用户名字与ip的绑定信息设置用户字典
        self.clients_username_ip={}
        # 创建实例时开始连接
        self.get_conn()


    # 监听客户端连接
    def get_conn(self):
        while True:
            # 获取连接客户端的信息
            client,address=self.server.accept()
            print(address)
            data="与服务器连接成功！请你输入昵称才可以聊天。"
            # server与client通信通过send()(!!需要encode())和recv()(!!需要decode())
            client.send(data.encode())
            # 把连接的用户添加到服务器的用户列表当中
            self.clients.append(client)
            # 服务器启动多个线程，处理每个客户端的消息，一个线程维护一个客户端
            Thread(target=self.get_msg,args=(client,self.clients,self.clients_username_ip,address)).start()


    # 进行所有客户端的消息处理
    def get_msg(self,client,clients,clients_username_ip,address):
        # 接收客户端发来的昵称
        username=client.recv(1024).decode()
        print("from client "+username)
        # 将昵称与ip绑定
        clients_username_ip[address]=username
        # 循环监听所有客户端的消息
        while True:
            # 异常检测，获取用户的所有发送的消息
            try:
                recv_data=client.recv(1024).decode()
            # 抛出任何异常
            except Exception as e:
                # 直接break退出
                self.close_client(client,address)
                break

            #如果用户退出，输入Q
            if recv_data.upper()=="Q":
                self.close_client(client,address)
                break
            # 给每一个用户发送信息
            for c in clients:
                # 谁在什么时候发送了什么消息
                c.send((clients_username_ip[address]+" "+time.strftime("%x")+"\n"+recv_data).encode())


    # 关闭资源
    def close_client(self,client,address):
        self.clients.remove(client)
        client.close()
        print(self.clients_username_ip[address]+"已经离开了")
        for c in self.clients:
            c.send((self.clients_username_ip[address]+"已经离开了").encode())


if __name__=='__main__':
    server()




