from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import Text
from tkinter import Button
from tkinter import END
from tkinter import UNITS
from tkinter import Listbox
from time import localtime, strftime, time


class WindowChat(Toplevel):

    def __init__(self):
        super(WindowChat, self).__init__()
        # 设置窗口大小、窗口不能修改
        self.geometry('%dx%d' % (845, 485))
        self.resizable(False, False)

        # 添加组件
        self.add_widget()

    def add_widget(self):
        """添加组件的方法"""
        # 聊天区
        chat_text_area = ScrolledText(self)
        chat_text_area['width'] = 100
        chat_text_area['height'] = 30
        chat_text_area.grid(row=0, column=0)
        chat_text_area.tag_config('green', foreground='#008B00')
        self.children['chat_text_area'] = chat_text_area

        # 在线列表
        user_list = Listbox(self)
        user_list['width'] = 15
        user_list['height'] = 20
        user_list.grid(row=0, column=1)
        self.children['user_list'] = user_list

        # 输入区
        chat_input_area = Text(self, name='chat_input_area')
        chat_input_area['width'] = 100
        chat_input_area['height'] = 5
        chat_input_area.grid(row=1, column=0, pady=10)

        # 发送
        send_button = Button(self, name='send_button')
        send_button['text'] = '发送'
        send_button['width'] = 5
        send_button['height'] = 2
        send_button.grid(row=1, column=1)

    def set_title(self, title):
        """设置标题"""
        self.title('龘龘龘聊天室：用户 %s' % title)

    def on_send_button_click(self, command):
        """注册事件，当发送按钮被点击时，执行command方法"""
        self.children['send_button']['command'] = command

    def get_input(self):
        """获取输入框内容"""
        return self.children['chat_input_area'].get(0.0, END)

    def clear_input(self):
        """清空输入框内容"""
        self.children['chat_input_area'].delete(0.0, END)

    def append_message(self, sender, message):
        """添加一条信息到聊天区"""
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        send_info = '%s: %s\n' % (sender, send_time)
        self.children['chat_text_area'].insert(END, send_info, 'green')
        self.children['chat_text_area'].insert(END, ' ' + message + '\n')

        # 向下滚动屏幕
        self.children['chat_text_area'].yview_scroll(3, UNITS)

    def on_window_closed(self, command):
        """注册关闭窗口时执行的指令"""
        self.protocol('WM_DELETE_WINDOW', command)




