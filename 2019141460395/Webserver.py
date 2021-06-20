import re
import socket
import threading

def service_client(new_socket):
    """为这个客户端返回数据"""
    #1.接受浏览器发送过来的请求，即http请求
    #GET/HTTP/1.1
    #...
    request = new_socket.recv(1024).decode("utf-8")
    # print(request)
    request_linse = request.splitlines()

    #GET (提取出:index.html file_name)
    file_name = ""
    ret = re.match(r"[^/]+(/)+([^ ]*)",request_linse[0])
    if ret:
        file_name = ret.group(2)

    try:
        f = open(file_name,"rb")
    except:
        response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
        response += "-------file not found-----"
        new_socket.send(response.encode("utf-8"))
    else:
        # 2.返回http格式的数据给浏览器
        response = "http/1.1 200 OK\r\n\r\n"
        # 2.1准备发送给浏览器的数据---header
        # 2.2准备发送给浏览器的数据---body
        html_content = f.read()
        f.close()
        # 发送header和body
        new_socket.send(response.encode("utf-8"))
        new_socket.send(html_content)

    #3.关闭套接字
    new_socket.close()

def main():
    """用来完成整体控制"""
    #1.创建套接字

    print("创建一个新的套接字")
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #2.绑定
    tcp_server_socket.bind(("",7890))
        #3.变为监听套接字
    tcp_server_socket.listen(128)
    # 4.等待新客户端的链接
    print("server is ready to serve...")


    while True:
        new_socket, client_addr = tcp_server_socket.accept()
        # 5.为这个客户端服务(分配一个线程)
        print("分配了一个线程")
        t = threading.Thread(target=service_client,args=(new_socket,))
        print(t.name)
        t.start()


    #关闭套接字
    tcp_server_socket.close()

if __name__ == "__main__":
      main()
