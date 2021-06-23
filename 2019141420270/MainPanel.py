from tkinter import *
import time


# 主界面类
class MainPanel:

    def __init__(self, username, send_func, close_callback):
        self.username = username
        self.friend_list = None
        self.message_text = None
        self.send_text = None
        self.send_func = send_func
        self.close_callback = close_callback
        self.main_frame = None

    def show(self):
        global main_frame
        main_frame = Tk()
        main_frame.title("SCU聊天室")
        main_frame.configure(background="#f2f2f2")
        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        main_frame.protocol("WM_DELETE_WINDOW", self.close_callback)
        width = 800
        height = 600
        screen_width = main_frame.winfo_screenwidth()
        screen_height = main_frame.winfo_screenheight()
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        main_frame.geometry(gm_str)
        # 设置最小尺寸
        main_frame.minsize(width, height)
        Label(main_frame, text="welcome：" + self.username+"          输入 #!(你想要私聊的人)!# 加上消息内容就可以私聊哦 注意半角符号", font=("黑体", 13), bg="#f2f2f2",
              fg="#003366").grid(row=0, column=0, ipady=10, padx=10, columnspan=2, sticky=W)
        
        friend_list_var = StringVar()
        self.friend_list = Listbox(main_frame, selectmode=NO, listvariable=friend_list_var,
                                   bg="white", fg="#003366", font=("黑体", 14), highlightcolor="#9933ff")
        self.friend_list.grid(row=1, column=0, rowspan=3, sticky=N + S, padx=10, pady=(0, 5))
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(1, weight=1)
        sc_bar = Scrollbar(main_frame)
        sc_bar.grid(row=1, column=0, sticky=N + S + E, rowspan=3, pady=(0, 5))
        sc_bar['command'] = self.friend_list.yview
        self.friend_list['yscrollcommand'] = sc_bar.set
        msg_sc_bar = Scrollbar(main_frame)
        msg_sc_bar.grid(row=1, column=1, sticky=E + N + S, padx=(0, 10))
        self.message_text = Text(main_frame, bg="white", height=1,
                                 highlightcolor="white", highlightthickness=1)
        
        # 显示消息的文本框不可编辑，当需要修改内容时再修改版为可以编辑模式 NORMAL
        self.message_text.config(state=DISABLED)
        self.message_text.tag_configure('greencolor', foreground='green')
        self.message_text.tag_configure('bluecolor', foreground='blue')
        self.message_text.grid(row=1, column=1, sticky=W + E + N + S, padx=(10, 30))
        msg_sc_bar["command"] = self.message_text.yview
        self.message_text["yscrollcommand"] = msg_sc_bar.set
        send_sc_bar = Scrollbar(main_frame)
        send_sc_bar.grid(row=2, column=1, sticky=E + N + S, padx=(0, 10), pady=10)
        self.send_text = Text(main_frame, bg="white", height=11, highlightcolor="white",
                              highlightbackground="#cc99ff", highlightthickness=3)
        
        self.send_text.see(END)
        self.send_text.grid(row=2, column=1, sticky=W + E + N + S, padx=(10, 30), pady=10)
        send_sc_bar["command"] = self.send_text.yview
        self.send_text["yscrollcommand"] = send_sc_bar.set
        Button(main_frame, text="发送", bg="#4d88ff", font=("黑体", 14), fg="white", command=self.send_func) \
            .grid(row=3, column=1, pady=5, padx=10, sticky=W, ipady=3, ipadx=10)
        Button(main_frame, text="清空", bg="#4d88ff", font=("黑体", 14), fg="white", command=self.clear_send_text) \
            .grid(row=3, column=1, pady=5, sticky=W, padx=(110, 0), ipady=3, ipadx=10)
        self.main_frame = main_frame
        main_frame.mainloop()

    # 刷新在线列表
    def refresh_friends(self, names):
        self.friend_list.delete(0, END)
        for name in names:
            self.friend_list.insert(0, name)

    # 接受到消息，在文本框中显示，自己的消息用绿色，别人的消息用蓝色
    def recv_message(self, user, content):
        self.message_text.config(state=NORMAL)
        title = user + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
        if user == self.username:
            self.message_text.insert(END, title, 'greencolor')
        else:
            self.message_text.insert(END, title, 'bluecolor')
        self.message_text.insert(END, content + "\n")
        self.message_text.config(state=DISABLED)
        # 滚动到最底部
        self.message_text.see(END)

    # 清空消息输入框
    def clear_send_text(self):
        self.send_text.delete('0.0', END)

    # 获取消息输入框内容
    def get_send_text(self):
        return self.send_text.get('0.0', END)
