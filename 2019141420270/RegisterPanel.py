from tkinter import *


# 注册界面类
class RegisterPanel:

    def __init__(self, quit_func, reg_func, close_callback):
        self.reg_frame = None
        self.btn_reg = None
        self.btn_quit = None
        self.user = None
        self.key = None
        self.confirm = None
        self.quit_func = quit_func
        self.reg_func = reg_func
        self.close_callback = close_callback

    def show(self):
        self.reg_frame = Tk()
        self.reg_frame.configure(background="#f2f2f2")
        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        self.reg_frame.protocol("WM_DELETE_WINDOW", self.close_callback)
        screen_width = self.reg_frame.winfo_screenwidth()
        screen_height = self.reg_frame.winfo_screenheight()
        width = 400
        height = 320
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        self.reg_frame.geometry(gm_str)
        self.reg_frame.title("注册")
        self.reg_frame.resizable(width=False, height=False)

        title_lable = Label(self.reg_frame, text="SCU聊天室 - 注册", font=("黑体", 16),
                            fg="white", bg="#80aaff")
        title_lable.pack(ipady=10, fill=X)

        # 注册表单frame
        form_frame = Frame(self.reg_frame, bg="#f2f2f2")
        Label(form_frame, text="用户名：", font=("黑体", 12), bg="#f2f2f2", fg="#003366") \
            .grid(row=0, column=1, pady=20)
        Label(form_frame, text="密码(必须包含英文)：", font=("黑体", 12), bg="#f2f2f2", fg="#003366") \
            .grid(row=1, column=1, pady=20)
        Label(form_frame, text="确认密码：", font=("黑体", 12), bg="#f2f2f2", fg="#003366") \
            .grid(row=2, column=1, pady=20)
        self.user = StringVar()
        self.key = StringVar()
        self.confirm = StringVar()
        Entry(form_frame, textvariable=self.user, bg="#e3e3e3", width=30) \
            .grid(row=0, column=2, ipady=1)
        Entry(form_frame, textvariable=self.key, show="*", bg="#e3e3e3", width=30) \
            .grid(row=1, column=2, ipady=1)
        Entry(form_frame, textvariable=self.confirm, show="*", bg="#e3e3e3", width=30) \
            .grid(row=2, column=2, ipady=1)
        form_frame.pack(fill=X, padx=20, pady=10)
        # 按钮frame
        btn_frame = Frame(self.reg_frame, bg="#f2f2f2")
        self.btn_quit = Button(btn_frame, text="取消", bg="#4d88ff", fg="white", width=15,
                               font=('黑体', 11), command=self.quit_func).pack(side=LEFT, ipady=3)
        self.btn_reg = Button(btn_frame, text="注册", bg="#4d88ff", fg="white", width=15,
                              font=('黑体', 11), command=self.reg_func).pack(side=RIGHT, ipady=3)
        btn_frame.pack(fill=X, padx=20, pady=20)
        self.reg_frame.mainloop()

    def close(self):
        if self.reg_frame == None:
            print("no interface error")
        else:
            self.reg_frame.destroy()

    # 获取输入的用户名、密码、确认密码
    def get_input(self):
        return self.user.get(), self.key.get(), self.confirm.get()
