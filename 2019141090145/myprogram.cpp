from socket import *
import sys
import os
import time
serverName = 'DESKTOP-RPMTUJK'
serverPort = 12003

#if len(sys.argv) <= 1:
#    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
#	sys.exit(2)

# 为代理服务器 创建一个TCP套接字、绑定端口号、设置服务器最大连接客户机数量为3(因为是多线程Web服务器)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('',1234))
tcpSerSock.listen(3)

while 1:
	# 准备从客户机接收响应消息
	print ('准备从客户机接收响应消息...')
	tcpCliSock, addr = tcpSerSock.accept()
	print ('接收到一个连接，来自：', addr)
	
	# 获取客户机发送过来的消息
	message = tcpCliSock.recv(4096).decode()
	print ('客户机发送过来的消息：',message)
	
	# 从消息从提取出文件名
	filename = message.split()[1].partition("//")[2].replace('/','_')
	print ('文件名：',filename)
	fileExist = "false"
	
	try:
		# 检查要访问的文件是否在此Web代理服务器中
		print ('开始检查代理服务器中是否存在文件：',filename)
		f = open(filename, "r")
		outputdata = f.readlines()
		fileExist = "true"
		print ('文件存在在代理服务器中')
		# 文件存在在代理服务器中，返回响应消息(请求的web网页)给客户机
		#tcpCliSock.send("HTTP/1.0 200 OK\r\n")
		#tcpCliSock.send("Content-Type:text/html\r\n")
		for i in range(0,len(outputdata)):
				tcpCliSock.send(outputdata[i].encode())	
		print ('Read from cache')
			
	# 文件不在代理服务器当中，代理服务器就会向远端服务器请求消息，保存好了再返回给客户机
	except IOError:
		if fileExist == "false":
			print ('文件不在代理服务器当中，开始向远端服务器请求网页')
			# 在代理服务器中创建一个TCP套接字
			c = socket(AF_INET,SOCK_STREAM)
			
			hostn = message.split()[1].partition("//")[2].partition("/")[0]
			print ('Host Name: ',hostn)
			try:
				# TCP套接字c 连接到远端服务器80端口
				c.connect((hostn,80))
				print ('套接字连接到主机的80号端口')
				
				# 在套接字上创建一个临时的文件，而且要向80端口(远端服务器)请求信息
				#for the file requested by the client
				#fileobj = c.makefile('r', 0)
				#fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")
				
				# 代理服务器 读取 从远端服务器从响应的消息
				c.sendall(message.encode())
				buff = c.recv(4096)
				tcpCliSock.sendall(buff)
				
				# 在代理服务器中 创建一个新的文件 用于存放请求过来的消息
				# 将代理服务器中的响应 发送到客户端套接字，并将相应的文件发送到缓存中
				tmpFile = open("./" + filename,"w")
				tmpFile.writelines(buff.decode().replace('\r\n','\n'))
				tmpFile.close()
				
			except:
				print ("代理服务器向远端服务器请求网页失败")
		else:
			# 如果客户机请求的消息在远端服务器也找不到，就说明请求不到了
			print ('文件存在，但是还是出现了 IOError异常')

	# 关闭客户机 和 代理服务器的TCP套接字
	print ('关闭套接字：tcpCliSock')
	tcpCliSock.close()
# 关闭代理服务器 和 服务器的TCP套接字
print ('关闭套接字：tcpSerSock')
tcpSerSock.close()
