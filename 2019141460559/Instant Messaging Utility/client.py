import socket
import tkinter
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
import os
import sys
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from  PIL import Image,ImageTk

IP = ''
PORT = ''
user = ''
listbox1 = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = '------Group chat-------'  # 聊天对象

def get_image(filename,width,height):
	im=Image.open(filename).resize((width,height))
	return ImageTk.PhotoImage(im)
#登陆窗口

root0 = tkinter.Tk()
root0.geometry("340x300")
root0.title('登录')
root0.resizable(0,0)
one = tkinter.Label(root0,width=300,height=150,bg="#E6E6F2")
one.pack()
canvas_root=tkinter.Canvas(root0,width=340,height=300)
im_root=get_image('11.png',200,100)
canvas_root.create_image(200,100,image=im_root)
canvas_root.pack()


IP0 = tkinter.StringVar()
IP0.set('')
PORT0 = tkinter.StringVar()
PORT0.set('')
USER = tkinter.StringVar()
USER.set('')

labelIP = tkinter.Label(root0,text='IP地址',bg="#E6E6F2")
labelIP.place(x=20,y=20,width=100,height=40)
entryIP = tkinter.Entry(root0, width=60, textvariable=IP0)
entryIP.place(x=120,y=25,width=100,height=30)

labelPORT = tkinter.Label(root0,text='端口号',bg="#E6E6F2")
labelPORT.place(x=20,y=70,width=100,height=40)
entryPORT = tkinter.Entry(root0, width=60, textvariable=PORT0)
entryPORT.place(x=120,y=75,width=100,height=30)

labelUSER = tkinter.Label(root0,text='用户名',bg="#E6E6F2")
labelUSER.place(x=20,y=120,width=100,height=40)
entryUSER = tkinter.Entry(root0, width=60, textvariable=USER)
entryUSER.place(x=120,y=125,width=100,height=30)

# 登录函数
def Login(*args):
	global IP, PORT, user
	IP=entryIP.get()
	PORT=entryPORT.get()
	# IP, PORT = entryIP.get().split(':')
	user = entryUSER.get()
	if not user:
		tkinter.messagebox.showwarning('warning', message='用户名为空!')
	else:
		root0.destroy()

# 登录页面续
loginButton = tkinter.Button(root0, text ="登录", command = Login,bg="#8E8E8E",fg="white")
loginButton.place(x=135,y=180,width=40,height=25)
root0.bind('<Return>', Login)

root0.mainloop()

# 建立连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, int(PORT)))
if user:
    s.send(user.encode())  # 发送用户名
else:
    s.send('用户名不存在'.encode())
    user = IP + ':' + PORT

# 聊天窗口
root1 = tkinter.Tk()
root1.geometry("640x480")
root1.title('群聊')
root1.resizable(0,0)

# 消息界面
listbox = ScrolledText(root1)
listbox.place(x=5, y=0, width=640, height=320)
listbox.tag_config('tag1', foreground='white',backgroun="purple")
listbox.insert(tkinter.END, '欢迎进入群聊，大家开始聊天吧!', 'tag1')
listbox.insert(tkinter.END, '私聊请输入 内容~用户名~对象', 'tag1')

INPUT = tkinter.StringVar()
INPUT.set('')
entryIuput = tkinter.Entry(root1, width=120, textvariable=INPUT)
entryIuput.place(x=5,y=320,width=580,height=170)

# 在线用户列表
listbox1 = tkinter.Listbox(root1)
listbox1.place(x=510, y=0, width=130, height=320)

# 消息发送函数
def send(*args):
	message = entryIuput.get() + '~' + user + '~' + chat+'~'+'1'
	s.send(message.encode())
	INPUT.set('')



def sendtxt(*args):
	filepath=entryIuput.get()
	with open(filepath,'r',encoding='utf-8') as fp:
		content = fp.read();
	print(content)
	message= content+'~'+user + '~' + chat+'~'+'2'
	s.send(message.encode())
	INPUT.set('')

# def sendPic(*args):
# 	filepath=entryIuput.get()
# 	if os.path.isfile(filepath):
# 		# 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
# 		fileinfo_size = struct.calcsize('128sl')
# 		# 定义文件头信息，包含文件名和文件大小
# 		fhead = struct.pack('128sl', bytes(os.path.basename(filepath).encode('utf-8')), os.stat(filepath).st_size)
# 		s.send(fhead)
# 		print('client filepath: {0}'.format(filepath))
# 		fp = open(filepath, 'rb')
# 		while 1:
# 			data = fp.read(1024)
# 			if not data:
# 				print('{0} file send over...'.format(filepath))
# 				break
# 			s.send(data)


# 聊天界面续
sendButton = tkinter.Button(root1, text ="\n发\n送",anchor = 'n',command = send,font=('Helvetica', 18),bg = 'white')
sendButton.place(x=575,y=320,width=65,height=300)
root1.bind('<Return>', send)

sendtxtButton=tkinter.Button(root1,text="\n发送\n文本\n文件",anchor= 'n',command= sendtxt,font=('Helvetica', 18),bg = 'white')
sendtxtButton.place(x=510,y=320,width=65,height=300)
root1.bind('<Return>',sendtxt)

# sendPicButton=tkinter.Button(root1,text="\n发送\n图片",anchor= 'n',command= sendPic,font=('Helvetica', 18),bg = 'white')
# sendPicButton.place(x=445,y=320,width=65,height=300)
# root1.bind('<Return>',sendPic)


# 消息接收函数
def receive():
	global uses
	while True:
		data = s.recv(500000)
		data = data.decode()
		print(data)
		try:
			uses = json.loads(data)
			listbox1.delete(0, tkinter.END)
			listbox1.insert(tkinter.END, "当前在线用户")
			listbox1.insert(tkinter.END, "------Group chat-------")
			for x in range(len(uses)):
				listbox1.insert(tkinter.END, uses[x])
			users.append('------Group chat-------')
		except:
			data = data.split('~')
			message = data[0]
			userName = data[1]
			chatwith = data[2]
			type= data[3]
			print(type)
			message = '\n' + message
			if type=='1':
				if chatwith == '------Group chat-------':   # 群聊
					if userName == user:
						listbox.insert(tkinter.END, message)
					else:
						listbox.insert(tkinter.END, message)
				elif userName == user or chatwith == user:  # 私聊
					if userName == user:
						listbox.tag_config('tag2', foreground='red')
						listbox.insert(tkinter.END, message, 'tag2')
					else:
						listbox.tag_config('tag3', foreground='green')
						listbox.insert(tkinter.END, message,'tag3')
				listbox.see(tkinter.END)

			if type=='2':
				if chatwith == '------Group chat-------':   # 群聊
					if userName == user:
						listbox.insert(tkinter.END, message)
					else:
						listbox.insert(tkinter.END, message)
				elif userName == user or chatwith == user:  # 私聊
					if userName == user:
						listbox.tag_config('tag2', foreground='red')
						listbox.insert(tkinter.END, message, 'tag2')
					else:
						listbox.tag_config('tag3', foreground='green')
						listbox.insert(tkinter.END, message,'tag3')
				listbox.see(tkinter.END)


r = threading.Thread(target=receive)
r.start()  # 开始线程接收信息

root1.mainloop()
s.close()
