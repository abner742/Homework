import smtplib
from email.mime.text import MIMEText
from tkinter import *

'''邮件和可视化界面'''

mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "2559354136@qq.com"  # 用户名
mail_pass = "jmcssetjoaatebcg"  # 授权码
me = "2559354136" + "<" + "2559354136@qq.com" + ">"

'''发送函数'''
def sendmail(mail_receiver, mail_subject, mail_content):

    msg = MIMEText(mail_content, 'plain', 'utf-8')
    msg['Subject'] = mail_subject
    msg['From'] = me
    msg['To'] = ";".join(mail_receiver)

    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(mail_user, mail_pass)
        server.sendmail(me, mail_receiver, msg.as_string())
        server.quit()
    except smtplib.SMTPException:
        print("Error: 邮件发送错误")

'''可视化界面'''
def client():

    top = Tk()
    top.title("邮件发送客户端")
    top.geometry('600x700')

    '''发送人'''
    Label(top, text="发送人:", bg="grey",font="隶书", width=10, height=1).place(x=30, y=30)
    Label(top, text="2559354136@qq.com",font="隶书",bg="white", width=20, height=1).place(x=170, y=30)

    '''接收人'''
    Label(top, text="接收人:", bg="grey",font="隶书",width=10, height=1).place(x=30,y=70)
    receiver_entry = Entry(top,width=50)
    receiver_entry.place(x=170,y=70)

    '''主题'''
    Label(top, text="主题:", bg="grey",font="隶书",width=10, height=1).place(x=30,y=110)
    subject_entry = Entry(top,  width=50)
    subject_entry.place(x=170, y=110)

    '''内容'''
    Label(top, text="内容:", bg="grey",font="隶书",width=10, height=1).place(x=30,y=150)
    content_text = Text(top,width=60,height=20)
    content_text.place(x=30,y=190)

    def clearcontent():
        content_text.delete('0.0','end')

    def send():
        receiver = receiver_entry.get()
        subject = subject_entry.get()
        content = content_text.get('0.0','end')
        if "@" in receiver:
            try:
                sendmail(receiver,subject,content)
                print("邮件已发送")
            except IOError:
                print("发送失败")
        else:
            print("邮箱格式不对\n请确认接收人邮箱")

    '''按钮'''
    Button(top,text="清空",bd=5,font="隶书",width=10,command=clearcontent).place(x=30,y=460)
    Button(top,text="发送",bd=5,font="隶书",width=10,command=send).place(x=170,y=460)

    top.mainloop()

if __name__ == '__main__':
    client()
