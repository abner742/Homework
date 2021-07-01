#coding:utf-8
import socket
import re
from multiprocessing import Process

#设置静态文件根目录
HTML_ROOT_DIR="./files"

def handle_client(client_socket):
    """处理客户端请求"""

    #获取客户端请求数据
    request_data=client_socket.recv(1024)
    print(request_data)
    request_lines=request_data.splitlines()
    for line in request_lines:
        print(line)

    #解析请求报文
    request_start_line=request_lines[0]
    print("********",bytes.decode(request_start_line))
    #提取用户请求的文件名
    request_start_line=bytes.decode(request_start_line)
    file_name=re.match(r"\w+ +(/[^ ]*) ",request_start_line).group(1)
    print(file_name)

    if "/"== file_name:
        file_name= "/index.html"

    #打开文件，读取内容
    try:
        file=open(HTML_ROOT_DIR+file_name,"rb")
    except IOError:
        response_start_line="HTTP/1.1 404 Not Found\r\n"
        response_headers="Server:My server\r\n"
        response_body="The file is not found!"
    else:
        file_data=file.read()
        file.close()
        #构造响应数据
        response_start_line="HTTP/1.1 200 OK\r\n"
        response_headers="Server:My server\r\n"
        response_body=bytes.decode(file_data)

    response=response_start_line+response_headers+ "\r\n"+response_body
    print("response data:",response)

    #向客户端返回响应数据
    client_socket.send(bytes(response,"utf-8"))

    #关闭客户端连接
    client_socket.close()


if __name__ == "__main__":
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)   
    server_socket.bind(("",8000))
    server_socket.listen(128)

    while True:
        client_socket,client_address=server_socket.accept()
        print("[%s,%s]用户连接上" % client_address)
        handle_client_process=Process(target=handle_client,args=(client_socket,))
        handle_client_process.start()
        client_socket.close()

# def fun(cli_socket):
#     #接收数据
#     #request_data=recv()
#     #print(request_data)
#     #解析HTTP报文数据
#     #提取请求路径path
#         HTML_ROOT_DIR="./files"(根目录)
#         path=/index.html
#         try:
#             file=open("index.html")
#         data=file.read()
#         file.close()
#         except IOError:
    
#     HTTP1.1 404 Not Found\r\n
#     \r\n
#     not found



#     #返回响应数据
#     #HTTP1.1 200 OK\r\n
#     #\r\n
#     #send()
#     #close()
