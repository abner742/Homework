# server.py
# 服务端代码
import os
from time import ctime
from multiprocessing import Process, Queue
from select import select
from socket import *
from settings import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from server import main


def main_gui():
    # 主窗口
    root = Tk()

    # 设置窗口居中
    center(root)

    # 设置窗口其他属性
    root.title("多人聊天室主窗口")
    root.resizable(0, 0)
    root.configure(bg="white")
    # root.iconbitmap("python.ico")

    # 添加主机名（HOST）以及端口号（PORT）等输入框
    pad = 10
    Label(root, text="主机名（Host）：").grid(row=0, column=0, padx=pad, pady=pad)
    ent_host = Entry(root)
    ent_host.insert(0, HOST)
    ent_host.grid(row=0, column=1, padx=pad, pady=pad)
    Label(root, text="端口号（Port）：").grid(row=1, column=0, padx=pad, pady=pad)
    ent_port = Entry(root)
    ent_port.insert(0, PORT)
    ent_port.grid(row=1, column=1, padx=pad, pady=pad)

    # 组件列表
    widgets = {
        "ent_host": ent_host,
        "ent_port": ent_port
    }

    # 添加确认按钮
    btn_cfm = Button(root, text="新建网络聊天室", command=lambda: validate(root, widgets))
    btn_cfm.grid(rowspan=2, columnspan=2, padx=pad, pady=pad)

    # 绑定事件
    root.bind("<Return>", lambda event: validate(root, widgets))

    # 主循环事件
    root.mainloop()


def validate(root, widgets):
    # 确认按钮事件，检查是否输入有误
    host, port = widgets["ent_host"].get(), widgets["ent_port"].get()

    # 如果端口号不是纯数字
    try:
        port = int(port)
    except:
        messagebox.showerror("错误", "端口号必须为数字！")
        return

        # 弹出错误窗口
    if not host or not port:
        messagebox.showerror("错误", "主机名或端口不可为空！")
        return

    # 有效地址
    addr = (host, port)

    # 检查是否套接字成功
    try:
        # print(host, port)
        command = "start python server.py " + host + " " + str(port)
        print(command)
        os.system(command)
        command = "start python client.py "
        print(command)
        os.system(command)
        print("成功了！！！")
        messagebox.showinfo(title='成功了', message='成功了！！！请继续在黑框里按照提示操作')
        # messagebox.showerror("成功了！！！", "成功了！！！请继续在黑框里按照提示操作")
        # main(host, port)
        # server = socket(AF_INET, SOCK_STREAM)
        # server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # server.bind(addr)
        # server.listen(10)
    except Exception as e:
        messagebox.showerror("错误", f"无法在{addr}上生成套接字！")
        print(e)
        root.destroy()
        return
    else:
        root.destroy()
        return


if __name__ == "__main__":
    main_gui()
