import socket
import configparser
import time
import os
import logging


# 主函数方法
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

    # 绑定ip地址和端口
    addr = (ip, port)
    soc.bind(addr)

    # 打印操作成功的信息
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "已成功在ip地址"
          , addr[0], ":", addr[1], "号端口建立UDP服务器！")

    # 创建clients用户列表，把用户名称和端口号以name:addr的字典形式存储进clients中
    clients = {}

    # 服务器工作主循环
    while True:
        try:
            # 把从客户端接收用户信息
            data, addr = soc.recvfrom(1024)

            # 若addr不在clients中，说明是第一次进入聊天服务器，将接收其名称和地址存入clients
            if addr not in clients:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      '"%s" 来自ip地址 %s:%s 号端口已连接' % (data.decode('utf-8'), addr[0], addr[1]))
                for address in clients:  # 从clients遍历数据出来address
                    soc.sendto(data + ' 已进入聊天室~'.encode('utf-8'), address)
                clients[addr] = data.decode('utf-8')
                # 反之则正常进行信息服务逻辑
                continue
            
            # 若发送的信息中没有EXIT，则服务器端打印接收到的信息，同时将用户发送的信息发给其余客户端（均显示时间）
            if 'EXIT'.lower() not in data.decode('utf-8').lower():
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      '"%s" 来自ip地址 %s:%s 号端口' % (data.decode('utf-8'), addr[0], addr[1]))
                for address in clients:
                    if address != addr:
                        soc.sendto((time.strftime("%Y-%m-%d %H:%M", time.localtime())
                                    + ' ').encode('utf-8') + data, address)
                
            # 反之，则从clients里删除该用户的信息，同时服务器打印离开提示，并向其他客户端发送提示（均显示时间）
            else:
                name = clients[addr]
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      '"%s" 来自ip地址 %s:%s 号端口已断开连接' % (name, addr[0], addr[1]))
                clients.pop(addr)
                for address in clients:
                    soc.sendto((time.strftime("%Y-%m-%d %H:%M", time.localtime())
                                + ' ' + name + ' 离开了...').encode('utf-8'), address)



        # 出错时发送报错信息
        except ConnectionResetError:
            logging.warning('用户离开时出错！')


if __name__ == '__main__':
    main()
