#	query.py

import socket
import os
import frozen_dir
import sys

def query(filename):
	#向局域网内广播query请求
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #创建UDP socket (IPv4)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	ip = getIP()
	ttl = 5
	message = 'query ' + filename + ' ' \
		+ ip + ' ' + str(ttl) #发送信息格式为 （query 文件名 IP TTL）
	ipaddress = '255.255.255.255'
	port = 16380

	s.sendto(message.encode('utf-8'), (ipaddress, port))	#发送广播信息
	s.close()

def get(filename, filepath, ipaddress, filesize):
	#收到返回的ACK信息后，向第一个传回信息的peer发送get请求
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建TCP socket (IPv4)
	s.bind(('0.0.0.0', 16580))
	message = 'get ' + filepath
	port = 16381
	#print(ipaddress)
	s.connect((ipaddress[0], port))	#建立TCP连接
	s.send(message.encode('utf-8'))	#发送get请求
	#download_path = os.path.abspath(os.path.dirname(__file__)) + '/download/'
	download_path = os.path.abspath(frozen_dir.app_path()) + '/download/'
	try:
		#print(download_path + filename)
		curr_size = 0
		print('文件大小共{}bytes'.format(filesize))
		with open(download_path + filename, 'wb') as file:
			while True:
				data = s.recv(65535)
				#print("recv" + str(data))
				if data == b'end' or data == b'':
					print('')
					break
				else:
					#print(data)
					curr_size += len(data)
					file.write(data)
					done = int(50*(curr_size/filesize))
					sys.stdout.write("\r[%s%s]" % ('█' * done, ' ' * (50 - done)))
					sys.stdout.flush()
					if curr_size == filesize:
						print('')
						break
	except Exception as e:
		s.close()
		print(e)
		return False
	#print('finish')
	s.close()
	return True

def send_quit():
	# 向本机监听线程发送退出信息
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto('quit'.encode('utf-8'), ('127.0.0.1', 16380))
	s.close()
	s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	TCP_PORT = 16381
	s_tcp.connect(('127.0.0.1', TCP_PORT))
	s_tcp.send('quit'.encode('utf-8'))
	s_tcp.close()

def getIP():
	return socket.gethostbyname(socket.gethostname())



# 大致实现思路：
# 1. 用固定文件夹作为共享文件夹位置
# 2. 请求方输入文件名
# 3. 向局域网内广播query请求信息 (UDP)
# 4. 收到信息的peer在本地的共享文件夹中搜索该文件，如果存在，向请求方发送一个ACK
# 5. 若不存在，则向本地存储的IP地址转发请求（为了防止死循环 应设置TTL）
# 6. 请求方向第一个传回ACK信号的peer发送get请求 (TCP)
# 7. 建立连接，进行附件下载

# 具体问题：
# 1. 如何同时监听和发送信息 => 多线程
# 2. 监听线程收到ACK之后如何通知发送线程发送get请求？ => 可以将ACK监听放到客户端线程中去
# 3. 若网络中无该文件，如何判断？ => 超过一定时间未收到ACK，则说明无该文件
# 4. 联机测试中，MSI无法接收到Surface发出的广播，反之则可以 => 发现是防火墙的问题，关掉就好了

