# 因为在测试html文件时
# 将其路径指定为 "C:\webproject\index.html"

# 所以麻烦主教小哥哥如果要进行测试代码
# 请在C盘目录下创建文件夹webproject，并将html文件放进去

# 测试时，在运行该代码后（多线程Web服务器），请在浏览器键入"localhost:8000/index.html"（文字文件）
# 或者是“localhost:8000/image.html"(图片文件)

# 另外，该项目代码只象征性import了标准库中的re，socket，multiprocssing包
# 未导入第三方库
# 所以通过pipreqs生成的requiments.txt为空

import re
import socket

 
from multiprocessing import Process

 
def handle_client(client_socket):
    """处理客户端请求"""
 
    # 接收客户端请求数据(报文)
    request_data = client_socket.recv(1024)
    print("request_data:", request_data)
 
    # splitlines返回的是一个列表形式
    request_lines = request_data.splitlines()
 
    print("==" * 20)
    print(request_lines)
    print("==" * 20)
    for line in request_lines:
        print(line)
 
    # 'GET / HTTP/1.1'
    request_start_line = request_lines[0]
    print("*" * 20)
    # 用户要请求的文件名(request_start_line由byte转化成str类型)

    print(request_start_line.decode("utf-8"))
    file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode("utf-8")).group(1)
 
    if "/" == file_name:
        file_name = "/index.html"
    #针对一开始测试index.html这个文件，其实也可以测试其他html文件，该赋值不影响    
 
    # 打开文件，读取内容
    try:
        file = open("C:/webproject" + file_name,"rb")
        #文件路径为"C:\webproject\index.html"打开index.html文件


    except IOError:
        response_start_line = "HTTP/1.1 404 Not Found\r\n"
        response_headers = "Server:My server\r\n"
        response_body = "The file is not found"
    else:
        file_data = file.read()
        file.close()
 
        # 构造相应数据
        # 构建：响应行
        # 响应的起始行
        response_start_line = "HTTP/1.1 200 OK\r\n"
        # 自己伪造的服务器的响应头
        response_headers = "Server:My server\r\n"
        # 响应体
        # response_body = "hello world"
        response_body = file_data.decode("utf-8")
 
    response = response_start_line + response_headers + "\r\n" + response_body
    print("#" * 20)
    print("response data:", response)
    print("#" * 20)
 
    # 向客户端返回响应数据
    # 字符串转化成字节
    client_socket.send(bytes(response, "utf-8"))
 
    # 关闭客户端连接
    client_socket.close()
 
 
if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 可以重复地址
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 接收任何IP地址,端口号8000
    server_socket.bind(("", 8000))

    # 监听队列大小设成128(最多连接128个用户)
    server_socket.listen(128)
 
    # 采用多进程的用户监听
    while True:
        # 等待连接
        # 接收到的是客户端的socket，和客户端的地址
        client_socket, client_address = server_socket.accept()

        # 打印：第一个参数是：IP地址，第二个参数是：端口号（存在于client_address里，它本身是个元组）
        # print("[%s,%s]用户连接上" % (client_address[0], client_address[1]))
        print("[%s,%s]用户连接上" % client_address)

        # Process参数target应该接收的是函数名，args接收的应该是个元组
        handle_client_process = Process(target=handle_client, args=(client_socket,))

        # 开启进程
        handle_client_process.start()
        
        # 客户端的socket已经没有用了，关闭
        client_socket.close()
