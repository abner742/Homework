import pickle
import socket
import threading
import queue
import json  # json.dumps(some)打包   json.loads(some)解包
import configparser
import os

curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "info.ini")

# 创建管理对象
myInfo = configparser.ConfigParser()

# 读ini文件
myInfo.read(cfgpath, encoding="utf-8")

# 获取IP
IP = myInfo.get("info", "IP")
print(IP)
# 获取端口号
PORT = myInfo.get("info", "PORT")
print(PORT)


messages = queue.Queue()
users = []  # 0:用户名 1:连接
lock = threading.Lock()

# 统计当前在线人员
def onlines():
    online = []
    for i in range(len(users)):
        online.append(users[i][0])
    return online


class ChatServer(threading.Thread):
    global users, lock

    def __init__(self):  # 构造函数
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self, conn, addr):  # 接收消息
        # flag代表是否登录成功
        flag = '0'
        while flag != '1':
            # 接收用户请求
            info = conn.recv(1024)
            info = info.decode()
            # 判断注册请求
            if info[0:6] == 'signup':
                # 打开用户文件
                f = open("usersinfo.txt", 'r+', encoding='utf8')    # f.read()读取的是字符串，用eval()将字符串转化为字典
                USER = eval(f.read())
                _, usr_name, usr_pwd = info.split('~')

                if usr_name in USER:                  # 如果已经在名单里面了，即重复注册
                    conn.send('用户已注册'.encode())
                else:                                 # 不在名单内，就注册
                    USER[usr_name] = {'password': usr_pwd}
                    f.seek(0)
                    f.truncate()
                    f.writelines(str(USER))
                    conn.send('注册成功'.encode())
                    f.close()
                continue
            # 处理登录请求
            usr_name, usr_pwd = info.split('~')
            print(usr_pwd + usr_name)
            print(addr)
            f = open("usersinfo.txt", 'r', encoding='utf8')
            USER = eval(f.read())
            if usr_name in USER:               # 如果用户名在名单内
                if usr_pwd == USER[usr_name]['password']:        # 密码正确，登录成功
                    flag = '1'
                    conn.send(flag.encode())
                    print(flag)
                    f.close()
                else:                    # 密码错误， 失败
                    nock = '密码错误'
                    conn.send(nock.encode())
            else:                          # 用户名不在名单内
                nock = '用户名不存在'
                conn.send(nock.encode())
        users.append((usr_name, conn))
        USERS = onlines()
        self.Load(USERS, addr)
        # 在获取用户名后便会不断地接受用户端发来的消息（即聊天内容），结束后关闭连接。
        try:
            while True:
                message = conn.recv(1024)  # 发送消息
                message = message.decode()
                message = usr_name + ':' + message
                self.Load(message, addr)
            conn.close()


        # 如果用户断开连接，将该用户从用户列表中删除，然后更新用户列表。
        except:
            j = 0  # 用户断开连接
            for man in users:
                if man[0] == user:
                    users.pop(j)  # 服务器段删除退出的用户
                    break
                j = j + 1
            USERS = onlines()
            self.Load(USERS, addr)
            conn.close()

    # 将地址与数据（需发送给客户端）存入messages队列。
    def Load(self, data, addr):
        lock.acquire()
        try:
            messages.put((addr, data))

        finally:
            lock.release()

    # 服务端在接受到数据后，会对其进行一些处理然后发送给客户端，如下图，对于聊天内容，服务端直接发送给客户端，而对于用户列表，便由json.dumps处理后发送。
    def sendData(self):  # 发送数据
        while True:
            if not messages.empty():
                message = messages.get()
                if isinstance(message[1], str):
                    for i in range(len(users)):
                        data = ' ' + message[1]
                        users[i][1].send(data.encode())
                        print(data)
                        print('\n')

                if isinstance(message[1], list):
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            users[i][1].send(data.encode())
                        except:
                            pass

    def run(self):
        self.s.bind((IP, int(PORT)))
        self.s.listen(5)
        q = threading.Thread(target=self.sendData)
        q.start()
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.receive, args=(conn, addr))
            t.start()
        self.s.close()


if __name__ == '__main__':
    cserver = ChatServer()
cserver.start()
