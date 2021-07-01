import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
host = 'smtp.qq.com'  # 设置发件服务器地址
port = 25  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
 
#发送邮箱
sender = '62***416@qq.com'
 
#接收邮箱
receiver = ['22**47177@qq.com','62****7416@qq.com']
cc = ['22***7177@qq.com','625***416@qq.com']
 
#发送邮件主题
subject = 'Python email test'
 
#发送邮箱服务器
smtpserver = 'smtp.qq.com'
 
username = '62***416@qq.com'  #发送邮箱用户
password = 'eip*****gmu***ga'  #邮箱密码或授权码
 
#编写 text 类型的邮件正文
msg = MIMEText('<html><h1>复习了复习了！</h1></html>','html','utf-8')
msg['Subject'] = Header(subject, 'utf-8')
msg['From'] = sender
msg['To'] =','.join(receiver) 
msg['Cc'] =','.join(cc) 
print(msg['To'])
 
smtp = smtplib.SMTP()
smtp.connect('smtp.qq.com',25)
smtp.login(username, password)  # 登陆邮箱
smtp.sendmail(msg['From'], msg['To'].split(',') + msg['Cc'].split(',') , msg.as_string())  # 发送邮件！
print("邮件发送成功!")
