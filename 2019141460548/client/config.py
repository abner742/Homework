import configparser

config = configparser.ConfigParser()
config.read("client.ini")

# 服务器相关配置
SERVER_IP = config.get("server", "SERVER_IP")
SERVER_PORT = int(config.get("server", "SERVER_PORT"))

# 通讯协议相关配置
REQUEST_LOGIN = '001'
REQUEST_CHAT = '002'
REQUEST_REGISTER = '004'
RESPONSE_LOGIN = '101'
RESPONSE_CHAT = '102'
RESPONSE_USER_LIST = '103'
RESPONSE_REGISTER = '104'
