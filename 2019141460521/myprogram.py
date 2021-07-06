import smtplib
import tkinter.messagebox
from tkinter import *
from email.mime.text import MIMEText
from email.utils import formataddr

sn = 123456789  # 发件人qq
p = 'abcdefghijkl'  # 发件人qq邮箱授权码
rn = 123456789  # 收件人qq
s = 'It is the subject'  # 主题
c = 'It is the content'  # 正文
sname = 'It is the sender name'  # 发件人姓名
state = True


# 检查是否发送成功
def check_state():
    global state
    print(state)
    if state:
        tkinter.messagebox.showinfo("成功", "邮件发送成功")
    else:
        tkinter.messagebox.showerror("错误", "邮件发送失败\n请关闭写邮件窗口\n重新登陆")


# 发送邮件
def mail():
    global state
    state = True
    qqnums: str = "%d@qq.com" % (int(sn))
    my_sender: str = qqnums  # 发件人QQ邮箱账号
    my_pass = p  # 发件人QQ邮箱授权码
    qqnumr: str = "%d@qq.com" % (int(rn))
    my_receiver: str = qqnumr  # 收件人QQ邮箱账号
    my_subject: str = s
    my_content: str = c
    my_sendername: str = sname
    try:
        msg = MIMEText(my_content, 'plain', 'utf-8')
        msg['From'] = formataddr([my_sendername, my_sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["收件人邮箱名字", my_receiver])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = my_subject  # 邮件的主题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是2
        server.login(my_sender, my_pass)  # 发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_receiver], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        state = False
    check_state()


# 获取发送的信息
def sendmail(entry1, entry2, entry3, entry4):
    global rn
    global s
    global c
    global sname
    rn = entry1.get()
    s = entry2.get()
    c = entry3.get()
    sname = entry4.get()
    mail()


# 主界面，填写内容
def main_face():
    mface = Tk()
    mface.title("邮件发送窗口")
    mface.geometry("1296x656")
    framemf1 = Frame(mface)
    l1 = Label(framemf1, text="收件人QQ号码：")
    l1.pack(side=LEFT)
    e1 = Entry(framemf1, bd=5, width=50)
    e1.pack(side=LEFT, fill=X)
    framemf1.pack(fill=X, pady=15)
    framemf2 = Frame(mface)
    l2 = Label(framemf2, text="             主题：")
    l2.pack(side=LEFT)
    e2 = Entry(framemf2, bd=5, width=50)
    e2.pack(side=LEFT, fill=X)
    framemf2.pack(fill=X, pady=15)
    framemf3 = Frame(mface)
    l3 = Label(framemf3, text="             正文：")
    l3.pack(side=LEFT)
    e3 = Entry(framemf3, bd=5, width=150)
    e3.pack(side=LEFT, fill=Y)
    framemf3.pack(fill=X, pady=15)
    framemf4 = Frame(mface)
    l4 = Label(framemf4, text="    发件人名字：")
    l4.pack(side=LEFT)
    e4 = Entry(framemf4, bd=5, width=50)
    e4.pack(side=LEFT, fill=X)
    framemf4.pack(fill=X, pady=15)
    framemf5 = Frame(mface)
    send = Button(framemf5, text="发送", command=lambda: sendmail(e1, e2, e3, e4))
    send.pack(pady=10, ipadx=5)
    framemf5.pack(fill=X, pady=15)
    mface.mainloop()


# 获取发件人的QQ和授权码
def get_entry(entry1, entry2):
    global sn
    global p
    sn = entry1.get()
    p = entry2.get()
    main_face()


# QQ登录界面
def qq_loginface():
    login.destroy()
    qq = Tk()
    qq.title("QQ登录")
    qq.geometry("648x328")
    frameqq1 = Frame(qq)
    frameqq2 = Frame(qq)
    frameqq3 = Frame(qq)
    l1 = Label(frameqq1, text="QQ账号：")
    l1.pack(side=LEFT)
    l2 = Label(frameqq2, text="授权码：")
    l2.pack(side=LEFT)
    e1 = Entry(frameqq1, bd=5, )
    e1.pack(side=LEFT)
    e2 = Entry(frameqq2, bd=5, textvariable=str)
    e2.pack(side=LEFT)
    qqlog = Button(frameqq3, text="登录", command=lambda: get_entry(e1, e2))
    frameqq1.pack(padx=10, pady=40)
    frameqq2.pack(padx=10, pady=10)
    frameqq3.pack(padx=10, pady=10)
    qqlog.pack(pady=10, ipadx=5)
    qq.mainloop()


# 其他登录方式界面（其他网站未编写）
def other_loginface():
    login.destroy()
    otherlog = Tk()
    otherlog.title("其他登录")
    otherlog.geometry("648x328")
    frameqt1 = Frame(otherlog)
    frameqt2 = Frame(otherlog)
    frameqt3 = Frame(otherlog)
    l1 = Label(frameqt1, text="账号")
    l1.pack(side=LEFT)
    l2 = Label(frameqt2, text="密码")
    l2.pack(side=LEFT)
    l3 = Label(frameqt3, text="网站")
    l3.pack(side=LEFT)
    e1 = Entry(frameqt1, bd=5)
    e1.pack(side=LEFT)
    e2 = Entry(frameqt2, bd=5)
    e2.pack(side=LEFT)
    e3 = Entry(frameqt3, bd=5)
    e3.pack(side=LEFT)
    otherlogin_1 = Button(otherlog, text="登录")
    frameqt1.pack(padx=10, pady=10)
    frameqt2.pack(padx=10, pady=10)
    frameqt3.pack(padx=10, pady=10)
    otherlogin_1.pack(pady=10)
    otherlog.mainloop()


# 登录选择界面
login = Tk()
login.title("邮件客户端登录")
login.geometry("648x328")
qqlogin = Button(login, text="QQ登录", command=qq_loginface)
other = Button(login, text="其他登录方式", command=other_loginface)
qqlogin.pack(padx=10, pady=50, ipadx=5)
other.pack(padx=10, pady=10, ipadx=5)
login.mainloop()
