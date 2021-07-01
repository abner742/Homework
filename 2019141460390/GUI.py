from email.mime.text import MIMEText#专门发送正文
from email.mime.multipart import MIMEMultipart#发送多个部分
from email.mime.application import MIMEApplication#发送附件
from email.mime.base import MIMEBase
import smtplib#发送邮件
from email import encoders
import tkinter as tk

send_user = ''   #发件人
password = ''   #授权码/密码
receive_users = ''   #收件人，可为list
subject = ''  #邮件主题
email_text = ''   #邮件正文
server_address = 'smtp.qq.com'   #服务器地址
mail_type = '1'    #邮件类型

file = 'D:\\neywork.txt' #附件路径
file1 = 'D:\\neywork.txt' #附件路径

window = tk.Tk()#定义一个窗口
window.title('my qq email client')
window.geometry('500x500')##窗口尺寸

smtp= smtplib.SMTP(server_address, 25) # 连接服务器，SMTP_SSL是安全传输

msg = MIMEMultipart()#构造一个邮件体：正文 附件

# 标签1
l1 = tk.Label(window, 
    text='输入邮箱',    # 标签1的文字
    bg='green',     # 标签背景颜色
    font=('Arial', 12),     # 字体和字体大小
    width=15, height=2  # 标签长宽
    )
l1.pack()    # 固定窗口位置
e1=tk.Entry(window,show=None)#输入用户
e1.pack()

 # 标签2
l2 = tk.Label(window,   
    text='输入授权码',   
    bg='green',     
    font=('Arial', 12),     
    width=15, height=2  
    )
l2.pack()    
e2=tk.Entry(window,show=None)
e2.pack()

var=tk.StringVar()#定义一个字符串变量
# 标签3
l = tk.Label(window,         
    textvariable=var,    
    bg='green',     
    font=('Arial', 12),    
    width=15, height=2  
    )
l.pack()   

def Login():
    smtp.login(send_user, password)#登录
    var.set('登录成功！')#显示登录成功！

#定义按钮功能
def insert_send_user_password():
    global send_user
    global password
    global msg
    send_user=e1.get() 
    password=e2.get()
    msg['From']=send_user      #发件人
    

b1 = tk.Button(window,text="确定",command=lambda:[insert_send_user_password(), Login()]) 
b1.pack() 

# 标签3
l3 = tk.Label(window,     
    text='输入收件人',   
    bg='green',     
    font=('Arial', 12),   
    width=15, height=2  
    )
l3.pack() 
e3=tk.Entry(window,show=None)
e3.pack()
def insert_receive_users():
    global receive_users
    global msg   
    receive_users = e3.get()
    msg['To']=receive_users      #收件人  
        

# 标签4
l4 = tk.Label(window,     
    text='输入主题',    
    bg='green',    
    font=('Arial', 12),     
    width=15, height=2  
    )
l4.pack()    
e4=tk.Entry(window,show=None)
e4.pack()
def insert_subject():  
    global subject  
    subject = e4.get() 
    msg['Subject']=subject   
 
 # 标签5
l5 = tk.Label(window,     
    text='输入正文',    
    bg='green',     
    font=('Arial', 12),    
    width=15, height=2 
    )
l5.pack()    
e5=tk.Entry(window,show=None)
e5.pack()
def insert_email_text(): 
    global email_text
    global msg   
    email_text = e5.get()     
    #构建正文
    part_text=MIMEText(email_text)
    msg.attach(part_text)             #把正文加到邮件体里面去

def send():   
    smtp.sendmail(send_user, receive_users, msg.as_string())  # 发送邮件
    print('邮件发送成功！')
    var.set('登录成功！')


b2 = tk.Button(window,text="发送",command=lambda:[insert_receive_users(),insert_subject(),insert_email_text(), send()]) 
b2.pack() 

window.mainloop()





 

