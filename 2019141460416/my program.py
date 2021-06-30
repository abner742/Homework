# Homework
计算机网络03班课程大作业
# *** python 多线程web服务器的设计    ****#
# *************************************#
from socket import *
'''引入线程模块'''
import threading
import os

'''自定义线程函数'''
'''针对线程使用编写的函数'''
def Server(tcpClisock, addr):
    '''将缓冲区大小设置为1KB'''
    BUFSIZE = 1024
    print('Waiting for the connection：', addr)
    data = tcpClisock.recv(BUFSIZE).decode()
    filename = data.split()[1]
    filename = filename[1:]

    '''当网络质量差没有收到浏览器的访问数据时执行'''
    if filename == "":
        tcpClisock.close()
        print("请输入要访问的文件")

    base_dir = os.getcwd()
    file_dir = os.path.join(base_dir,filename)

    '''当访问的文件在本地服务器存在时执行'''
    if os.path.exists(file_dir):
        f = open(file_dir,encoding = 'utf-8')
        '''构造成功报文反馈给服务器'''
        SUCCESS_PAGE = "HTTP/1.1 200 OK\r\n\r\n" + f.read()
        print(SUCCESS_PAGE)
        '''返回给客户端浏览器成功的页面'''
        tcpClisock.sendall(SUCCESS_PAGE.encode())
        '''关闭专门针对一个客户机程序创建的新套接字'''
        tcpClisock.close()
    else:
        '''如果不存在，返回失败页面'''
        FAIL_PAGE = "HTTP/1.1 404 NotFound\r\n\r\n" + open(os.path.join(base_dir, "fail.html"), encoding="utf-8").read()
        print(FAIL_PAGE)
        '''返回给客户端浏览器失败的页面，sendall函数只可以发送字节类型，对字符串数据进行转换'''
        tcpClisock.sendall(FAIL_PAGE.encode())
        '''关闭专门针对一个客户机程序创建的新套接字'''
        tcpClisock.close()

'''主函数'''
if __name__ == '__main__':

    '''分配IP、端口、创建套接字对象'''
    '''地址=主机名+端口号'''
    ADDR = ("", 8080)
    '''创建套接字对象'''
    tcpSersock = socket(AF_INET, SOCK_STREAM)
    '''将套接字绑定到服务器地址，且绑定的是源ip地址以及源端口号。始终欢迎别的套接字的申请接入。'''
    tcpSersock.bind(ADDR)
    '''启用服务器监听,此处说明在连接被转接或拒绝之前允许传入最大链接请求数为5'''
    tcpSersock.listen(5)
    print("waiting for connection......\n")
    '''进入无限循环'''
    while True:
        '''调用 accept()函数开启一个单线程服务器，等待客户端连接'''
        tcpClisock, addr = tcpSersock.accept()
        thread = threading.Thread(target=Server, args=(tcpClisock, addr))
        '''开始执行该线程'''
        thread.start()
    tcpSersock.close()




