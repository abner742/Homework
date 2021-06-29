# 改为Python3格式
from socket import *
import base64
import smtplib
import poplib
from email.parser import Parser
from email.header import decode_header,Header
from email.utils import parseaddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def print_email(msg):
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            else:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
        print('%s: %s' % (header, value))
    # 获取邮件主体信息
    attachment_files = []
    for part in msg.walk():
        # 获取附件名称类型
        file_name = part.get_filename()
        # 获取数据类型
        contentType = part.get_content_type()
        # 获取编码格式
        mycode = part.get_content_charset()
        if file_name:
            h = Header(file_name)
            # 对附件名称进行解码
            dh = decode_header(h)
            filename = dh[0][0]
            if dh[0][1]:
                # 将附件名称可读化
                filename = decode_str(str(filename, dh[0][1]))
            attachment_files.append(filename)
            # 下载附件
            data = part.get_payload(decode=True)
            # 在当前目录下创建文件
            with open(filename, 'wb') as f:
                # 保存附件
                f.write(data)
        elif contentType == 'text/plain':
            data = part.get_payload(decode=True)
            content = data.decode(mycode)
            print('正文：',content)
        elif contentType == 'text/html':
            data = part.get_payload(decode=True)
            content = data.decode(mycode)
            print('正文：', content)
    print('附件名列表：', attachment_files)

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# Choose a mail server (e.g. Google mail server) and call it mailserver
choice = input("请选择发送方的邮箱类型（qq，163，126）：")
while True:
    if choice == 'qq':
        mailserver = "smtp.qq.com"
        popserver = "pop.qq.com"
        mailUser = input("请输入您的QQ邮箱账号：")
        mailFromAddress = mailUser

        break;
    elif choice == '163':
        mailserver = "smtp.163.com"
        popserver = "pop.163.com"
        mailUser = input("请输入您的163邮箱账号：")
        mailFromAddress = mailUser

        break;
    elif choice == "126":
        mailserver = "smtp.126.com"
        popserver = "pop.126.com"
        mailUser = input("请输入您的126邮箱账号：")
        mailFromAddress = mailUser

        break;
    else:
        print("未识别此邮箱，请重新输入")

 # Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))
recv = clientSocket.recv(10240)
recv = recv.decode()

if recv[:3] != '220':
    print('连接服务器出错了！')
# Send HELO command and print server response.
heloCommand = 'HELO mailserver\r\n'
while True:
    clientSocket.send(heloCommand.encode())
    recv = clientSocket.recv(10240)
    recv = recv.decode()
    print("连接服务器成功！")
    if recv[:3] == '250':
        break

mailPassWord = input("请输入密码（发送端邮箱授权码）：")
while True:
    # 登录过程
    loginCommand = 'auth login\r\n'
    while True:
        clientSocket.send(loginCommand.encode())
        recv = clientSocket.recv(10240)
        recv = recv.decode()
       # print(recv)
        if recv[:3] == '334':
            break

    # 邮箱账户经过base64编码
    userCommand = base64.b64encode(mailUser.encode()) + b'\r\n'
    while True:
        clientSocket.send(userCommand)
        recv = clientSocket.recv(10240)
        recv = recv.decode()
        #print(recv)
        if recv[:3] == '334':
            break
    # 邮箱密码经过base64编码 这里不展示密码了
    passCommand = base64.b64encode(mailPassWord.encode()) + b'\r\n'

    clientSocket.send(passCommand)
    recv = clientSocket.recv(10240)
    recv = recv.decode()
#    print(recv)
    if recv[:3] == '235':
        print("登陆成功！")
        break
    else:
        print("登录失败！请重新输入")
        mailPassWord = input("请输入密码（发送端邮箱授权码）：")

