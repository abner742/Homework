import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "1040938622@qq.com"  # 用户名
mail_pass = "rwxucpxrvlykbdid"  # 授权码
me = "1040938622" + "<" + "1040938622@qq.com" + ">"

# 发送纯文本邮件
def sendtextmail(mail_receiver, mail_subject, mail_content):

    msg = MIMEMultipart()
    msg['Subject'] = mail_subject
    msg['From'] = me
    msg['To'] = ";".join(mail_receiver)

    # 文字部分
    part = MIMEText(mail_content, 'plain', 'utf-8')
    msg.attach(part)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(me, mail_receiver, msg.as_string())
        smtpObj.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# 发送带有附件的邮件
def sendaccmail(mail_receiver, mail_subject, mail_content,filepath):

    msg = MIMEMultipart()
    msg['Subject'] = mail_subject
    msg['From'] = me
    msg['To'] = ";".join(mail_receiver)

    # 文字部分
    part = MIMEText(mail_content, 'plain', 'utf-8')
    msg.attach(part)

    # 附件部分
    part = MIMEApplication(open(filepath, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=filepath)
    msg.attach(part)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(me, mail_receiver, msg.as_string())
        smtpObj.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")