import socket
import time
import tkinter as tk
from tkinter import messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
import os
# str = input("请输入：")
# s=r"C:\Users\11435\Desktop"
# print(str)
# result = str.replace('\\','/')
# print(result)
# print(os.path.exists(result))

by = b'end'
print(type(by))
by = by.rstrip()
print(by)
by = by.rstrip(b'nd')
print(by)




# root = tk.Tk()
#
# frame1 = tk.Frame(root)
# frame2 = tk.Frame(root)
# root.title("tkinter frame")
#
# label = tk.Label(frame1, text="Label")
# label.grid()
#
#
# hi_there = tk.Button(frame2, text="say hi~").grid()
# text=tk.Text(frame2,bg='green',width=10).grid()
#
# frame1.pack(padx=1, pady=1)
# frame2.pack(padx=10, pady=10)
#
# f = tk.Frame(root)
# b1 = tk.Text(f, width=20, height=5, wrap=tk.NONE)
# b1.grid(column=0, row=1)
# s1 = tk.Scrollbar(f, orient=tk.HORIZONTAL, command=b1.xview)
# s1.grid(column=0, row=2, sticky=tk.EW)
# f.pack()

# root.mainloop()


# print(socket.gethostbyname(socket.gethostname()))
# str='sdsfgsg'
# print(type(str.find('a')))

# for line in open('/url.txt'):
#     print (line)
#     print('1')
# f.write('ergergergergergergergregreg')
# f.close()

# sources=['sdssdds','sdsdsdsfdfdgdg']
#
# root = tk.Tk()
# root.geometry('500x500')
# root.title('搜到的资源')
# for source in sources:
#     print('资源：{}', source)
#     frame = tk.Frame(root)
#     text = tk.Text(frame, height=1, width=20, wrap=tk.NONE)
#     text.insert('1.0', source)
#     text.config(state='disabled')
#     text.grid(row=1, column=0)
#     tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text.xview).grid(row=2, column=0, sticky=tk.EW)
#     frame.pack()
# root.mainloop()

# t0=time.time()
# while True:
#     if time.time()-t0>5:
#         break
#     print(time.time())

# str=''
# str=str+'sdfsf'
# print(str)
# str=str+str
# print(str)

# print(os.path.exists('C:/Users/11435/Desktop/waifu.png'))

#
# import tkinter as tk
# import time
#
# # 创建主窗口
# window = tk.Tk()
# window.title('进度条')
# window.geometry('630x150')
#
# # 设置下载进度条
# tk.Label(window, text='下载进度:', ).place(x=50, y=60)
# canvas = tk.Canvas(window, width=465, height=22, bg="white")
# canvas.place(x=110, y=60)
#
# # 填充进度条
# fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
# x = 500  # 未知变量，可更改
# n = 100 / x  # 465是矩形填充满的次数
# for i in range(x):
#     n = n + 465 / x
#     canvas.coords(fill_line, (0, 0, n, 60))
#     window.update()
#     time.sleep(0.001)  # 控制进度条流动的速度
#
#
#
# for t in range(x):
#     n = n + 465 / x
#     # 以矩形的长度作为变量值更新
#     canvas.coords(fill_line, (0, 0, n, 60))
#     window.update()
#     time.sleep(0)  # 时间为0，即飞速清空进度条
#
#
# window.mainloop()
# import load
# url=load.geturl()
# print(url)

# import tkinter as tk
#
# window = tk.Tk()  # 建立窗口window
# window.title('示例1')  # 窗口名称
# window.geometry("400x240")  # 窗口大小(长＊宽)
#
# textExample = tk.Text(window, height=10)  # 文本输入框
# textExample.pack()  # 把Text放在window上面，显示Text这个控件
#
#
# def getTextInput(text):
#     # result = textExample.get("1.0", "end")  # 获取文本框输入的内容
#     print(text)
#
#
# # Tkinter 文本框控件中第一个字符的位置是 1.0，可以用数字 1.0 或字符串"1.0"来表示。
# # "end"表示它将读取直到文本框的结尾的输入。我们也可以在这里使用 tk.END 代替字符串"end"。
# text=textExample.get('1.0','end')
# # 按钮（#command绑定获取文本框内容的方法）
# btnRead = tk.Button(window, height=1, width=10, text="Read", command=lambda :getTextInput(textExample))
# btnRead.pack()  # 显示按钮
#
# window.mainloop()  # 显示窗口


# import tkinter as tk
from tkinter import ttk
# import time
# def increment(*args):
#     for i in range(100):
#         p1["value"] = i+1
#         print(i)
#         root.update()
#         time.sleep(0.1)
# root = tk.Tk()
# root.geometry('360x240')
# p1 = ttk.Progressbar(root, length='2i', mode="determinate",
#                      orient=tk.HORIZONTAL)
# p1.grid(row=1,column=1)
# btn = ttk.Button(root,text="Start",command=increment)
# btn.grid(row=1,column=0)
# root.mainloop()

# win_progress = tk.Tk()
# win_progress.geometry('360x240')
# win_progress.title('下载进度')
# progress_bar = ttk.Progressbar(win_progress, length='2i', mode='determinate',
#                                orient=tk.HORIZONTAL)
# progress_bar.grid(row=1, column=1)
# progress_bar['value'] = 20
# win_progress.update()
# # win_progress.mainloop()
#
# a='D:\苍组的文件'
# os.system("start explorer %s")


# coding=utf-8




def handler(event, a):
    '''事件处理函数'''
    print(event)
    print("handler", a)


def handlerAdaptor(fun, **kwds):
    '''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


if __name__ == '__main__':
    root = tk.Tk()
    btn = tk.Button(text=u'按钮')

    # 通过中介函数handlerAdaptor进行事件绑定
    btn.bind("<Button-1>", handlerAdaptor(handler, a=1))

    btn.pack()
    root.mainloop()