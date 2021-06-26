import socket
import sys
import os
import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from load import *


def download(source, tcp_port):
    source = source.split('_')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP socket (IPv4)
    s.bind(('0.0.0.0', gettcp_get_port()))
    message = 'down ' + source[0]
    # print(address)
    s.connect((getIP(), tcp_port))  # 建立TCP连接
    s.send(message.encode('utf-8'))  # 发送get请求
    filepath = source[0].split('/')
    filename = filepath[-1]
    try:
        # print(download_path + filename)
        curr_size = 0
        # print('文件大小共{}bytes'.format(source[1]))
        if not os.path.exists('download'):  # 如果此目录下没有文件夹dwownload 就创建一个
            os.makedirs('download')
        win_progress = tk.Tk()
        win_progress.geometry('360x240')
        win_progress.title('下载进度')
        progress_bar = ttk.Progressbar(win_progress, length='350', mode='determinate',
                                       orient=tk.HORIZONTAL)
        progress_bar.grid(row=1, column=1)
        with open('download/' + filename, 'wb') as file:
            while True:
                data = s.recv(65535)
                curr_size += len(data)
                if curr_size == int(source[1]) + 3:
                    data=data.rstrip(b'end')
                    file.write(data)
                else:
                    file.write(data)
                # #早先的控制台进度条不再需要
                # done = int(50 * (curr_size / int(source[1])))
                # print('百分比:')
                # print((curr_size / int(source[1])))
                # sys.stdout.write("\r[%s%s]" % ('█' * done, ' ' * (50 - done)))
                # sys.stdout.flush()
                progress_bar['value'] = 100 * (curr_size / int(source[1]))
                time.sleep(1)
                win_progress.update()  # 进度条更新
                # print('curr_size:%d\n'%int(curr_size))
                # print('source[1]:%d\n'%int(source[1]))
                if curr_size == int(source[1]) + 3:
                    result = tk.messagebox.askokcancel(title='提示', message='下载完成')
                    s.close()
                    if result is True:  # 因为会抽风，所以就干脆下载完了自动关闭进度条好了
                        win_progress.destroy()
                    else:
                        pass
                    break
        win_progress.mainloop()
    except Exception as e:
        s.close()
        print(e)
        return False
    return True
