from email.mime.text import MIMEText#专门发送正文
from email.mime.multipart import MIMEMultipart#发送多个部分
from email.mime.application import MIMEApplication#发送附件
from email.mime.base import MIMEBase
import smtplib#发送邮件
from email import encoders
import tkinter as tk

file = 'D:\\neywork.txt' #附件路径
file1 = 'D:\\neywork.txt' #附件路径
 
send_user = '62***8416@qq.com'   #发件人
password = 'eip***bga'   #授权码/密码
receive_users = '22****177@qq.com'   #收件人，可为list
subject = 'For you'  #邮件主题
email_text = 'my client'   #邮件正文
server_address = 'smtp.qq.com'   #服务器地址
mail_type = '1'    #邮件类型
 
#构造一个邮件体：正文 附件
msg = MIMEMultipart()
msg['Subject']=subject    #主题
msg['From']=send_user      #发件人
msg['To']=receive_users      #收件人
 
#构建正文
part_text=MIMEText(email_text)
msg.attach(part_text)             #把正文加到邮件体里面去
 
#构建邮件附件
#file = file           #获取文件路径
part_attach1 = MIMEApplication(open(file,'rb').read())   #打开附件
part_attach1.add_header('Content-Disposition','attachment',filename=file) #为附件命名
msg.attach(part_attach1)   #添加附件
 
 
with open('D:\\neywork.jpg', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'jpg', filename='tp.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='tp.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
 
#正文显示附件图片
msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))
 
# 发送邮件 SMTP
smtp= smtplib.SMTP(server_address, 25)  # 连接服务器，SMTP_SSL是安全传输
print('连接成功！')
smtp.login(send_user, password)
print('登录成功！')
smtp.sendmail(send_user, receive_users, msg.as_string())  # 发送邮件
print('邮件发送成功！')