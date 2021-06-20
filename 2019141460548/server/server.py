from DB import DB
from server_socket import ServerSoket
from socket_wrapper import ClientSockerWrapper
from threading import Thread
from config import *
from response_protocol import *


class Server(object):

    def __init__(self):

        self.server_socket = ServerSoket()

        # 创建请求的id和方法关联字典
        self.request_handle_function = {}

        # 注册处理函数到字典
        self.register(REQUEST_LOGIN, self.request_login_handle)
        self.register(REQUEST_CHAT, self.request_chat_handle)
        self.register(REQUEST_REGISTER, self.request_register_handle)

        # 创建保护当前在线用户的字典
        self.clients = {}

        # 创建数据库管理对象
        self.db = DB()

    def register(self, request_id, handle_function):
        """注册处理函数"""
        self.request_handle_function[request_id] = handle_function

    def startup(self):

        while True:
            # 获取客户端连接
            print("正在获取客户端连接")
            soc, addr = self.server_socket.accept()
            print("获取到客户端连接")

            # 封装client的soc
            client_soc = ClientSockerWrapper(soc)
            # 交给子线程处理
            Thread(target=lambda: self.request_handle(client_soc)).start()

    def request_handle(self, client_soc):
        # 处理客户端请求
        while True:
            # 接受客户端数据
            recv_data = client_soc.recv_data()
            if not recv_data:
                # 没有接收到数据，关闭套接字
                self.remove_offline_user(client_soc)
                client_soc.close()
                break

            # 解析数据
            parse_data = self.parse_request_text(recv_data)

            # 分析请求类型，并根据请求类型调用相应的处理函数
            # 根据request_id获取字典中对应的处理函数并返回给handle_function
            handle_function = self.request_handle_function.get(parse_data['request_id'])
            if handle_function:
                handle_function(client_soc, parse_data)

    def remove_offline_user(self, client_soc):
        # 客户端下线的处理
        print("有客户端下线了")
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                del self.clients[username]
                # 更新在线用户列表
                self.send_user_list()
                break

    def parse_request_text(self, recv_data):
        """解析客户端发送来的数据"""
        # 登录信息：001 username password
        # 聊天信息：002 username message
        # 注册消息：004 username password
        # 按照类型解析
        request_data={}
        request_data['request_id'] = recv_data['request_id']

        if request_data['request_id'] == REQUEST_LOGIN:
            # 用户请求登录
            request_data['username'] = recv_data['username']
            request_data['password'] = recv_data['password']

        elif request_data['request_id'] == REQUEST_CHAT:
            # 用户发来聊天信息
            request_data['username'] = recv_data['username']
            request_data['message'] = recv_data['message']
        elif request_data['request_id'] == REQUEST_REGISTER:
            # 用户请求注册
            request_data['username'] = recv_data['username']
            request_data['password'] = recv_data['password']
            request_data['nickname'] = recv_data['nickname']

        return request_data

    def request_chat_handle(self, client_sock, request_data):
        """聊天请求处理"""
        print("收到收到收到", request_data)
        # 获取消息内容
        username = request_data['username']
        message = request_data['message']
        nickname = self.clients[username]['nickname']
        # 拼接发送给客户端的消息文本
        response = ResponseProtocol.response_chat(nickname, message)
        # 转发消息给在线用户
        for u_name, info in self.clients.items():
            # 不需要向发送信息的账号转发数据
            if username == u_name:
                continue
            info['sock'].send_data(response)

    def request_login_handle(self, client_sock, request_data):
        """登录请求处理"""
        # 登录用户名和密码
        username = request_data['username']
        password = request_data['password']

        # 查询用户名是否合法
        ret, nickname, username = self.check_user_login(username, password)
        # 如果登录成功，则保存用户连接套接字
        if ret == '1':
            self.clients[username] = {'sock': client_sock, 'nickname': nickname}
            self.send_user_list()
        # 组装响应结果
        response = ResponseProtocol.response_login(ret, nickname, username)
        # 发送响应结果
        client_sock.send_data(response)

    def request_register_handle(self, client_sock, request_data):
        """处理注册功能"""
        print("收到注册请求，准备处理")

        # 登录用户名和密码
        username = request_data['username']
        password = request_data['password']
        nickname = request_data['nickname']

        # 查询用户是否存在
        ret, nickname, username = self.check_user_register(username, password, nickname)
        # 组装响应结果
        response = ResponseProtocol.response_register(ret, username, nickname)
        # 发送响应结果
        client_sock.send_data(response)

    def check_user_login(self, username, password):
        """检查用户是否登录成功，并返回结果（0/失败，1/成功），昵称，用户账号"""
        # 查询用户信息
        sql = "select * from users where user_name='%s'" % username
        result = self.db.get_one(sql)
        # 没有查询结果，用户不存在，登陆失败
        if not result:
            return '0', '', ''
        # 密码不匹配
        if password != result['user_password']:
            return '0', '', username

        # 否则登录成功
        return '1', result['user_nickname'], username

    def check_user_register(self, username, password, nickname):
        """检查注册用户名是否存在，不存在就插入，并返回结果（0/失败，1/成功）"""
        # 查询用户信息
        sql = "select * from users where user_name='%s'" % username
        result = self.db.get_one(sql)
        # 有查询结果，用户存在，注册失败
        if result:
            return '0', '', ''

        # 查询没结果，进行注册
        sql = "insert into users(user_name, user_password, user_nickname) values('%s','%s','%s')" % (username, password, nickname)
        self.db.insert_one(sql)
        return '1', 'username', 'nickname'

    def send_user_list(self):
        """发送在线用户列表给客户端"""
        user_list = []
        for u_name, info in self.clients.items():
            user_list.append(info['nickname'])
        response = ResponseProtocol.response_user_list(user_list)
        for u_name, info in self.clients.items():
            info['sock'].send_data(response)


if __name__ == '__main__':
    Server().startup()