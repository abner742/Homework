from socket import *
import threading
from mail import  *
from config import *
from urllib import parse
import json,gzip
from datetime import datetime



class ServerThread(threading.Thread):

    # ------------------------------------------------------------------------------
    def __init__(self,name=None,clientsock = None, addr = None):
        threading.Thread.__init__(self,name=name)
        self.clientsock = clientsock
        self.addr = addr

    # ------------------------------------------------------------------------------
    # 获取http请求头中的信息
    def processMessage(self,msg):
        message = msg.split('\r\n')
        print(message)
        headerMap = {}

        if len(message) > 1:
            req_line = message[0].split()
            headerMap['method'] = req_line[0]
            headerMap['protocol'] = req_line[2]
            headerMap['fileName'] = req_line[1]

        for i in message:
            if ': ' in i:
                headerMap[i.split(': ', 1)[0]] = i.split(': ', 1)[1]
        return headerMap

    # ------------------------------------------------------------------------------

    def getReq(self,message):
        # 处理空请求
        if not message:
            return '',bytes('')
        try:
            if len(message) > 0:
                # 分割请求行
                reqLine = message.split()[1]
                if 'html' in reqLine:
                    f = open(WEB_ROOT + reqLine[1:], 'rb')

                    outputdata = f.read()
                    outputdata = gzip.compress(outputdata)
                    header = self.getHeader('html', reqLine, outputdata)
                    f.close()

                elif 'css' in reqLine:
                    f = open(WEB_ROOT + reqLine[1:], 'rb')
                    outputdata = f.read()
                    outputdata = gzip.compress(outputdata)
                    header = self.getHeader('css', reqLine, outputdata)
                    f.close()

                elif 'js' in reqLine:
                    f = open(WEB_ROOT + reqLine[1:], 'rb')
                    outputdata = f.read()
                    outputdata = gzip.compress(outputdata)
                    header = self.getHeader('js', reqLine, outputdata)
                    f.close()

                elif 'jpg' in reqLine or 'gif' in reqLine or 'png' in reqLine or 'png' in reqLine or 'ico' in reqLine:
                    f = open(WEB_ROOT + reqLine[1:], 'rb')
                    outputdata = f.read()
                    outputdata = gzip.compress(outputdata)
                    header = self.getHeader(reqLine[1:].split('.')[-1], reqLine, outputdata)
                    f.close()

                else:
                    message = message.split('\r\n') # message[0]: 'POST / HTTP/1.1'
                    reqLine = message[0].split() # reqLine: 'POST'
                    method = reqLine[0]
                    paramMap = {}

                    if method == 'POST':
                        url = message[0].split()[1]
                        reqBody = message[-1]
                        print(reqBody)
                        loginParam = reqBody.split('&')
                        for item in loginParam:
                            key = item.split('=')[0]
                            value = item.split('=')[1]
                            paramMap[key] = value

                    if method == 'GET':
                        print(reqLine)
                        url = reqLine[1].split('?')[0]
                        reqBody = reqLine[1].split('?')[1] # reqBody: username=a%27a%27a&password=a%27a%27a
                        loginParam = reqBody.split('&')
                        # 构造请求参数字典
                        for item in loginParam:
                            key = item.split('=')[0]
                            value = item.split('=')[1]
                            paramMap[key] = value
                    res = self.processWithUrl(url, paramMap)

                    # 把结果转化为gzip编码
                    outputdata = bytes(json.dumps(res), 'utf-8')
                    outputdata = gzip.compress(outputdata)
                    header = self.getHeader('query', reqLine, outputdata)

        except IOError:

            self.clientsock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            self.clientsock.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
            self.clientsock.close()

        return header,outputdata


    # ------------------------------------------------------------------------------
    def getHeader(self, type, reqLine, outputdata):
        # 构造http请求头
        header = "HTTP/1.1 200 OK\r\n"
        header += "date:{}\r\n".format(datetime.utcnow().strftime(GMT_FORMAT))
        header += "Content-Encoding: gzip\r\n"

        if type == 'html':
            header += "Content-Length:{}\r\n".format(len(outputdata))
            header += "Content-Type: text/html\r\n\r\n"

        elif type == 'css':
            header += "Content-Length:{}\r\n".format(len(outputdata))
            header += "Content-Type: text/css\r\n\r\n"

        elif type == 'js':
            header += "Content-Length:{}\r\n".format(len(outputdata))
            header += "Content-Type: application/javascript\r\n\r\n"

        elif type == 'query':
            header += "Content-Length:{}\r\n".format(len(outputdata))
            header += "Content-Type: application/json\r\n\r\n"

        elif type == 'jpg'  or type == 'gif' or type == 'png' or type == 'png' :
            if type == 'ico':
                type = 'x-icon'
            header += "Content-Length:{}\r\n".format(len(outputdata))
            header += "Content-Type: image/{}\r\n\r\n".format(type)

        return header

    # ------------------------------------------------------------------------------

    def run(self):
        while True:
                message = self.clientsock.recv(REC_CAPACITY).decode()
                header, outputdata = self.getReq(message)
                self.clientsock.send(header.encode())
                self.clientsock.send(outputdata)
                # print('\r\n0\r\n'.encode())


    # ------------------------------------------------------------------------------

    def processWithUrl(self, url, paramMap):
        res = ''
        if url == '/login':
            res, SMTPclient = loginMail(paramMap['username'], paramMap['password'])
            if res == True:
                self.username = parse.unquote(paramMap['username'])
                print('self.username', self.username,'self.clientsock',self.clientsock)
                self.SMTPclient = SMTPclient

        elif url == '/send':
            print('self.clientsock',self.clientsock)
            res = sendMail(self.username, paramMap['rev_mail'], paramMap['subject'], paramMap['content'], self.SMTPclient)
        else:
            res = False
        return  res

    # ------------------------------------------------------------------------------

def main():

    address = MULTI_SERVER_ADDRESS
    port = MULTI_SERVER_PORT
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(MAX_LINK_NUM)
    while True:
        clientsock,clientaddress=s.accept()
        t = ServerThread(clientsock = clientsock, addr = clientaddress)
        t.start()
    s.close()


if __name__ == '__main__':
    main()