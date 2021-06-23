from socket import *
import base64

#登陆,分别输入邮箱账号和授权码
print('请输入您要登陆的qq邮箱账号')
fromaddress = input()
print('请输入您的授权码')
passi = input()

#确定发送邮件的对象
print('请输入发送对象的邮箱账号')
toaddress = input()

#简单的验证输入的邮箱地址是否符合最基本的格式，如果不符合，直接结束程序
if "@" not in toaddress:
	print('输入的邮箱格式不对，请确定收件人')
	exit()

#编写邮件的主题和文本内容
print('邮件的主题为')
subject = input()
print('邮件具体内容为')
msg = input()
contenttype = "text/plain"
endmsg = "\r\n.\r\n"

# 选择一个邮件服务，在我这里选择的是qq
mailserver = "smtp.qq.com"

# Sender and reciever
#fromaddress = "1240153152@qq.com"
#toaddress = "3125435020@qq.com"均为之前测试所用

# 由于邮箱输入信息会使用base64编码，因此需要进行编码
username = base64.b64encode(fromaddress.encode()).decode()
password = base64.b64encode(passi.encode()).decode()

#password = base64.b64encode("arzfrncnbxtpidai".encode()).decode()之前测试用的

# # 创建客户端套接字并建立连接
clientSocket = socket(AF_INET, SOCK_STREAM) 
clientSocket.connect((mailserver, 25))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# 发送 HELO 命令并且打印服务端回复
# 开始与服务器的交互，服务器将返回状态码250,说明请求动作正确完成
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# 发送"AUTH LOGIN"命令，验证身份.服务器将返回状态码334（服务器等待用户输入验证信息）
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
	print('334 reply not received from server')

## 发送验证信息
clientSocket.sendall((username + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
	print('334 reply not received from server')

clientSocket.sendall((password + '\r\n').encode())
recv = clientSocket.recv(1024).decode()

# 如果用户验证成功，服务器将返回状态码235
print(recv)
if (recv[:3] != '235'):
	print('235 reply not received from server')

#  发送 MAIL FROM 命令，并包含发件人邮箱地址
clientSocket.sendall(('MAIL FROM: <' + fromaddress + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')

#发送 RCPT TO 命令，并包含收件人邮箱地址，返回状态码 250
clientSocket.sendall(('RCPT TO: <' + toaddress + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')

# 发送 DATA 命令，表示即将发送邮件内容。服务器将返回状态码354（开始邮件输入，以"."结束）
clientSocket.send('DATA\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '354'):
	print('354 reply not received from server')

# 发送邮件内容
message = 'from:' + fromaddress + '\r\n'
message += 'to:' + toaddress + '\r\n'
message += 'subject:' + subject + '\r\n'
message += 'Content-Type:' + contenttype + '\t\n'
message += '\r\n' + msg
clientSocket.sendall(message.encode())

# 以"."结束。请求成功返回 250
clientSocket.sendall(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')

# QUIT命令 断开连接
clientSocket.sendall('QUIT\r\n'.encode())

# 关闭连接
clientSocket.close()
