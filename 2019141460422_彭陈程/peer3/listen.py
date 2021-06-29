import os.path
import socket
import time
import tkinter as tk
from download import download
import tkinter.messagebox
from load import *

from search import search


def listen_query():  # 监听查询
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 建立UDP套接字
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # 设置套接字接收UDP广播
    udp_port = getudp_id()  # 查询广播发送到的本地端口
    s.bind(('', udp_port))
    while True:  # 持续监听
        # print('正在监听udp广播')
        data, address = s.recvfrom(65535)
        data = data.decode('utf-8')
        data = data.split(' ')
        # print(data)
        if data[0] == 'query':
            # print('收到一个查询')
            keyword = data[1]
            # print(data)
            ip = data[2]
            udp_ack_port = int(data[3])
            ttl = int(data[4]) - 1  # 转发次数减1
            filepaths = search(keyword)  # 寻找是否有这个关键字对应的文件路径确定是否有相关文件
            if filepaths == []:  # 没有相关文件
                if ttl == 0:  # ttl为0什么都不做 继续监听
                    continue
                else:  # 否则继续在自己所知的端口里帮忙转发
                    message = 'query' + ' ' + keyword + ' ' + ip + ' ' + str(udp_ack_port) + ' ' + str(ttl)
                    udp_ports = getudp_port()
                    ip = getIP()
                    for port in udp_ports:
                        s.sendto(message.encode('utf-8'), (ip, port))
            else:  # 找到有关文件 返回包含路径的ACK信息
                message = 'ack'
                # filepaths_2=dict()#包含路径和大小的字典
                for filepath in filepaths:
                    filepath = filepath.replace('\n', '').replace('\r', '')
                    # print(filepath)
                    if os.path.exists(filepath):
                        filesize = os.path.getsize(filepath)
                        # filepaths_2[filepath] = filesize
                        message += ' ' + filepath + '_' + str(filesize)
                        # print(message)
                # print('发送一个ack')
                message+=' '+str(gettcp_port())
                s.sendto(message.encode('utf-8'), (ip, udp_ack_port))

        else:
            continue


def listen_ack():
    # print('listen_ack开始运行')
    ack_port = getudp_ack_port()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', ack_port))
    s.settimeout(2)  # 搜索的时间
    # s.listen(5)#udp无listen队列 麻了

    sources = []
    message = []
    # t0=time.time()#初始时间
    while True:
        try:
            data, address = s.recvfrom(65535)
            # print(time.time())
            # if time.time()-t0>20:#只搜索5s 搜不到就算了
            #     break
            # print('收到udp消息')
            message = data.decode('utf-8').split(' ')
            # print(message)
            if message[0] == 'ack':
                for source in message[1:-1]:
                    sources.append(source)
                    # print('找到了一个资源')
        except:  # 超时啥也没找到跳出循环
            break
    s.close()
    if not sources:
        tk.messagebox.askokcancel(title='提示', message='找半天啥也妹找到哇')
        return -1
    else:
        # print('开始绘制界面')
        sources=list(set(sources))
        tcp_port=int(message[-1])
        root = tk.Tk()
        root.geometry('500x500')
        root.title('搜到的资源')
        for source in sources:
            # print(source)
            frame = tk.Frame(root)
            text = tk.Text(frame, height=1, width=50, wrap=tk.NONE)
            text.insert('1.0', source)
            text.config(state='disabled')
            text.grid(row=1, column=0)
            tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text.xview).grid(row=2, column=0, sticky=tk.EW)
            button_download = tk.Button(frame, text='下载', command=lambda: download(source, tcp_port))
            button_download.grid(row=1, column=1)
            frame.pack()
        root.mainloop()
        return sources


def listen_download():  # 此时作为服务器端
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP 套接字
    tcp_port = gettcp_port()

    s.bind(('', tcp_port))
    s.listen(5)

    while True:
        client_socket, client_ip = s.accept()  # accept后未关闭
        data = client_socket.recv(65535)
        message = data.decode('utf-8')
        messages = message.split(' ')
        try:
            if messages[0] == 'down':
                filepath = messages[1]
                with open(filepath, "rb") as file:
                    while True:
                        file_data = file.read(65535)
                        if file_data:
                            client_socket.send(file_data)
                        else:
                            client_socket.send(b'end')
                            client_socket.close()
                            break
            else:
                continue
        except:
            continue
    s.close()
