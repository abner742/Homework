from LoginPanel import LoginPanel
from MainPanel import MainPanel
from RegisterPanel import RegisterPanel

from tkinter import messagebox
from threading import Thread
import time
import re
import math
import socket
import configparser


class ChatClient:

    def __init__(self):
        cf=configparser.ConfigParser()
        cf.read("userdata\\config.ini")
        secs=cf.sections()
        opts=cf.options("sec_a")
        items=cf.items("sec_a")
        val=cf.get("sec_a","server_ip")

        self.sk = socket.socket()
        self.sk.connect((val, 8080))
        #self.sk.connect(('10.132.3.123', 8080))

    # 验证登录
    def check_user(self, user, key):
        # 请求类型
        self.sk.sendall(bytes("1", "utf-8"))
        # 依次发送用户名密码
        self.send_string_with_length(user)
        self.send_string_with_length(key)
        # 获取服务器的返回值，"1"代表通过，“0”代表不通过
        check_result = self.recv_string_by_length(1)
        return check_result == "1"

    # 注册
    def register_user(self, user, key):
        # 请求类型
        self.sk.sendall(bytes("2", "utf-8"))
        # 依次发送用户名密码
        self.send_string_with_length(user)
        self.send_string_with_length(key)
        # 获取服务器的返回值，"0"代表通过，“1”代表已有用户名, "2"代表其他错误
        return self.recv_string_by_length(1)

    # 发送消息
    def send_message(self, message):
        self.sk.sendall(bytes("3", "utf-8"))
        self.send_string_with_length(message)
    
    #发送私聊
    def send_private(self,message):
        self.sk.sendall(bytes("5", "utf-8"))
        self.send_string_with_length(message)

    # 发送带长度的字符串
    def send_string_with_length(self, content):
        # 发送内容的长度
        self.sk.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
        # 发送内容
        self.sk.sendall(bytes(content, encoding='utf-8'))

    # 获取服务器传来的定长字符串
    def recv_string_by_length(self, len):
        return str(self.sk.recv(len), "utf-8")

    # 获取服务端传来的变长字符串，这种情况下服务器会先传一个长度值
    def recv_all_string(self):
        # 获取消息长度
        length = int.from_bytes(self.sk.recv(4), byteorder='big')
        b_size = 3 * 1024  # utf8编码中汉字占3字节，英文占1字节
        times = math.ceil(length / b_size)
        content = ''
        for i in range(times):
            if i == times - 1:
                seg_b = self.sk.recv(length % b_size)
            else:
                seg_b = self.sk.recv(b_size)
            content += str(seg_b, encoding='utf-8')
        return content

    def send_number(self, number):
        self.sk.sendall(int(number).to_bytes(4, byteorder='big'))

    def recv_number(self):
        return int.from_bytes(self.sk.recv(4), byteorder='big')


def send_message():
    print("send message:")
    content = main_frame.get_send_text()
    if content == "" or content == "\n":
        print("empty message")
        return
    print(content)
    # 清空输入框
    main_frame.clear_send_text()
    flag="#!"
    if(flag in content):
        client.send_private(content)
    else:
        client.send_message(content)


# def close_sk():
#     client.sk.close()

def close_main_window():
    client.sk.close()
    main_frame.main_frame.destroy()


def close_login_window():
    client.sk.close()
    login_frame.login_frame.destroy()


# 关闭注册界面并打开登陆界面
def close_reg_window():
    reg_frame.close()
    login_frame.show()


# 关闭登陆界面前往主界面
def goto_main_frame(user):
    login_frame.close()
    global main_frame
    main_frame = MainPanel(user, send_message, close_main_window)
    # 新开一个线程专门负责接收并处理数据
    Thread(target=recv_data).start()
    main_frame.show()


def login():
    user, key = login_frame.get_input()
   
    if user == "" or key == "":
        messagebox.showwarning(title="提示", message="用户名或者密码为空")
        return
    print("user: " + user + ", key: " + key)
    if client.check_user(user, key):
        # 验证成功
        goto_main_frame(user)
    else:
        # 验证失败
        messagebox.showerror(title="错误", message="用户名或者密码错误")


# 登陆界面前往注册界面
def register():
    login_frame.close()
    global reg_frame
    reg_frame = RegisterPanel(close_reg_window, register_submit, close_reg_window)
    reg_frame.show()


# 提交注册表单
def register_submit():
    user, key, confirm = reg_frame.get_input()
    if user == "" or key == "" or confirm == "":
        messagebox.showwarning("错误", "请完成注册表单")
        return
    if not key == confirm:
        messagebox.showwarning("错误", "两次密码输入不一致")
        return
    contain_en=bool(re.search('[a-z]',key))
    if(not contain_en):
        messagebox.showwarning("错误", "密码必须包含英文")
        return

    # 发送注册请求
    result = client.register_user(user, key)
    if result == "0":
        # 注册成功，跳往登陆界面
        messagebox.showinfo("成功", "注册成功")
        close_reg_window()
    elif result == "1":
        # 用户名重复
        messagebox.showerror("错误", "该用户名已被注册")
    elif result == "2":
        # 未知错误
        messagebox.showerror("错误", "发生未知错误")


# 处理消息接收的线程方法
def recv_data():
    # 暂停几秒，等主界面渲染完毕
    time.sleep(1)
    while True:
        try:
            # 首先获取数据类型
            message_type = client.recv_all_string()
            print("recv type: " + message_type)
            if message_type == "#!onlinelist#!":
                #获取在线列表数据
                online_list = list()
                for n in range(client.recv_number()):
                    online_list.append(client.recv_all_string())
                main_frame.refresh_friends(online_list)
                print(online_list)
            elif message_type == "#!message#!":
                #获取新消息
                user = client.recv_all_string()
                print("user: " + user)
                content = client.recv_all_string()
                print("message: " + content)
                main_frame.recv_message(user, content)
        except Exception as e:
            print("server error occurred:" + str(e))
            break


def start():
    global client
    client = ChatClient()
    global login_frame
    login_frame = LoginPanel(login, register, close_login_window)
    global main_frame
    global reg_frame
    
    login_frame.show()


if __name__ == "__main__":
    start()