import configparser
import os
import socket
import threading
import json
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText


curPath = os.path.dirname(os.path.realpath(__file__))
cfgPath = os.path.join(curPath, "config.ini")
conf = configparser.ConfigParser()
conf.read(cfgPath, encoding="utf-8")

# ip = conf.get("test1", "local_IP")
# port =int(conf.get("test1", "port1"))

IP = ''
PORT = ''
user = ''
listbox1 = ''  # 用于显示在线用户的列表框
ii = 0  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = '------Group chat-------'  # 聊天对象, 默认为群聊

# 登陆窗口
root1 = tkinter.Tk()
root1.title('Log in')
root1['height'] = 110
root1['width'] = 270
root1.resizable(0, 0)  # 限制窗口大小

testIp = conf.get("test1", "local_IP") + ":" + conf.get("test1", "port1")
print(testIp)

IP1 = tkinter.StringVar()
IP1.set(testIp)         # 默认显示的ip和端口
# IP1.set('127.0.0.1:50007')  # 默认显示的ip和端口
User = tkinter.StringVar()
User.set('')

# 服务器标签
labelIP = tkinter.Label(root1, text='服务器地址')
labelIP.place(x=20, y=10, width=100, height=20)

entryIP = tkinter.Entry(root1, width=80, textvariable=IP1)
entryIP.place(x=120, y=10, width=130, height=20)

# 用户名标签
labelUser = tkinter.Label(root1, text='用户名')
labelUser.place(x=30, y=40, width=80, height=20)

entryUser = tkinter.Entry(root1, width=80, textvariable=User)
entryUser.place(x=120, y=40, width=130, height=20)


# 登录
def login(*args):
    global IP, PORT, user
    IP, PORT = entryIP.get().split(':')  # 获取IP和端口号
    PORT = int(PORT)  # 端口号转换为int类型
    user = entryUser.get()
    if not user:
        tkinter.messagebox.showerror('用户名错误', message='用户名不能为空')
    else:
        root1.destroy()  # 关闭窗口


# 回车键绑定登录函数
root1.bind('<Return>', login)
but = tkinter.Button(root1, text='登录', command=login)
but.place(x=100, y=70, width=70, height=30)

root1.mainloop()

# 连接服务器
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

if user:
    s.send(user.encode())  # 发送用户名
else:
    s.send('no'.encode())  # 没有输入用户名则标记no

# 如果没有用户名则将ip和端口号设置为用户名
addr = s.getsockname()  # 获取客户端ip和端口号
addr = addr[0] + ':' + str(addr[1])
if user == '':
    user = addr

# 聊天窗口
# 创建图形界面
root = tkinter.Tk()
root.title(user)  # 窗口命名为用户名
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)  # 限制窗口大小

# 创建多行文本框
listbox = ScrolledText(root)
listbox.place(x=5, y=0, width=570, height=320)
# 文本框使用的字体颜色
listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')
listbox.insert(tkinter.END, '欢迎进入小乌龟聊天室!', 'blue')

# 表情功能代码部分
# 四个按钮, 使用全局变量, 方便创建和销毁
b1 = ''
b2 = ''
b3 = ''
b4 = ''
# 将表情图片打开存入变量中
p1 = tkinter.PhotoImage(file='./emoji/facepalm.png')
p2 = tkinter.PhotoImage(file='./emoji/smirk.png')
p3 = tkinter.PhotoImage(file='./emoji/concerned.png')
p4 = tkinter.PhotoImage(file='./emoji/smart.png')

# 用字典将标记与表情图片一一对应, 用于后面接收标记判断表情
dic = {'aa**': p1, 'bb**': p2, 'cc**': p3, 'dd**': p4}
ee = 0  # 判断表情面板开关的标志


# 发送表情标记的函数, 在按钮点击事件中调用
# 参数是发的表情图标记, 发送后将按钮销毁
def mark(exp):
    global ee
    mes = exp + ':;' + user + ':;' + chat
    s.send(mes.encode())
    b1.destroy()
    b2.destroy()
    b3.destroy()
    b4.destroy()
    ee = 0


# 四个对应的函数
def bb1():
    mark('aa**')


def bb2():
    mark('bb**')


def bb3():
    mark('cc**')


def bb4():
    mark('dd**')


def express():
    global b1, b2, b3, b4, ee
    if ee == 0:
        ee = 1
        b1 = tkinter.Button(root, command=bb1, image=p1,
                            relief=tkinter.FLAT, bd=0)
        b2 = tkinter.Button(root, command=bb2, image=p2,
                            relief=tkinter.FLAT, bd=0)
        b3 = tkinter.Button(root, command=bb3, image=p3,
                            relief=tkinter.FLAT, bd=0)
        b4 = tkinter.Button(root, command=bb4, image=p4,
                            relief=tkinter.FLAT, bd=0)

        b1.place(x=5, y=248)
        b2.place(x=75, y=248)
        b3.place(x=145, y=248)
        b4.place(x=215, y=248)
    else:
        ee = 0
        b1.destroy()
        b2.destroy()
        b3.destroy()
        b4.destroy()