while True:
    choice = input("请选择您需要的服务：（发送邮件、查看邮箱、退出程序）")
    if choice=="发送邮件":
        mailToAddress = input("请输入收件人邮箱地址：")
        subject = input("请输入邮件主题：")
        content = input("请输入邮件内容：")
        doAttach = input("请问是否需要添加附件:(是、否)")
        while True:
            if doAttach == "否" :
                msg = 'FROM: ' + mailFromAddress + '\r\n'
                msg += 'TO: ' + mailToAddress + '\r\n'
                msg += 'Subject: ' + subject + '\r\n'
                msg += content
                endmsg = "\r\n.\r\n"
                print(msg)



                # Send MAIL FROM command and print server response.
                MFCommand = 'MAIL FROM: <' + mailFromAddress + '>\r\n'
                while True:
                    clientSocket.send(MFCommand.encode())
                    recv = clientSocket.recv(10240)
                    recv = recv.decode()
                    #print(recv)
                    if recv[:3] == '250':
                        break

                # Send RCPT TO command and print server response.
                RTCommand = 'RCPT TO: <' + mailToAddress + '>\r\n'
                while True:
                    clientSocket.send(RTCommand.encode())
                    recv = clientSocket.recv(10240)
                    recv = recv.decode()
                   # print(recv)
                    if recv[:3] == '250':
                        break

                # Send DATA command and print server response.
                DATACommand = 'DATA\r\n'
                while True:
                    clientSocket.send(DATACommand.encode())
                    recv = clientSocket.recv(10240)
                    recv = recv.decode()
                    #print(recv)
                    if recv[:3] == '354':
                        break

                # Send message data.
                clientSocket.send(msg.encode())

                # Message ends with a single period.
                while True:
                    clientSocket.send(endmsg.encode())
                    recv = clientSocket.recv(10240)
                    recv = recv.decode()
                    #print(recv)
                    print("发送成功！")
                    if recv[:3] == '250':
                        break


                break
            elif doAttach == "是":

                msgRoot = MIMEMultipart('related')
                msgRoot['Subject'] = subject
                msgRoot['From'] = mailUser
                msgRoot['To'] = mailToAddress
                message = MIMEText(content, "plain", "utf-8")
                msgAtv = MIMEMultipart('alternative')
                msgRoot.attach(msgAtv)
                msgRoot.attach(message)
                while True:
                    type = input("请输入附件类型:(txt,img,html)")
                    # txt
                    if type=="img":
                    #img
                        url = input("请输入文件路径（绝对路径与非绝对路径皆可）")
                        f = open(url, 'rb')
                        msgImage = MIMEImage(f.read())
                        f.close()
                        msgImage.add_header('Content-ID', '<image>')
                        msgRoot.attach(msgImage)
                        again = input("继续添加附件吗？（是/否）")
                        if again == "是":
                            continue
                        else:
                            break
                    # txt
                    elif type=="txt":
                        url = input("请输入文件路径：")
                        name = input("请输入文件名：")
                        annex = MIMEText(open(url, 'rb').read(), 'base64', 'utf-8')
                        annex['Content-Type'] = 'application/octet-stream'
                        annex['Content-Disposition'] = 'attachment; filename='+name
                        msgRoot.attach(annex)
                        again = input("继续添加附件吗？（是/否）")
                        if again == "是":
                            continue
                        else:
                            break
                    elif type=="html":
                        url = input("请输入文件路径")
                        html = MIMEText(open(url, 'rb').read(), 'html', 'utf-8')
                        msgRoot.attach(html)
                        again = input("继续添加附件吗？（是/否）")
                        if again == "是":
                            continue
                        else:
                            break
                    else:
                        print("不可识别文件类型，请重新输入！")
                try:
                    server = smtplib.SMTP_SSL(mailserver, smtplib.SMTP_SSL_PORT)
                    print('成功连接到邮件服务器')
                    server.login(mailUser, mailPassWord)
                    print('成功登录邮箱')
                    server.sendmail(mailUser, mailToAddress, msgRoot.as_string())
                    print('邮件发送成功')
                except smtplib.SMTPException as e:
                    print('邮件发送异常')
                break;
            else:
                print("您输入有误！请重新输入")

    elif choice=="查看邮箱":
        server = poplib.POP3_SSL(popserver,995)
        #身份认证
        server.user(mailUser)
        server.pass_(mailPassWord)
        #start()返回邮件数量和占用空间
        print('邮件数量:%s  占用空间:%s' % server.stat())
        # list() 返回所有邮件的编号，lines 存储了邮件的原始文本的每一行
        resp, mails, octets = server.list()
        index = len(mails)
        # 获取最新一封邮件
        while True:
            index = input("请输入邮件编号进行查看：(编号范围在所有邮件数量范围之内)")
            resp, lines, octets = server.retr(index)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            # 解析邮件
            msg = Parser().parsestr(msg_content)
            print_email(msg)
            again = input("继续查看其他邮件？（是\否）")
            if again=="是":
                continue
            else:
                break

    elif choice=="退出程序":
        print("感谢您的使用")
        exit(0)
