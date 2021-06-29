import socket
import time

from query import query_broadcast
import tkinter as tk
from tkinter import messagebox
from listen import listen_ack
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
from load import *
import os


class Application1(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self.pack()
        self.envar = tk.StringVar(None, '123')
        root.geometry('500x500')
        root.title('欢迎')

        self.initWindow()

    def buttonShare(self):
        root = tk.Tk()
        app = ApplicationShare(root=root)
        app.mainloop()

    def buttonDownLoad(self):
        root = tk.Tk()
        app = ApplicationDownLoad(root=root)
        app.mainloop()

    def buttonWatch(self):
        root = tk.Tk()
        app = ApplicationWatch(root=root)
        app.mainloop()

    def initWindow(self):
        # #标签
        # tk.Label(self,text='11111',fg='red',bg='green',width=10).grid(row=1,column=1)
        # #输入框
        # tk.Entry(self,textvariable=self.envar,width=100).grid(row=1,column=2)
        # #文本框
        # text=tk.Text(self,fg='#ff0',bg='#255',width=10)
        # text.grid(columnspan=2,rowspan=2,pady=10,padx=50,ipadx=50)
        # text.insert('end','*在尾部加入*')
        # text.insert('3.1','0—>2')
        # #按钮
        # tk.Button(self,text='登录').grid()
        tk.Button(self, text='分享', command=self.buttonShare).grid(row=1, column=1, pady=10)
        tk.Button(self, text='下载', command=self.buttonDownLoad).grid(row=1, column=2, padx=50)
        tk.Button(self, text='分享管理', command=self.buttonWatch).grid(row=1, column=3)


class ApplicationShare(tk.Frame):  # 分享
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self.pack()
        # self.envar=tk.StringVar(None,'123')
        root.geometry('500x500')
        root.title('分享')

        self.initWindow()

    def getSourceLocation(self, text):
        text = text.get("1.0", "end")
        # print(text)
        path = text.replace('\n', '').replace('\r', '')
        path = path.replace('\\', '/')  # 将反斜杠转换为斜杠 否则os.path.exists()函数不认识
        url = geturl()
        if os.path.exists(path):
            if path in url:
                messagebox.showinfo("提示：", "资源已在分享列表中")
            else:
                url.append(path)
                try:
                    f = open('url.txt', 'a')
                    f.write('\n')
                    f.write(path)
                    f.close()
                    messagebox.showinfo("提示：", "加入成功")
                except:
                    messagebox.showinfo("提示：", "加入失败")
        else:
            messagebox.showinfo("提示：", "文件不存在，请确认后输入")

    def initWindow(self):
        # #标签
        # tk.Label(self,text='11111',fg='red',bg='green',width=10).grid(row=1,column=1)
        # #输入框
        # tk.Entry(self,textvariable=self.envar,width=100).grid(row=1,column=2)
        # #文本框
        # text=tk.Text(self,fg='#ff0',bg='#255',width=10)
        # text.grid(columnspan=2,rowspan=2,pady=10,padx=50,ipadx=50)
        # text.insert('end','*在尾部加入*')
        # text.insert('3.1','0—>2')
        # #按钮
        # tk.Button(self,text='登录').grid()
        tk.Label(self, text='请在下方输入文件绝对路径').grid()
        text = tk.Text(self, height=10, width=70)
        text.grid()
        # 因为在图形编程里实在不好加逻辑，只能把判断放在函数里
        tk.Button(self, text='确定', command=lambda: self.getSourceLocation(text)).grid()


class ApplicationDownLoad(tk.Frame):  # 下载
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self.pack()
        root.geometry('500x500')
        root.title('下载')

        self.initWindow()

    def initWindow(self):
        tk.Label(self, text='请在下方输入文件关键字').grid()
        text = tk.Text(self, height=10, width=70)
        text.grid()
        # 因为在图形编程里实在不好加逻辑，只能把判断放在函数里
        tk.Button(self, text='搜索', command=lambda: [query_broadcast(text), listen_ack()]).grid()


class ApplicationWatch(tk.Frame):  # 分享管理
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self.pack()
        root.geometry('500x500')
        root.title('分享管理')

        self.initWindow()

    def initWindow(self):
        url = geturl()

        # print(url)
        def myopen(event,filepath):
            # print(filepath)
            dirpath = filepath[0:-len(filepath.split('/')[-1])]
            dirpath = dirpath.replace('/', '\\')
            dirpath = 'start explorer ' + dirpath
            os.system(dirpath)

        def mydetele(event,filepath):
            if deteleurl(filepath):
                messagebox.showinfo("提示",'删除成功')
                self.destroy()
                win=tk.Tk()
                win=ApplicationWatch(root=win)
                win.mainloop()


        def handler(event, a, b, c):
            '''事件处理函数'''
            print(event)
            print("handler", a, b, c)

        def handlerAdaptor(fun, **kwds):
            '''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

        def viod():
            pass

        for url_one in url:
            frame = tk.Frame(self)
            text = tk.Text(frame, height=1, width=50, wrap=tk.NONE)
            text.insert('1.0', url_one)
            text.config(state='disabled')
            text.grid(row=1, column=0)
            tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text.xview).grid(row=2, column=0, sticky=tk.EW)
            b1=tk.Button(frame, text='打开所在文件夹',command=viod)
            b1.bind("<Button-1>", handlerAdaptor(myopen, filepath=url_one))
            b1.grid(row=1, column=1)
            b2=tk.Button(frame, text='删除',command=viod)
            b2.bind("<Button-1>", handlerAdaptor(mydetele, filepath=url_one))
            b2.grid(row=1, column=2)
            frame.pack()

        # for url1 in url:
        #     print(type(url1))
        #     buttons[url1].bind("<Button-1>", handlerAdaptor(myopen, filepath=url1))


def client():
    root = tk.Tk()
    app = Application1(root=root)
    app.mainloop()
