import pickle
import socket
import threading
import queue
import json  # json.dumps(some)打包   json.loads(some)解包
import config


Server_IP = config.Server_IP
PORT = int(config.Server_Port)
print(Server_IP)
print(PORT)
# Server_IP = '127.0.0.1'
# PORT = 9999

messages = queue.Queue()
users = []   # 0:用户名 1:连接
lock = threading.Lock()

def onlines():    # 统计当前在线人员
    online = []
    for i in range(len(users)):
        online.append(users[i][0])
    return online

class ChatServer(threading.Thread):
    global users,lock

    def __init__(self):         # 构造函数
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self, conn, addr):             # 接收消息
        # ack判断验证是否通过
        ack='0'
        while(ack!='1'):
            info = conn.recv(1024)        #接收用户登陆请求
            info = info.decode()
            print(info)
            # 处理注册
            if(info[0:3]=='reg'):
                with open('usrs_info.pickle', 'rb') as usr_file:
                    usrs_info = pickle.load(usr_file)
                    usr_file.close()
                    _,usr_name,usr_pwd = info.split('~')
                    # 判断是否重复注册
                    if(usr_name in usrs_info):
                        conn.send('用户已经注册'.encode())
                    else:
                        usrs_info.setdefault(usr_name,usr_pwd)
                        with open('usrs_info.pickle', 'wb') as usr_file:
                            pickle.dump(usrs_info,usr_file)
                            usr_file.close()
                        conn.send('注册成功！'.encode())
                    continue
            usr_name,usr_pwd = info.split('~')
            print(usr_pwd+usr_name)
            print(addr)
            try:
                with open('usrs_info.pickle', 'rb') as usr_file:
                    usrs_info = pickle.load(usr_file)
            except FileNotFoundError:
                with open('usrs_info.pickle', 'wb') as usr_file:
                    # 没有文件创建管理员
                    usrs_info = {'admin': 'admin'}
                    pickle.dump(usrs_info, usr_file)
            if usr_name in usrs_info:
                if usr_pwd == usrs_info[usr_name]:
                    ack='1'
                    conn.send(ack.encode())
                    print(ack)
                else:
                    nock='密码错误'
                    conn.send(nock.encode())
            else:
                nock = '用户名不存在'
                conn.send(nock.encode())
        users.append((usr_name, conn))
        USERS = onlines()
        self.Load(USERS,addr)
        # 在获取用户名后便会不断地接受用户端发来的消息（即聊天内容），结束后关闭连接。
        try:
            while True:
                message = conn.recv(1024)            # 发送消息
                message = message.decode()
                message = usr_name + ':' + message
                self.Load(message,addr)
            conn.close()


        # 如果用户断开连接，将该用户从用户列表中删除，然后更新用户列表。
        except:
            j = 0            # 用户断开连接
            for man in users:
                if man[0] == user:
                    users.pop(j)       # 服务器段删除退出的用户
                    break
                j = j+1
            USERS = onlines()
            self.Load(USERS,addr)
            conn.close()

# 将地址与数据（需发送给客户端）存入messages队列。
    def Load(self, data, addr):
        lock.acquire()
        try:
            messages.put((addr, data))

        finally:
            lock.release()

    # 服务端在接受到数据后，会对其进行一些处理然后发送给客户端，如下图，对于聊天内容，服务端直接发送给客户端，而对于用户列表，便由json.dumps处理后发送。
    def sendData(self): # 发送数据
        while  True:
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
        self.s.bind((Server_IP,PORT))
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
