import socket
from load import *
from tkinter import messagebox



def query_broadcast(text):
    # 带着关键字向局域网内广播查询请求
    keyword = text.get('1.0', 'end').replace('\n', '')
    if keyword == '':
        messagebox.showinfo("提示：","输入了空值")
        return -1
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建UDP套接字
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # 设置选项为广播

    ip = getIP()
    ttl = str(5)  # ttl表示转发次数
    # 发送信息的格式是 query keword ip ttl
    message = 'query' + ' ' + keyword + ' ' + ip + ' ' + str(getudp_ack_port())+' '+ttl
    ipaddress = getIP()  #获取自己的ip
    udp_ports = getudp_port()

    # print('正在发送查询广播%d'%udp_port)
    for udp_port in udp_ports:
        s.sendto(message.encode('utf-8'), (ipaddress, udp_port))  # 发送广播
    s.close()
