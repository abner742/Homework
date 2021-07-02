from socket import *
import base64

# ------------------------------------------------------------------------

login_mailaddress = input('Please input your mailaddress:')    # 输入发送方163邮箱地址
login_password = input('Please input your mailaddress Authorization password:')      # 输入163邮箱授权密码(需要申请)
to_mailaddress = input('Please input the mailaddress you want to send to:')    # 输入收件邮箱地址

# ------------------------- SMTP Commands -------------------------------
END_MSG = '\r\n.\r\n'
FORMAT = 'UTF-8'
QUIT_CMD = 'QUIT\r\n'
HELLO_CMD = 'HELO Alice\r\n'
STARTTLS_CMD = 'STARTTLS\r\n'
AUTHORIZATION_CMD = 'AUTH LOGIN\r\n'
MAIL_FROM = 'MAIL FROM: <' + login_mailaddress + '> \r\n'  # 发送邮箱
RCPT_TO = 'RCPT TO: <' + to_mailaddress + '> \r\n'    # 收件邮箱
DATA_CMD = 'DATA\r\n'
# ------------------------------------------------------------------------

# 创建TCP套接字
mailserver1 = ('smtp.163.com', 25)  # (SMTP服务器地址,端口号)
clientSocket = socket(AF_INET, SOCK_STREAM)
# 连接服务器
clientSocket.connect(mailserver1)

recv = clientSocket.recv(1024).decode(FORMAT)

print('\nServer message after connection request: ' + recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# 发送 HELO 指令并输出服务器响应信息
clientSocket.send(HELLO_CMD.encode())
recv1 = clientSocket.recv(1024).decode(FORMAT)
print('Server response after HELO: ' + recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# 发送 AUTH LOGIN 指令并输出服务器响应信息
clientSocket.send(AUTHORIZATION_CMD.encode())
recv = clientSocket.recv(1024).decode(FORMAT)
print('Server response after AUTH LOGIN: ' + recv)

if recv[:3] != '334':
    print('334 Not received from the server')

# 发送用户邮箱以验证并输出服务器响应信息
clientSocket.send(
    (base64.b64encode(login_mailaddress.encode())) + '\r\n'.encode())
recv = clientSocket.recv(1024).decode(FORMAT)
print('Server response after sending username: ' + recv)

# 发送授权密码以验证并输出服务器响应信息
clientSocket.send(
    (base64.b64encode(login_password.encode())) + '\r\n'.encode())
recv = clientSocket.recv(1024).decode(FORMAT)
print('Server response after sending password: ' + recv)

if recv[:3] != '235':
    print('235 Not received from the server')

# 发送发送方邮箱地址并并输出服务器响应信息
clientSocket.send(MAIL_FROM.encode())
recv2 = clientSocket.recv(1024).decode(FORMAT)
print('Server response After MAIL FROM command: '+recv2)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# 发送收件方邮箱地址并输出服务器响应信息
clientSocket.send(RCPT_TO.encode())
recv3 = clientSocket.recv(1024).decode()
print('Server response After RCPT TO command: '+recv3)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# 发送 DATA 命令并输出服务器响应信息

clientSocket.send(DATA_CMD.encode())
recv4 = clientSocket.recv(1024).decode(FORMAT)
print('Server response After DATA command: ' + recv4)

if recv4[:3] != '354':
    print('354 reply not received from server.')

# 发送邮件内容
subject = 'Subject:' + input('Please input your subject:') + '\r\n\r\n'
clientSocket.send(subject.encode())
message = input('\nPlease enter your message: ')
message = (str(message) + '\r\n').encode()

clientSocket.send(message)
clientSocket.send(END_MSG.encode())
recv_msg = clientSocket.recv(1024)

print('\nServer response after sending message body: ' + recv_msg.decode())

if recv1[:3] != '250':
    print('250 reply not received from server.')

# 发送 QUIT 指令并输出服务器响应信息
clientSocket.send(QUIT_CMD.encode())
message = clientSocket.recv(1024)
print('Server response after QUIT: ' + message.decode())

# 关闭TCP连接
clientSocket.close()

print('Email sent successfully :)')
