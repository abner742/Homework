
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sendmail as s

def client():

    global file

    top = tk.Tk()
    top.title("邮件发送客户端")
    top.geometry('600x520')

    # 背景图
    im = Image.open("image.jpg")
    img = ImageTk.PhotoImage(im)
    imLabel = tk.Label(top, image=img).pack()


    # 发送人
    tk.Label(top, text="发送人:", font="幼圆", width=10, height=1).place(x=30, y=30)
    tk.Label(top, text="1040938622<1040938622@qq.com>", width=40, height=1).place(x=170, y=30)

    # 接收人
    tk.Label(top, text="接收人:",  font="幼圆", width=10, height=1).place(x=30, y=70)
    receiver_entry = tk.Entry(top, width=40)
    receiver_entry.place(x=170, y=70)

    # 主题
    tk.Label(top, text="主题:",  font="幼圆", width=10, height=1).place(x=30, y=110)
    subject_entry = tk.Entry(top,  width=40)
    subject_entry.place(x=170, y=110)

    # 添加文件
    tk.Label(top, text="文件路径:", font="幼圆", width=10, height=1).place(x=30, y=150)
    file_path = tk.Entry(top, width=40)
    file_path.place(x=170, y=150)

    # 复选框选择邮件类型
    tk.Label(top, text="邮件类型:", font="幼圆", width=10, height=1).place(x=30, y=190)
    CheckVar1 = tk.IntVar()
    CheckVar2 = tk.IntVar()
    C1 = tk.Checkbutton(top, text="纯文本", variable=CheckVar1)
    C2 = tk.Checkbutton(top, text="带附件", variable=CheckVar2)
    C1.place(x=170, y=190)
    C2.place(x=250, y=190)

    # 内容
    content_text = tk.Text(top, width=60, height=20)
    content_text.place(x=30, y=230)

    # 清除函数
    def clearcontent():
        content_text.delete('0.0', 'end')

    # 上传文件函数
    def upload_file():
        selectFile = tk.filedialog.askopenfilename()
        file_path.insert(0,selectFile)

    # 发送函数
    def send():
        receiver = receiver_entry.get()
        subject = subject_entry.get()
        content = content_text.get('0.0', 'end')
        file = file_path.get()
        
        # 判断接收人邮箱格式
        if "@" in receiver:
            try:
                typetext = CheckVar1.get()
                typeacc = CheckVar2.get()
                if typetext == 1:
                    s.sendtextmail(receiver, subject, content)
                    tk.messagebox.showinfo('提示', '邮件已发送')
                    print("邮件已发送")
                if typeacc == 1:
                    s.sendaccmail(receiver, subject, content, file)
                    tk.messagebox.showinfo('提示', '邮件已发送')
                    print("邮件已发送")
                if typetext == 0 and typeacc == 0:
                    tk.messagebox.showinfo('提示', '请选择邮件类型')
            except IOError:
                tk.messagebox.showinfo('提示', '邮件发送失败')
                print("发送失败")
        else:
            tk.messagebox.showinfo('提示', '邮箱格式不对\n请确认接收人邮箱')
            print("邮箱格式不对\n请确认接收人邮箱")

    '''按钮'''
    im1 = Image.open("发送.png")
    im1 = im1.resize((30, 30))
    img1 = ImageTk.PhotoImage(im1)

    im2 = Image.open("删除.png")
    im2 = im2.resize((28, 28))
    img2 = ImageTk.PhotoImage(im2)

    im3 = Image.open("attachment.png")
    im3 = im3.resize((20, 20))
    img3 = ImageTk.PhotoImage(im3)

    b1 = tk.Button(top, text='添加附件',  image=img3, width=80, height=20, compound="left",  command=upload_file)
    b1.place(x=330, y=190)
    b2 = tk.Button(top, text="清空", bd=3, font="幼圆", image=img2, width=110, height=30, compound="left", command=clearcontent)
    b2.place(x=470, y=400)
    b3 = tk.Button(top, text="发送", bd=3, font="幼圆", image=img1, width=110, height=30, compound="left", command=send)
    b3.place(x=470, y=455)

    top.mainloop()

if __name__ == '__main__':
    client()


