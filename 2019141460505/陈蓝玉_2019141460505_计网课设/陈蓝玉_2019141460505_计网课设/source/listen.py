#	listen.py

import socket
import os

from search import search
from load import getIPList

def listen_query():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#建立UDP socket
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	port = 16380		# UDP监听端口
	ipList = getIPList()			# 读取的本地已知IP列表

	s.bind(('', port))
	while True:
		# 持续监听，直到收到quit消息
		datacode, address = s.recvfrom(65535)
		data = datacode.decode('utf-8')
		#print("query: " + data)
		dataarr = data.split(' ')
		if dataarr[0] == 'query':
			#continue
			filename = dataarr[1]
			ip = dataarr[2]
			ttl = int(dataarr[3])-1  #设置ttl的目的主要是防止两个互相知道对方存在的节点重复查询
			filepath = search(filename)
			message = 'query ' + filename + ' ' + ip \
				+ ' ' + str(ttl)
			if filepath == None:	#未找到，则转发
				if ttl == 0:
					continue
				else:
					for ipaddress in ipList:
						s.sendto(message.encode('utf-8'), (ipaddress, port))
			else:		#找到，则回传带有文件路径的ACK信息
				ACK_PORT = 16382
				filesize = os.path.getsize(filepath)
				message = 'ack ' + filepath + ' ' + str(filesize)
				s.sendto(message.encode('utf-8'), (ip, ACK_PORT))
		elif dataarr[0] == 'quit':
			break
		else:
			continue

def listen_ack(ack_port) :
	# 因为需求中要求是对第一个发回ACK的设备进行连接
	# 因此，对ACK端口的监听应该是一次性的
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', ack_port))
	s.settimeout(10)	#设置10s的搜索时限
	try:
		data, address = s.recvfrom(65535)
		message = data.decode('utf-8').split(' ')
		filepath = message[1]
		filesize = message[2] 
		return filepath, address, filesize
	except:
		# except包含了两种情况：信息格式错误 以及等待超时
		return None

def listen_get():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建TCP socket
	TCP_PORT = 16381
	
	s.bind(('', TCP_PORT))
	s.listen(5)

	while True:
		client_socket, client_ip = s.accept() #accept后未关闭
		data = client_socket.recv(65535)
		message = data.decode('utf-8')
		messages = message.split(' ')
		try:
			command = messages[0]
			if command == 'get':
				#print('get')
				filepath = messages[1]
				with open(filepath, "rb") as file:
					while True:
						file_data = file.read(65535)
						#print("send" + str(file_data))
						if file_data:
							client_socket.send(file_data)
						else:
							client_socket.send(b'end')
							client_socket.close()
							break
			elif command == 'quit':
				s.close()
				break
			else:
				continue
		except:
			continue










