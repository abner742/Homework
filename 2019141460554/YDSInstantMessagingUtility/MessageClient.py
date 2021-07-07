import socket
import threading
import os
import configparser
import logging
import time


# 接受消息方法，需要先send一次声明所占用的端口
def receive(soc, addr):
    """
        参数含义：
            soc：一个实例化socket对象
            addr：服务器IP和端口
     """
    soc.sendto(name.encode('utf-8'), addr)
    while True:
        data = soc.recv(1024)
        print(data.decode('utf-8'))


# 发送数据方法
def send(soc, addr):
    """
        参数含义：
            soc：一个实例化socket对象
            addr：服务器IP和端口
    """
    while True:
        string = input('')
        message = name + ' : ' + string
        data = message.encode('utf-8')
        soc.sendto(data, addr)
        if string.lower() == 'EXIT'.lower():
            break


# 主函数方法，通过多线程来实现多个客户端之间的信息交流
def main():
    # 创建socket对象
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # config.ini中获取服务器ip和端口号
    cur_path = os.path.dirname(os.path.realpath(__file__))
    cfg_path = os.path.join(cur_path, "config.ini")
    conf = configparser.ConfigParser()
    conf.read(cfg_path, encoding="utf-8")

    # 赋值
    ip = conf.get("402c", "ip")
    port = int(conf.get("402c", "port"))

    # 连接服务器
    try:
        server = (ip, port)
    # 若连接失败则报错
    except OSError:
        logging.warning('连接服务器时出错')

    # 等待一段时间以确保连接建立成功，否则输入的信息不会发送
    print("正在建立连接，请稍侯...")
    time.sleep(3)
    print("连接建立成功！")

    # 多线程的收发
    tr = threading.Thread(target=receive, args=(soc, server), daemon=True)  # 接收线程
    ts = threading.Thread(target=send, args=(soc, server))  # 发送线程
    tr.start()
    ts.start()
    ts.join()

    # 发送完”EXIT“后结束，关闭socket
    soc.close()


if __name__ == '__main__':
    print("-----欢迎使用YDS实时信息工具,退出请输入\"EXIT\"-----")
    name = input('请输入你的名称:')
    print('--------------------%s--------------------' % name)
    main()
