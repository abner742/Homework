# coding:utf-8


import configparser
import os

# 用os模块来读取
# curpath = os.path.dirname(os.path.realpath(__file__))
# cfgpath = os.path.join(curpath, "new.ini")  # 读取到本机的配置文件


# 调用读取配置模块中的类

conf = configparser.ConfigParser()

conf.read('new.ini')
# 调用get方法，然后获取配置的数据

Server_IP = conf.get("server","Server_IP")
target_IP = conf.get("client", "target_IP")

PORT = conf.get("client", "PORT")
Server_Port = conf.get("server","PORT")