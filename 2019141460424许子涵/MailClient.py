# MailClient.py
from socket import *
import base64
# 选择一个邮件服务
mailServer = "smtp.163.com"
# 选择发送方（from）和接收方（to）地址
fromAddress = "a15152sk@163.com"
toAddress = "1119450385@qq.com"

# 发送方验证信息。
# 由于邮箱输入信息会使用base64编码，因此需要进行编码
username = str(base64.b64encode(fromAddress.encode('utf-8')),'utf-8')  # 此处为邮件客户端用户名 “a15152sk@163.com” 经过base64编码的过程
password = "Q1JaSlRHWkFMQkhQQVhEWA=="  # 此处不是密码，而是邮箱申请SMTP服务时需要的授权码，同理需要经过base64编码

# 创建客户端套接字并建立连接
serverPort = 25  # SMTP使用25号端口
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, serverPort))
# 从客户套接字中接收信息
recv = clientSocket.recv(1024).decode()
print(recv)
if '220' != recv[:3]:
    print('Command 220 no response')

# 发送 HELO 命令并且打印服务端回复
# 开始与服务器的交互，服务器将返回状态码250,说明请求动作正确完成
word = 'HELO man\r\n'
clientSocket.send(word.encode())  # 随时注意对信息编码和解码
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if '250' != recv1[:3]:
    print('Command 250 no response')

# 发送"AUTH LOGIN"命令，验证身份.服务器将返回状态码334（服务器等待用户输入验证信息）
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if '334' != recv2[:3]:
    print('Command 334 no response')

# 发送验证信息
clientSocket.sendall((username + '\r\n').encode())
recvUsername = clientSocket.recv(1024).decode()
print(recvUsername)
if '334' != recvUsername[:3]:
    print('Command 334 no response')

clientSocket.sendall((password + '\r\n').encode())
recvPassword = clientSocket.recv(1024).decode()
print(recvPassword)
# 如果用户验证成功，服务器将返回状态码235
if '235' != recvPassword[:3]:
    print('Command 235 no response')

# TCP连接建立好之后，通过用户验证就可以开始发送邮件。邮件的传送从MAIL命令开始，MAIL命令后面附上发件人的地址。
# 发送 MAIL FROM 命令，并包含发件人邮箱地址
clientSocket.sendall(('MAIL FROM: <' + fromAddress + '>\r\n').encode())
recvFrom = clientSocket.recv(1024).decode()
print(recvFrom)
if '250' != recvFrom[:3]:
    print('Command 250 no response')

# 接着SMTP客户端发送一个或多个RCPT (收件人recipient的缩写)命令，格式为RCPT TO: <收件人地址>。
# 发送 RCPT TO 命令，并包含收件人邮箱地址，返回状态码 250
clientSocket.sendall(('RCPT TO: <' + toAddress + '>\r\n').encode())
recvTo = clientSocket.recv(1024).decode()
print(recvTo)
if '250' != recvTo[:3]:
    print('Command 250 no response')

# 发送 DATA 命令，表示即将发送邮件内容。服务器将返回状态码354（开始邮件输入，以"."结束）
clientSocket.send('DATA\r\n'.encode())
recvData = clientSocket.recv(1024).decode()
print(recvData)
if '354' != recvData[:3]:
    print('Command 354 no response')

# 编辑邮件信息，发送数据
subject: str = "This is a test text for the computer network project"
contentType = "text/plain"

# 邮件内容： msg + endMsg
txt = "\r\n When you see these words, it means that the program is running successfully! Congratulations"
end = "\r\n.\r\n"

message = 'from:' + fromAddress + '\r\n' \
          + 'to:' + toAddress + '\r\n' \
          + 'subject:' + subject + '\r\n' \
          + 'Content-Type:' + contentType + '\t\n' \
          + '\r\n' + txt

clientSocket.sendall(message.encode())

# 以"."结束。请求成功返回 250
clientSocket.sendall(end.encode())
recvEnd = clientSocket.recv(1024).decode()
print(recvEnd)
if '250' != recvEnd[:3]:
    print('Command 250 no response')

# QUIT命令 断开连接
clientSocket.sendall('QUIT\r\n'.encode())

clientSocket.close()

