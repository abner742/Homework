from window_login import WindowLogin
from request_protocol import RequestProtocol
from client_socket import ClientSocket
from threading import Thread
from config import *
from tkinter.messagebox import showinfo
from window_chat import WindowChat
from window_register import WindowRegister
import sys


class Client(object):

    def __init__(self):
        """初始化客户端资源"""
        # 初始化登录窗口
        self.window = WindowLogin()
        self.window.on_reset_button_click(self.clear_inputs)
        self.window.on_login_button_click(self.send_login_data)
        self.window.on_register_button_click(self.register_to)
        self.window.on_window_closed(self.exit)

        # 初始化注册窗口
        self.window_register = WindowRegister()
        self.window_register.withdraw()  # 隐藏窗口
        self.window_register.on_yes_button_click(self.send_register_data)
        self.window_register.on_no_button_click(self.register_cancel)
        self.window_register.on_window_closed(self.exit)

        # 初始化聊天窗口
        self.window_chat = WindowChat()
        self.window_chat.withdraw()  # 隐藏窗口
        self.window_chat.on_send_button_click(self.send_chat_data)
        self.window_chat.on_window_closed(self.exit)

        # 创建客户端套接字
        self.conn = ClientSocket()

        # 初始化消息处理函数
        self.response_handle_function = {}
        self.register(RESPONSE_LOGIN, self.response_login_handle)
        self.register(RESPONSE_CHAT, self.response_chat_handle)
        self.register(RESPONSE_REGISTER, self.response_register_handle)
        self.register(RESPONSE_USER_LIST, self.refresh_user_list)

        # 在线用户名
        self.username = None

        # 程序正在运行的标记
        self.is_running = True

    def register(self, request_id, handle_function):
        """注册消息类型和处理函数到字典"""
        self.response_handle_function[request_id] = handle_function

    def startup(self):
        """开启窗口"""
        self.conn.connect()
        # 创建并开启一个子线程专门来接受消息
        Thread(target=self.response_handle).start()

        self.window.mainloop()

    def clear_inputs(self):
        """清空窗口内容"""
        self.window.clear_username()
        self.window.clear_password()

    def send_login_data(self):
        """发送登录消息到服务器"""
        # 获取到用户输入的账号密码
        username = self.window.get_username()
        password = self.window.get_password()

        # 生成协议文本
        request_text = RequestProtocol.request_login(username, password)

        # 发送协议文本到服务器
        self.conn.send_data(request_text)

    def register_to(self):
        """跳转到注册窗口"""
        # 显示注册窗口
        self.window_register.deiconify()

        # 清空输入框
        self.window.clear_username()
        self.window.clear_password()

        # 隐藏登录窗口
        self.window.withdraw()

    def send_register_data(self):
        """发送注册消息到服务器"""
        # 获取到用户输入的账号密码昵称
        username = self.window_register.get_username()
        password = self.window_register.get_password()
        nickname = self.window_register.get_nickname()

        # 生成协议文本
        request_text = RequestProtocol.request_register(username, password, nickname)

        # 发送协议文本到服务器
        self.conn.send_data(request_text)

    def register_cancel(self):
        """取消注册，返回登录窗口"""
        # 显示登录窗口
        self.window.deiconify()

        # 清空输入框
        self.window_register.clear_username()
        self.window_register.clear_password()
        self.window_register.clear_nickname()
        self.window_register.update()

        # 隐藏注册窗口
        self.window_register.withdraw()

    def send_chat_data(self):
        """获取输入框内容发送"""
        message = self.window_chat.get_input()
        self.window_chat.clear_input()

        # 拼接协议文本
        request_text = RequestProtocol.request_chat(self.username, message)

        # 发送消息内容
        self.conn.send_data(request_text)

        # 把消息内容显示到聊天区
        self.window_chat.append_message('我', message)

    def response_handle(self):
        """不断地接受服务器的新消息"""
        while self.is_running:
            # 获取服务器消息
            recv_data = self.conn.recv_data()

            # 解析消息内容
            response_data = self.parse_response_data(recv_data)

            # 根据消息内容分别进行处理
            handle_function = self.response_handle_function[response_data['response_id']]

            if handle_function:
                handle_function(response_data)

    @staticmethod
    def parse_response_data(recv_data):
        """
        登录的响应数据：101 成功/失败 昵称 账号
        聊天的响应数据：102 发送者昵称 消息内容
        用户列表的响应数据 103 在线用户列表
        注册的响应数据：104 成功/失败 用户名 昵称
        :param recv_data:
        :return:
        """
        # 解析消息的各个组成部分
        response_data = dict()
        response_data['response_id'] = recv_data['response_id']

        if response_data['response_id'] == RESPONSE_LOGIN:
            # 登录结果的响应
            response_data['result'] = recv_data['result']
            response_data['nickname'] = recv_data['nickname']
            response_data['username'] = recv_data['username']

        elif response_data['response_id'] == RESPONSE_CHAT:
            # 聊天信息的响应
            response_data['nickname'] = recv_data['nickname']
            response_data['message'] = recv_data['message']

        elif response_data['response_id'] == RESPONSE_USER_LIST:
            # 在线用户列表的响应
            response_data['user_list'] = recv_data['user_list']

        elif response_data['response_id'] == RESPONSE_REGISTER:
            # 注册结果的响应
            response_data['result'] = recv_data['result']
            response_data['username'] = recv_data['username']
            response_data['nickname'] = recv_data['nickname']

        return response_data

    def response_login_handle(self, response_data):
        """登录结果响应"""
        result = response_data['result']
        if result == '0':
            showinfo('提示', '账号或密码错误!')
            return

        showinfo('提示', '登录成功!')
        # 登陆成功获取用户信息
        nickname = response_data['nickname']
        # 保存登陆用户的账号，供发送消息使用
        self.username = response_data['username']

        # 显示聊天窗口
        self.window_chat.set_title(nickname)
        self.window_chat.update()
        self.window_chat.deiconify()

        # 隐藏登录窗口
        self.window.withdraw()

    def response_register_handle(self, response_data):
        """注册结果响应"""
        result = response_data['result']
        username = response_data['username']
        if result == '0':
            showinfo('提示', '用户名 %s 已存在。' % username)
            return
        showinfo('提示', '注册成功！')
        # 隐藏注册窗口
        self.window_register.withdraw()

        # 清空输入框
        self.window_register.clear_username()
        self.window_register.clear_password()
        self.window_register.clear_nickname()

        # 显示登录窗口
        self.window.deiconify()

    def response_chat_handle(self, response_data):
        """聊天消息响应"""
        sender = response_data['nickname']
        message = response_data['message']
        self.window_chat.append_message(sender, message)

    def exit(self):
        """退出程序"""
        self.is_running = False
        self.conn.close()
        # 退出程序
        sys.exit(0)

    def refresh_user_list(self, response_data):
        """更新用户列表"""
        self.window_chat.children['user_list'].delete(0, 'end')
        for item in response_data['user_list']:
            self.window_chat.children['user_list'].insert('end', item)


if __name__ == '__main__':
    client = Client()
    client.startup()