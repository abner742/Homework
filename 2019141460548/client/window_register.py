from tkinter import Toplevel
from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from tkinter import Button
from tkinter import LEFT
from tkinter import END


class WindowRegister(Toplevel):
    """注册窗口"""

    def __init__(self):
        """初始化注册窗口"""
        super(WindowRegister, self).__init__()

        # 设置窗口属性
        self.window_init()

        # 填充控件
        self.add_widgets()

    def window_init(self):
        """初始化窗口属性"""
        # 设置窗口标题
        self.title('注册窗口')

        # 设置窗口不能被拉伸
        self.resizable(False, False)

        # 获取窗口的位置变量
        window_width = 255
        window_height = 115

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        pos_x = (screen_width - window_width) / 2
        pos_y = (screen_height - window_height) / 2

        # 设置窗口大小和位置
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, pos_x, pos_y))

    def add_widgets(self):
        """添加控件到窗口里"""
        # 用户名
        username_label = Label(self)
        username_label['text'] = '用户名:'
        username_label.grid(row=0, column=0)

        username_entry = Entry(self, name='username_entry')
        username_entry['width'] = 25
        username_entry.grid(row=0, column=1)

        # 密码
        password_label = Label(self)
        password_label['text'] = '密 码:'
        password_label.grid(row=1, column=0, padx=10, pady=5)

        password_entry = Entry(self, name='password_entry')
        password_entry['show'] = '*'
        password_entry['width'] = 25
        password_entry.grid(row=1, column=1)

        # 昵称
        nickname_label = Label(self)
        nickname_label['text'] = '昵 称:'
        nickname_label.grid(row=2, column=0)

        nickname_entry = Entry(self, name='nickname_entry')
        nickname_entry['width'] = 25
        nickname_entry.grid(row=2, column=1)

        # 创建frame
        button_frame = Frame(self, name='button_frame')

        # 按钮区
        yes_bt = Button(button_frame, name='yes')
        yes_bt['text'] = ' 确认 '
        yes_bt.pack(side=LEFT)

        no_bt = Button(button_frame, name='no')
        no_bt['text'] = ' 取消 '
        no_bt.pack(side=LEFT, padx=20)

        button_frame.grid(row=3, columnspan=2, pady=5)

    def get_username(self):
        """获取用户名"""
        return self.children['username_entry'].get()

    def get_password(self):
        """获取密码"""
        return self.children['password_entry'].get()

    def get_nickname(self):
        """获取昵称"""
        return self.children['nickname_entry'].get()

    def clear_username(self):
        """清空用户名输入框"""
        self.children['username_entry'].delete(0, END)

    def clear_password(self):
        """清空密码输入框"""
        self.children['password_entry'].delete(0, END)

    def clear_nickname(self):
        """清空昵称输入框"""
        self.children['nickname_entry'].delete(0, END)

    def on_yes_button_click(self, command):
        """登录按钮的响应注册"""
        yes_bt = self.children['button_frame'].children['yes']
        # 把command函数赋值给登录按钮的command，则当点击按钮时会调用 command函数
        yes_bt['command'] = command

    def on_no_button_click(self, command):
        """重置按钮的响应注册"""
        no_bt = self.children['button_frame'].children['no']
        no_bt['command'] = command

    def on_window_closed(self, command):
        """窗口关闭事件处理方法"""
        self.protocol('WM_DELETE_WINDOW', command)
