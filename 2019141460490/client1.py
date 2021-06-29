
import json
import pickle
import socket
import threading
import tkinter as tk
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import config

target_IP = config.target_IP
port  = config.PORT

usr_name = ''
usr_pwd = ''
server_name = ''


def usr_login(*args):
    global usr_name
    global usr_pwd
    global server_name
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    server_name = var_server_name.get()

    # 发送访问请求,验证用户信息
    s.send(usr_name.encode() + '~'.encode() + usr_pwd.encode())

    comfirm = s.recv(1024).decode()
    print(comfirm)
    if (comfirm == '用户名不存在'):
        usr_sign_up = tk.messagebox.askyesno(title='注册', message='欢迎！不过你还没有注册哦，需要注册吗？')
        if usr_sign_up:
            _usr_sign_up()
    elif (comfirm == '密码错误'):
        tk.messagebox.showerror('密码错误,请重新输入！')

    else:
        window.destroy()


#     进入聊天室


def _usr_sign_up():
    def sign_to_chatroom():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()

        if np != npf:
            tk.messagebox.showerror(title='错误！', message='确认密码不一致，请重新输入！')
        else:
            register = 'reg~' + nn + '~' + np
            s.send(register.encode())
            data = s.recv(1024).decode()
            if (data == '注册成功！'):
                tk.messagebox.showinfo(title='恭喜', message='注册成功！')
                window_sign_up.destroy()
            if (data == '用户已经注册'):
                tk.messagebox.showerror(title='错误！', message="用户已经注册")

    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('注册窗口')

    new_name = tk.StringVar()
    new_name.set('张三')
    tk.Label(window_sign_up, text='用户名').place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='密码').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='确认密码').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='注册', command=sign_to_chatroom)
    btn_comfirm_sign_up.place(x=150, y=130)


window = tk.Tk()
window.title('Welcome to my chatroom')
window.geometry('450x300')
window.resizable(0, 0)
var_usr_name = tk.StringVar();
var_usr_pwd = tk.StringVar();
var_server_name = tk.StringVar();
var_server_name.set(target_IP+':'+port)
# var_usr_name.set('xy')
# var_usr_pwd.set('123')
# 登录界面:欢迎图片
canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='welcome.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# 用户信息
tk.Label(window, text='目标主机').place(x=50, y=130)
tk.Label(window, text='用户名:').place(x=50, y=170)
tk.Label(window, text='密码:').place(x=50, y=210)

# 输入框
entry_server_name = tk.Entry(window, textvariable=var_server_name)
entry_server_name.place(x=160, y=130)

entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=170)

entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=210)

btn_login = tk.Button(window, text='登录', command=usr_login)
btn_login.place(x=170, y=250)
window.bind('<Return>', usr_login)
btn_sign_up = tk.Button(window, text='注册', command=_usr_sign_up)
btn_sign_up.place(x=270, y=250)
# 建立连接
server_name = var_server_name.get()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip, server_port = server_name.split(':')
s.connect((server_ip, int(server_port)))

window.mainloop()

# 聊天室：聊天窗口
Chatroom = tkinter.Tk()
Chatroom.geometry("640x480")
Chatroom.title('聊天室')
Chatroom.resizable(0, 0)

# 消息界面
listbox = ScrolledText(Chatroom)
listbox.place(x=5, y=0, width=640, height=320)
listbox.tag_config('tag1', foreground='red', backgroun="yellow")
listbox.insert(tkinter.END, '欢迎进入群聊，大家开始聊天吧!', 'tag1')

INPUT = tkinter.StringVar()
INPUT.set('')
entryIuput = tkinter.Entry(Chatroom, width=120, textvariable=INPUT)
entryIuput.place(x=5, y=320, width=580, height=170)

# 在线用户列表
listbox1 = tkinter.Listbox(Chatroom)
listbox1.place(x=510, y=0, width=130, height=320)


def send(*args):
    message = entryIuput.get() + '~' + usr_name + '~'
    s.send(message.encode())
    INPUT.set('')


sendButton = tkinter.Button(Chatroom, text="\n发\n\n\n送", anchor='n', command=send, font=('Helvetica', 18), bg='white')
sendButton.place(x=585, y=320, width=55, height=300)
Chatroom.bind('<Return>', send)


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
        # users.append('------Group chat-------')
        except:
            data = data.split('~')
            message = data[0]
            userName = data[1]
            message = '\n' + message

            listbox.insert(tkinter.END, message)

            # listbox.tag_config('tag2', foreground='red')
            # listbox.insert(tkinter.END, message, 'tag2')
            #
            # listbox.tag_config('tag3', foreground='green')
            # listbox.insert(tkinter.END, message, 'tag3')

            listbox.see(tkinter.END)


r = threading.Thread(target=receive)
r.start()  # 开始线程接收信息
Chatroom.mainloop()









