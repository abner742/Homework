from PyQt5 import QtGui
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtWidgets import *
import sys
import socket
from threading import Thread


class Client(QWidget):
    # 初始化界面
    def __init__(self):
        QWidget.__init__(self)
        # 设置窗口大小
        self.button = QPushButton("发送", self)
        self.message = QLineEdit(self)
        self.content = QTextBrowser(self)
        self.setGeometry(600, 300, 360, 300)
        # 设置标题
        self.setWindowTitle("聊天室")
        self.add_ui()
        # 与服务器连接
        self.client = socket.socket()
        self.client.connect(("127.0.0.1", int(input("请输入服务器运行在的端口号"))))
        self.work_thread()

    # 设置界面中组件
    def add_ui(self):
        # 多行文本显示，显示所有聊天消息
        self.content.setGeometry(30, 30, 300, 150)

        # 单行文本，消息发送框
        self.message.setPlaceholderText(u"输入发送内容")
        self.message.setGeometry(30, 200, 300, 30)

        # 发送按钮
        # self.button.setFont("微软雅黑",10,QFont.Bold)
        self.button.setGeometry(270, 250, 60, 30)

    # 发送信息
    def send_msg(self):
        msg = self.message.text()
        self.client.send(msg.encode())
        if msg.upper() == "Q":
            self.client.close()
            self.destroy()
        self.message.clear()

    # 接受信息
    def recv_msg(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                print(data)
                data = data + "\n"
                self.content.append(data)
                self.content.moveCursor(self.content.textCursor().End)  # 文本框显示到底部
            except:
                exit()

    def btn_send(self):
        self.button.clicked.connect(self.send_msg)

    # 线程处理
    def work_thread(self):
        Thread(target=self.btn_send).start()
        Thread(target=self.recv_msg).start()


if __name__ == '__main__':
    print("创建server成功了！！！")
    print("已经自动为您打开client")
    print("接下来的操作与client有关")
    print("请继续在黑框里按照提示操作")
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())
