import configparser

config = configparser.ConfigParser()
config.read("server.ini")

# 服务器配置信息
SERVER_IP = config.get("server", "SERVER_IP")
SERVER_PORT = int(config.get("server", "SERVER_PORT"))

# 数据库配置信息
DB_HOST = config.get("database", "DB_HOST")
DB_PORT = int(config.get("database", "DB_PORT"))
DB_NAME = config.get("database", "DB_NAME")
DB_USER = config.get("database", "DB_USER")
DB_PASS = config.get("database", "DB_PASS")

# 通讯协议相关配置
REQUEST_LOGIN = '001'
REQUEST_CHAT = '002'
REQUEST_REGISTER = '004'
RESPONSE_LOGIN = '101'
RESPONSE_CHAT = '102'
RESPONSE_USER_LIST = '103'
RESPONSE_REGISTER = '104'
