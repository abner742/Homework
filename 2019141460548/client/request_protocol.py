from config import *


# 客户端请求协议
class RequestProtocol(object):

    @staticmethod
    def request_login(username, password):
        """
        登录请求
        :param username:用户名
        :param password: 密码
        :return: 返回请求字典
        """
        request = {}
        request['request_id'] = REQUEST_LOGIN
        request['username'] = username
        request['password'] = password
        return request

    @staticmethod
    def request_chat(username, msg):
        """
        聊天请求
        :param username: 用户名
        :param msg: 消息
        :return: 返回请求字典
        """
        request = {}
        request['request_id'] = REQUEST_CHAT
        request['username'] = username
        request['message'] = msg
        return request

    @staticmethod
    def request_register(username, password, nickname):
        """
        注册请求
        :param username: 用户名
        :param password: 密码
        :param nickname: 昵称
        :return: 返回请求字典
        """
        request = {}
        request['request_id'] = REQUEST_REGISTER
        request['username'] = username
        request['password'] = password
        request['nickname'] = nickname
        return request