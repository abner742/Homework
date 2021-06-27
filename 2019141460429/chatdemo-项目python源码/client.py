# coding=utf-8
# 导入python Qt库
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import sys
import socket
from threading import Thread


class client(QWidget):

    def __init__(self):
        # 初始化界面
        QWidget.__init__(self)
        # 设置窗口的大小与位置
        self.setGeometry(600,300,360,300)
        # 设置标题
        self.setWindowTitle("聊天室")
        # 添加背景
        palette = QtGui.QPalette()
        bg=QtGui.QPixmap(r"./image/background.jpg")
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(bg))
        self.setPalette(palette)
        self.add_ui()
        # 与服务器链接
        self.client = socket.socket()
        self.client.connect(("127.0.0.1",8989))
        self.work_thread()

    # 设置界面中的组件
    def add_ui(self):
        #多行文本显示，显示所有的聊天信息
        self.content=QTextBrowser(self)
        self.content.setGeometry(30,30,300,150)

        # 单行文本，消息发送框
        self.message = QLineEdit(self)
        self.message.setPlaceholderText(u"输入发送内容")
        self.message.setGeometry(30,200,300,30)

        # 发送按钮
        self.button = QPushButton("发送",self)
        self.button.setFont(QFont("微软雅黑",10,QFont.Bold))
        self.button.setGeometry(270,250,60,30)

    # 发送消息
    def send_msg(self):
        msg = self.message.text()
        self.client.send(msg.encode())
        if msg.upper()=="Q":
            self.client.close()
            self.destroy()
        self.message.clear()

    def btn_send(self):
        self.button.clicked.connect(self.send_msg)


    # 接收消息
    def recv_msg(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                print(data)
                data=data+"\n"
                self.content.append(data)
            except:
                exit()



    # 线程处理
    def work_thread(self):
        Thread(target=self.btn_send).start()
        Thread(target=self.recv_msg).start()


if __name__=="__main__":
    app = QApplication(sys.argv)
    client = client()
    client.show()
    sys.exit(app.exec())

