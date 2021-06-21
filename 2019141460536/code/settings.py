# settings.py
# 默认设置

HOST = "127.0.0.1"
PORT = 5555
ADDR = HOST, PORT


def center(root, width=300, height=150):
    # 设置窗口居中
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    x = (screenWidth - width) / 2
    y = (screenHeight - height) / 2
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))