from config import *


# 服务器相应协议的数据处理
class ResponseProtocol(object):
    @staticmethod
    def response_login(result, nickname, username):
        """
        生成用户登录的响应
        :param result: 0表示登录失败 1表示登录成功
        :param nickname: 用户昵称，登陆失败为空
        :param username: 用户登录账号，如果登录失败为空
        :return:供返回给用户的登录结果响应
        """
        response = {}
        response['response_id'] = RESPONSE_LOGIN
        response['result'] = result
        response['nickname'] = nickname
        response['username'] = username

        return response

    @staticmethod
    def response_chat(nickname, message):
        """
        生成返回给用户的消息响应
        :param nickname:发送消息的用户昵称
        :param message:消息
        :return:返回给用户的消息响应
        """
        response = {}
        response['response_id'] = RESPONSE_CHAT
        response['nickname'] = nickname
        response['message'] = message
        return response

    @staticmethod
    def response_register(result, username, nickname):
        """
        生成返回给用户的注册消息响应
        :param result: 0表示注册失败 1表示注册成功
        :param username: 注册的用户名
        :param nickname: 注册的昵称
        :return: 返回给用户的注册消息响应
        """
        response = {}
        response['response_id'] = RESPONSE_REGISTER
        response['result'] = result
        response['username'] = username
        response['nickname'] = nickname
        return response

    @staticmethod
    def response_user_list(user_list):
        """
        返回在线列表
        :param user_list:
        :return:
        """
        response = {}
        response['response_id'] = RESPONSE_USER_LIST
        response['user_list'] = user_list
        return response
