from socket import *
import threading
import os

'''自定义线程函数'''
def Server(tcpClisock, addr):

    BUFSIZE = 1024
    print('Waiting for the connection：', addr)
    data = tcpClisock.recv(BUFSIZE).decode()
    filename = data.split()[1]
    filename = filename[1:]

    '''当网络质量差没有收到浏览器的访问数据时执行'''
    if filename == "":
        tcpClisock.close()
        print("请输入要访问的文件")

    base_dir = os.getcwd()
    file_dir = os.path.join(base_dir,filename)

    '''当访问的文件在本地服务器存在时执行'''
    if os.path.exists(file_dir):
        f = open(file_dir,encoding = 'utf-8')
        SUCCESS_PAGE = "HTTP/1.1 200 OK\r\n\r\n" + f.read()
        print(SUCCESS_PAGE)
        tcpClisock.sendall(SUCCESS_PAGE.encode())
        tcpClisock.close()
    else:
        FAIL_PAGE = "HTTP/1.1 404 NotFound\r\n\r\n" + open(os.path.join(base_dir, "2.html"), encoding="utf-8").read()
        print(FAIL_PAGE)
        tcpClisock.sendall(FAIL_PAGE.encode())
        tcpClisock.close()

'''主函数'''
if __name__ == '__main__':

    '''分配IP、端口、创建套接字对象'''
    ADDR = ("", 8080)
    tcpSersock = socket(AF_INET, SOCK_STREAM)
    tcpSersock.bind(ADDR)
    tcpSersock.listen(5)
    print("waiting for connection......\n")
    while True:
        tcpClisock, addr = tcpSersock.accept()
        thread = threading.Thread(target=Server, args=(tcpClisock, addr))
        thread.start()
    tcpSersock.close()
          
          
<!DOCTYPE html>
<html>
<head>
    <title></title>
<meta http-equiv="content-type" content="text/html"; charset="utf-8"/>
</head>
<style type="text/css">
	div{
        font-size: x-large;
		text-align: center;
		font-family: 楷体;
		color: red;
		}
</style>
<body>
    <div>
        <br><br>
        <br><br>
        <h1 >404! 访问的路径不存在！</h1>
    </div>
</body>
</html>

<!DOCTYPE html>
<html>
<head>
	<title></title>
<meta http-equiv="content-type" content="text/html"; charset="utf-8"/>
</head>
<style type="text/css">
	div {
		text-align: center;
		font-family: 楷体;
		}
	a{
		color: red;
	}
</style>

<body>
	</br></br>
	<div>
		</br></br></br>
		<h1>欢迎来到四川大学！</a></h1>
	</div>
</body>
</html>
