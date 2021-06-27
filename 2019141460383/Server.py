import configparser
import os
import socket
import logging


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket对象

    curPath = os.path.dirname(os.path.realpath(__file__))
    cfgPath = os.path.join(curPath, "config.ini")
    conf = configparser.ConfigParser()
    conf.read(cfgPath, encoding="utf-8")

    ip = conf.get("test1", "local_IP")
    port =int(conf.get("test1", "port1"))

    addr = (ip, port)
    s.bind(addr)  # 绑定地址和端口

    logging.info('UDP Server on %s:%s...', addr[0], addr[1])

    user = {}  # 存放用户数据的dictionary

    print("--------服务已启动----------")
    while True:

        try:

            '''
            data: 客户端的用户名称和发送的信息数据
            addr: addr[0]:客户端发送的IP地址，addr[1]:端口
            等待接收客户端消息存放在2个变量data和addr里
            '''
            data, addr = s.recvfrom(1024)

            # 判断收到的IP地址是否已经在本次群聊中
            # 如果不在
            if not addr in user:

                for address in user:  # 从user遍历数据出来address

                    # 发送某用户的进入聊天室信息到每个客户端
                    s.sendto(data + ' enter the zChat...'.encode('utf-8'), address)

                # 将接收的消息解码成utf-8并存在user中,key：addr,value：name
                user[addr] = data.decode('utf-8')
                # 如果addr在user里，则跳过本次循环
                continue

            # 判断字符“exit”是否在data中，如果在则代表退出聊天室
            if 'EXIT'.lower() in data.decode('utf-8'):

                name = user[addr]   # 找出user中addr对应的name
                user.pop(addr)      # 删除user里的addr

                # 从user取出address
                for address in user:
                    # 发送某用户的离开聊天室信息到每个客户端
                    s.sendto((name + ' exit...').encode(), address)
            else:
                print('"%s" from %s:%s' % (data.decode('utf-8'), addr[0], addr[1]))

                # 遍历address
                for address in user:
                    # address不等于addr时间执行下面的代码（即用户直接终止程序离开而不是输入exit，导致user中的信息还没有删除）
                    if address != addr:
                        s.sendto(data, address)  # 发送data和address到客户端

        except ConnectionResetError:
            logging.warning('Someone left unexcept.')


if __name__ == '__main__':
    main()