# 创建表情选项按钮
eBut = tkinter.Button(root, text='表情', command=express)
eBut.place(x=5, y=320, width=60, height=30)

# 创建多行文本框, 显示在线用户
listbox1 = tkinter.Listbox(root)
listbox1.place(x=445, y=0, width=130, height=320)


def users():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=445, y=0, width=130, height=320)
        ii = 0
    else:
        listbox1.place_forget()  # 隐藏控件
        ii = 1


# 查看在线用户按钮
button1 = tkinter.Button(root, text='在线用户', command=users)
button1.place(x=485, y=320, width=90, height=30)

# 创建输入文本框和关联变量
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=350, width=570, height=40)


def send(*args):
    # 没有添加的话发送信息时会提示没有聊天对象
    users.append('------Group chat-------')
    print(chat)

    # 如果选择的聊天对象不在users中
    if chat not in users:
        tkinter.messagebox.showerror('发送错误', message='不存在该用户!')
        return

    if chat == user:
        tkinter.messagebox.showerror('发送错误', message='不能和自己进行私聊!')
        return
    mes = entry.get() + ':;' + user + ':;' + chat  # 添加聊天对象标记
    s.send(mes.encode())
    a.set('')  # 发送后清空文本框


# 创建发送按钮
button = tkinter.Button(root, text='发送', command=send)
button.place(x=515, y=353, width=60, height=30)
root.bind('<Return>', send)  # 绑定回车发送信息


# 私聊功能
def private(*args):
    global chat
    # 获取点击的索引然后得到内容(用户名)
    indexs = listbox1.curselection()
    index = indexs[0]
    if index > 0:
        chat = listbox1.get(index)
        # 修改客户端名称
        if chat == '------Group chat-------':
            root.title(user)
            return
        ti = user + '  -->  ' + chat
        root.title(ti)


# 在显示用户列表框上设置绑定事件
listbox1.bind('<ButtonRelease-1>', private)


# 用于时刻接收服务端发送的信息并打印
def recv():
    global users
    while True:
        data = s.recv(1024)
        data = data.decode()
        # 没有捕获到异常则表示接收到的是在线用户列表
        try:
            data = json.loads(data)
            users = data
            # 清空列表框
            listbox1.delete(0, tkinter.END)
            number = ('   Users online: ' + str(len(data)))
            listbox1.insert(tkinter.END, number)
            listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
            listbox1.insert(tkinter.END, '------Group chat-------')
            listbox1.itemconfig(tkinter.END, fg='green')
            for i in range(len(data)):
                listbox1.insert(tkinter.END, (data[i]))
                listbox1.itemconfig(tkinter.END, fg='green')
        except:
            data = data.split(':;')
            data1 = data[0].strip()  # 消息
            data2 = data[1]  # 发送信息的用户名
            data3 = data[2]  # 聊天对象

            markk = data1.split('：')[1]
            # 判断是不是图片
            pic = markk.split('#')
            # 判断是不是表情
            # 如果该表情在表情字典中
            if (markk in dic) or pic[0] == '``':

                # 新增信息，换行后显示“名字：信息”
                data4 = '\n' + data2 + '：'
                if data3 == '------Group chat-------':
                    # 如果是自己则显示为蓝色字体
                    if data2 == user:
                        listbox.insert(tkinter.END, data4, 'blue')
                    # 是其他用户则显示为绿色字体
                    else:
                        # END将信息加在最后一行
                        listbox.insert(tkinter.END, data4, 'green')

                # 显示私聊对象名称
                elif data2 == user or data3 == user:
                    # 将私聊信息显示为红色字体
                    listbox.insert(tkinter.END, data4, 'red')  # END将信息加在最后一行

                if pic[0] != '``':
                    # 将表情图贴到聊天框
                    listbox.image_create(tkinter.END, image=dic[markk])

            # 如果不在
            else:
                data1 = '\n' + data1
                if data3 == '------Group chat-------':
                    if data2 == user:
                        listbox.insert(tkinter.END, data1, 'blue')
                    else:
                        listbox.insert(tkinter.END, data1, 'green')  # END将信息加在最后一行
                    if len(data) == 4:
                        listbox.insert(tkinter.END, '\n' + data[3], 'pink')
                # 显示私聊
                elif data2 == user or data3 == user:
                    listbox.insert(tkinter.END, data1, 'red')  # END将信息加在最后一行
            listbox.see(tkinter.END)  # 显示在最后


r = threading.Thread(target=recv)
r.start()  # 开始线程接收信息

root.mainloop()
s.close()  # 关闭图形界面后关闭TCP连接
