import tkinter
import time
from email.mime.text import MIMEText
import smtplib
from tkinter import messagebox

class EmailSend:
    def __init__(self):
        # 进行gui部分的窗口搭建实现可视化操作
        # 窗口创建
        window = tkinter.Tk()
        # 大小设定
        window.geometry("500x400")
        # 窗口缩放禁止
        window.resizable(width=False, height=False)
        # 定义title
        window.title("邮件发送")
        # 主题定义标签
        label = tkinter.Label(window, text="邮件主题")
        # 把文本放入窗口
        label.pack()
        # 文本框 主题
        self.title = tkinter.Entry(window, width=50)
        self.title.pack()

        # 定义内容标签
        label = tkinter.Label(window, text="邮件内容")
        # 把文本放入窗口
        label.pack()
        # 文本框 内容
        self.con = tkinter.Entry(window, width=50)
        self.con.pack()

        # 定义内容标签
        label = tkinter.Label(window, text="发件人账号")
        # 把文本放入窗口
        label.pack()
        # 文本框 账号
        self.user = tkinter.Entry(window, width=50)
        self.user.pack()

        # 定义内容标签
        label = tkinter.Label(window, text="授权码（密码）")
        # 把文本放入窗口
        label.pack()
        # 文本框 授权码
        self.pwd = tkinter.Entry(window, width=50)
        self.pwd.pack()

        # 定义内容标签
        label = tkinter.Label(window, text="收件人")
        # 把文本放入窗口
        label.pack()
        # 文本框 收件人
        self.to = tkinter.Entry(window, width=50)
        self.to.pack()

        # 发送按钮
        button = tkinter.Button(window, text="点击发送", command=self.send)
        button.pack(side="top", pady=20, ipady=10, ipadx=20)
        timetxt = time.strftime('%Y-%m-%d-%H:%M')
        label_time = tkinter.Label(window, text="发送时间：【%s】" % timetxt)
        label_time.pack()
        # 显示
        window.mainloop()
        pass

    def send(self):
        # 当触发发送按钮的时候来调用
        # SMTP 邮件发送方法
        # 邮件发送所需：邮件主题，邮件内容，邮件发件人账号，授权码，收件人
        # 服务
        server = "smtp.163.com"
        # 账号
        user = self.user.get()
        # 授权码
        pwd = self.pwd.get()
        # 内容
        content = self.con.get()
        # 内容先去转成邮件形式
        content = MIMEText(content)
        # 发件人
        content["From"] = user
        # 收件人
        to = self.to.get()
        # 标题
        content["subject"] = self.title.get()
        # 定义邮件对象
        email_obj = smtplib.SMTP_SSL(server, 465)
        # 登录
        email_obj.login(user=user, password=pwd)
        # 发送
        email_obj.sendmail(user, to, content.as_string())
        # 断开连接
        email_obj.quit()
        # 弹框提示发送成功
        messagebox.showinfo("发送成功", "发送成功")
        pass

if __name__ == '__main__':
    wind = EmailSend()
    pass
