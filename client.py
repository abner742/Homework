import socket

from query import query
from query import send_quit
from query import get
from listen import listen_ack

def client():
	ack_port = 17065
	print('        ----欢迎使用文件分享系统----         ')
	print('使用方法：1.输入get 文件名来向网络中的设备搜索文件')
	print('        2.输入quit退出')
	while True:
		command = input('>> ')
		if command == 'quit':
			#退出程序
			send_quit()
			return
		else:
			commands = command.split(' ')
			if commands[0] == 'get':
				if len(commands) == 1:
					print('请在get之后输入要搜索的文件名')
					continue
				filename = commands[1]
				query(filename)
				print('正在搜索{}'.format(filename))
				ack_res = listen_ack(ack_port)
				if ack_res == None:
					# 未搜索到
					print('未搜索到相应文件')
					continue
				filepath = ack_res[0]
				address = ack_res[1]
				filesize = int(ack_res[2])
				#print(filepath)
				#print(address)
				print('开始向{}下载{}'.format(address[0], filename))
				res = get(filename, filepath, address, filesize)
				if res:
					print('下载完毕')
				else:
					print('下载过程出现问题，请稍后再试')
			else:
				print('指令{}无效'.format(commands[0]))
				continue

