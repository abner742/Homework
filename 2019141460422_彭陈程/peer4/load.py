import configparser
import os
import socket


def getudp_port():
    udp_ports = []
    path = 'portList.txt'
    try:
        for line in open(path):  # 打开保存已知公的peer
            udp_ports.append(int(line))  # 向udp_ports中添加
    except:
        return []  # 如果打不开或者无信息等错误 都返回空
    return udp_ports


def geturl():
    url = []
    path = 'url.txt'
    try:
        for line in open(path):
            # 这里可以加一个能否打开对应路径的判断 等打开菜加入url_list
            line.replace('\n', '').replace('\r', '')
            url.append(line)
            # print(line)
    except:
        return []
    return url


def deteleurl(url):
    try:
        with open('url.txt', 'r')as old_file:
            urls = old_file.readlines()
        with open('url.txt', 'w')as new_file:
            for item in urls:
                if url != item:
                    new_file.write(item)
        return True
    except:
        return False



def getIP():
    return socket.gethostbyname(socket.gethostname())



def gettcp_port():
    conf = configparser.ConfigParser()
    conf.read('port_config.ini')
    return conf.getint('port', 'tcp_port')


def getudp_ack_port():
    conf = configparser.ConfigParser()
    conf.read('port_config.ini')
    return conf.getint('port', 'udp_ack_port')


def gettcp_get_port():
    conf = configparser.ConfigParser()
    conf.read('port_config.ini')
    return conf.getint('port', 'tcp_get_port')

def getudp_id():
    conf = configparser.ConfigParser()
    conf.read('port_config.ini')
    return conf.getint('port', 'udp_id')