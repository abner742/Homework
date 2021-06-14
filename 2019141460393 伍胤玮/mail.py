from socket import *
import ssl
from base64 import b64encode
from config import *
from urllib import parse


class SMTPSocket:
    def __init__(self, server):

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket = ssl.wrap_socket(self.socket)
        self.socket.connect((server, SMTP_PORT))
        self.getServerReply()

    def sendAndReceive(self, cmd=''):
        data = str(cmd) + '\r\n'
        print(data.encode())
        self.socket.send(data.encode('utf-8'))
        return self.getServerReply()

    def getServerReply(self):
        reply = self.socket.recv(1024)
        print(reply)
        return reply

    # 不编码发送
    def sendDataWithoutEncode(self, data):
        self.socket.send(data)
        print(data)

class SMTPClient:
    def __init__(self, server):
        self.socket = SMTPSocket(server)
        self.socket.sendAndReceive('EHLO qq.com')

    # 登录认证
    def authenticate(self, user, password):

        userb64 = b64encode(bytes(user.encode('utf-8')))
        passb64 = b64encode(bytes(password.encode('utf-8')))

        self.socket.sendAndReceive('AUTH LOGIN')

        self.socket.sendDataWithoutEncode(userb64)
        self.socket.sendAndReceive()

        self.socket.sendDataWithoutEncode(passb64)
        authOutcome = self.socket.sendAndReceive()

        if authOutcome.decode().split(' ')[0] != str(235):
            return False
        return True

    def sendMail(self, FROM, TO, DATA):
        self.socket.sendAndReceive('MAIL FROM:<' + FROM + '>')
        self.socket.sendAndReceive('RCPT TO:<' + TO + '>')
        self.socket.sendAndReceive('DATA')
        res = self.socket.sendAndReceive(DATA + '\r\n' + '.')

        if '250' in res.decode('utf-8'):
            return True
        return False


def loginMail(username, password):
    print(username, password)
    username = parse.unquote(username)
    password = parse.unquote(password)
    SMTPclient = SMTPClient(SMTP_SERVER)
    loginResult = SMTPclient.authenticate(username, password)
    return  loginResult, SMTPclient


def sendMail(username, rev_mail, subject, content, SMTPclient):
    # 转化url编码
    rev_mail = parse.unquote(rev_mail)
    subject = parse.unquote(subject)
    content = parse.unquote(content)
    # 写smtp头和身体
    header = "Subject: " + subject + '\r\n'
    header += "From: " + username + '\r\n'
    header += "To: " + rev_mail + '\r\n'
    data = header + content
    sendResult = SMTPclient.sendMail(username, rev_mail, data)
    return sendResult
