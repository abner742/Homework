
#code=coding: utf-8

from socket import *
import threading
import os


def Server(client_socket, addr):
    print('Is connected from:', addr) 
    data = client_socket.recv(1024).decode()
    # 当服务器因为网络问题未收到返回信息就会退出
    if len(data) == 0:
        client_socket.close()
        return 

    Loc_doc = os.getcwd()
   # 服务器端可访问的文件目录
    print("************-----------**************\n")
    index = 4 
    # 检索文件的搜索路径
    # 找到路径
    while data[index] != ' ':
        index += 1
    # 如果检索文件为空，则默认导向访问成功的页面，
    if index == 5 : direction = os.path.join(Loc_doc, "Achieved.html") 
    else: direction = os.path.join(Loc_doc, data[5 : index])
    # 拼接出完整的路径
    if os.path.exists(direction) and direction.endswith(".html"):
        file=open(direction)
       # 打开路径中的文件
        Success_page = "HTTP/1.1 200 Found successfully!\r\n\r\n" + file.read() 
        # 构造成功报文反馈给服务器
        print(Success_page)
        client_socket.sendall(Success_page.encode())
       # 返回给客户端浏览器成功的页面
   
        client_socket.close() 
       #路径不存在则返回失败页面
    else:
        Fail_page = "HTTP/1.1 404 NotFound\r\n\r\n" + open(os.path.join(Loc_doc, "Failed.html")).read()
        print(Fail_page)
        client_socket.sendall(Fail_page.encode())
       # 返回客户端失败页面
       
        client_socket.close()
       # 关闭专门针对一个客户机程序创建的新套接字
    

if __name__ =='__main__': 
    Host = "" 
    #此程序在什么主机上运行，就会为该主机的IP地址
    Port = 2016 
   # 随机端口号
    Addr = (Host, Port)
    tcpSersock = socket(AF_INET, SOCK_STREAM) 
    # 创建一个套接字对象
    tcpSersock.bind(Addr) 
    # 将套接字绑定到服务器地址
    tcpSersock.listen(5) 
    #最多允许传入链接请求数是5
    print("等待连接ING......\n")                  
    while True:  #可以无限循环
        client_socket, addr = tcpSersock.accept() 
        # 调用 accept()函数之后，等待客户端的连接。
        thread = threading.Thread(target=Server, args=(client_socket,addr))  
        thread.start()
        #执行该线程

    tcpSersock.close()