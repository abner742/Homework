# coding=utf-8
import socket
import re
# 引入线程模块
import threading


def service_client(new_socket):
    """"为这个客户端返回数据"""
    # 接受浏览器发送过来的请求，即http请求
    request = new_socket.recv(1024).decode("utf-8")
    # 打印请求
    print("request:" + request)
    #
    print(new_socket)

    request_lines = request.splitlines(0)
    response = ""

    if request_lines:
        # GET /welcome.html
        # get post put del
        # print("request_lines:" + request_lines[0])
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        # print(ret)
        # print(ret.group(1))
        file_name = ""
        if ret:
            # 提取文件名
            file_name = ret.group(1)
            # 如果只输入端口号，返回主页面
            if file_name == "/":
                file_name = "/index.html"

        # 返回HTTP格式的数据，给浏览器
        # 打开文件
        try:
            f = open("./html" + file_name, "rb")
        # 文件不存在
        except:
            # 提取fail.html文件内容
            f = open("./html/fail.html", "rb")
            html_content = f.read()
            f.close()
            # 返回HTTP格式的数据，给浏览器
            # 准备发送给浏览器的数据（head）
            response = "HTTP/1.1 404 NOT FOUND\r\n"
            response += "\r\n"
            new_socket.send(response.encode("utf-8"))
            new_socket.send(html_content)

        # 文件存在
        else:
            # 提取文件内容
            html_content = f.read()
            f.close()
            # 返回HTTP格式的数据，给浏览器
            # 准备发送给浏览器的数据（head）
            response = "HTTP/1.1 200 OK\r\n"
            response += "\r\n"

            # 将response header发送给浏览器
            new_socket.send(response.encode("utf-8"))
            # 将response body发送给浏览器
            new_socket.send(html_content)
            # print(html_content)
    else:
        print("------request not exist------")

    # 关闭套接字
    new_socket.close()


def main():
    """用来完成整体的控制"""
    # 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定
    tcp_server_socket.bind(("", 7890))

    # 变为监听套接字
    tcp_server_socket.listen(128)

    while True:
        # 等待新客户端的链接
        new_socket, client_addr = tcp_server_socket.accept()

        # 为这个客户端服务
        t = threading.Thread(target=service_client, args=(new_socket,))
        t.start()

    # 关闭监听套接字
    tcp_server_socket.close()


if __name__ == "__main__":
    main()
