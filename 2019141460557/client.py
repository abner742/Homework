import configparser
import os
import json
import socket
import threading
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText

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

userName = ''
password = ''

# 登录窗口
loginWindow = tkinter.Tk()
loginWindow.geometry("500x350")
loginWindow.title('欢迎来到聊天室')
loginWindow.resizable(0, 0)

V_name = tkinter.StringVar()
V_pass = tkinter.StringVar()
V_serverName = tkinter.StringVar()
V_serverName.set('127.0.0.1:8888')

# 登录图片
canvas = tkinter.Canvas(loginWindow, height=350, width=500)
filename = tkinter.PhotoImage(file='sea.gif')
image = canvas.create_image(0, 0, anchor='nw', image=filename)
canvas.pack(side='top')


# 输入框
labelIP = tkinter.Label(loginWindow, text='目标主机')
labelIP.place(x=60, y=40, width=100, height=30)
entryIP = tkinter.Entry(loginWindow, width=60, textvariable=V_serverName)
entryIP.place(x=200, y=40, width=100, height=30)

labelUSER = tkinter.Label(loginWindow, text='用户名')
labelUSER.place(x=60, y=100, width=100, height=30)
entryUSER = tkinter.Entry(loginWindow, width=60, textvariable=V_name)
entryUSER.place(x=200, y=100, width=100, height=30)

labelUSER = tkinter.Label(loginWindow, text='密码')
labelUSER.place(x=60, y=160, width=100, height=30)
entryUSER = tkinter.Entry(loginWindow, width=60, textvariable=V_pass)
entryUSER.place(x=200, y=160, width=100, height=30)

# 登录
def login(*args):
    global userName
    global password
    global server_name
    userName = V_name.get()
    password = V_pass.get()
    server_name = V_serverName.get()

    # 发送访问请求,验证用户信息
    s.send(userName.encode() + '~'.encode() + password.encode())

    loginResult = s.recv(1024).decode()
    print(loginResult)
    if loginResult == '用户名不存在':
        flag = tkinter.messagebox.askyesno(title='注册', message='该用户不存在,是否需要注册？')
        if flag:
            SignUp()
    elif loginResult == '密码错误':
        tkinter.messagebox.showerror(title='错误！', message='密码错误,请重新输入！')
    # 登陆成功，进入聊天界面
    else:
        loginWindow.destroy()


# 注册
def SignUp():
    def SignUpNew():
        newname = N_name.get()
        newpass = N_pass.get()
        # 确认密码
        passconfirm = N_com.get()

        if newpass != passconfirm:
            tkinter.messagebox.showerror(title='错误！', message='确认密码不一致，请重新输入！')
        else:
            # 让server判断出是注册请求
            register = 'signup~' + newname + '~' + newpass
            s.send(register.encode())
            data = s.recv(1024).decode()
            if data == '注册成功':
                tkinter.messagebox.showinfo(title='恭喜', message='注册成功！')
                SignWindow.destroy()
            if data == '用户已注册':
                tkinter.messagebox.showerror(title='错误', message="用户已注册")

    # 注册窗口
    SignWindow = tkinter.Toplevel(loginWindow)
    SignWindow.geometry('350x200')
    SignWindow.title('注册窗口')
    # 输入框
    N_name = tkinter.StringVar()
    tkinter.Label(SignWindow, text='用户名').place(x=10, y=10)
    entry_new_name = tkinter.Entry(SignWindow, textvariable=N_name)
    entry_new_name.place(x=150, y=10)

    N_pass = tkinter.StringVar()
    tkinter.Label(SignWindow, text='密码').place(x=10, y=50)
    entry_usr_pwd = tkinter.Entry(SignWindow, textvariable=N_pass, show='*')
    entry_usr_pwd.place(x=150, y=50)

    N_com = tkinter.StringVar()
    tkinter.Label(SignWindow, text='确认密码').place(x=10, y=90)
    entry_usr_pwd_confirm = tkinter.Entry(SignWindow, textvariable=N_com, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)
    #按钮
    signButton = tkinter.Button(SignWindow, text='提交', command=SignUpNew)
    signButton.place(x=150, y=130)


# 登陆界面的按钮
loginButton = tkinter.Button(loginWindow, text='登录', command=login, bg='Yellow')
loginButton.place(x=200, y=250,width=40, height=25)
loginWindow.bind('<Return>', login)
signBn = tkinter.Button(loginWindow, text='注册', command=SignUp,bg='Yellow')
signBn.place(x=300, y=250,width=40, height=25)

# 建立连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((IP, int(PORT)))

loginWindow.mainloop()

# 聊天室：聊天窗口
ChatWindow = tkinter.Tk()
ChatWindow.geometry("640x410")
ChatWindow.title('聊天室')
ChatWindow.resizable(0, 0)

# 聊天界面
chatarea = ScrolledText(ChatWindow)
chatarea.place(x=5, y=0, width=640, height=320)
chatarea.tag_config('tips', foreground='blue', backgroun="yellow")

chatarea.insert(tkinter.END, '欢迎进入群聊，大家开始聊天吧!\n', 'tips')
chatarea.insert(tkinter.END, '若想私聊，请按照‘聊天内容~你的名字~ta的名字’格式输入', 'tips')

INPUT = tkinter.StringVar()
INPUT.set('')
entryIuput = tkinter.Entry(ChatWindow, width=120, textvariable=INPUT)
entryIuput.place(x=5, y=320, width=580, height=80)

# 在线用户列表
listbox1 = tkinter.Listbox(ChatWindow)
listbox1.place(x=510, y=0, width=130, height=320)


def send(*args):
    message = entryIuput.get() + '~' + userName + '~' + '群聊'
    s.send(message.encode())
    INPUT.set('')


sendButton = tkinter.Button(ChatWindow, text="\n发送", anchor='n', command=send, font=('Helvetica', 18), bg='white')
sendButton.place(x=510, y=320, width=130, height=80)
ChatWindow.bind('<Return>', send)

def receive():
    global uses
    while True:
        data = s.recv(1024)
        data = data.decode()
        print(data)
        try:
            uses = json.loads(data)
            listbox1.delete(0, tkinter.END)
            listbox1.insert(tkinter.END, "当前在线用户")
            listbox1.insert(tkinter.END, "------Group chat-------")
            for x in range(len(uses)):
                listbox1.insert(tkinter.END, uses[x])
        except:
            data = data.split('~')
            # 发送的消息
            message = data[0]
            # 该用户的名字
            myName = data[1]
            # 该用户想要私聊的人的名字
            chatwith = data[2]
            message = '\n' + message
            # 群聊
            if chatwith == '群聊':
                if myName == userName:
                    chatarea.insert(tkinter.END, message)
                else:
                    chatarea.insert(tkinter.END, message)
            # 私聊
            elif myName == userName or chatwith == userName:
                if myName == userName:
                    chatarea.tag_config('tag2', foreground='red')
                    chatarea.insert(tkinter.END, message, 'tag2')
                else:
                    chatarea.tag_config('tag3', foreground='green')
                    chatarea.insert(tkinter.END, message, 'tag3')

            chatarea.see(tkinter.END)


r = threading.Thread(target=receive)
r.start()  # 开始线程接收信息
ChatWindow.mainloop()
s.close()
