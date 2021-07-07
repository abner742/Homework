
from socket import *
import threading
import os
def Server(tcpClisock, addr):
    BUFSIZE = 1024
    print('connected from:', addr)
    rec = tcpClisock.recv(BUFSIZE)
    data = rec.decode()
    if len(data) == 0:
        tcpClisock.close()
        return
    HOME_DIR = os.getcwd()
    print("***************************************************\n")
    index = 4
    while data[index] != ' ':
        index += 1
    if index == 5:
        direction = os.path.join(HOME_DIR, "Success.html")
    else:
        direction = os.path.join(HOME_DIR, data[5: index])
    if os.path.exists(direction) and direction.endswith(".html"):
        file = open(direction)
        SUCCESS_PAGE = "HTTP/1.1 200 OK\r\n\r\n" + file.read()
        print(SUCCESS_PAGE)
        tcpClisock.sendall(SUCCESS_PAGE.encode())
        tcpClisock.close()
    else:
        FAIL_PAGE = "HTTP/1.1 404 NotFound\r\n\r\n" + open(os.path.join(HOME_DIR, "Fail.html")).read()
        print(FAIL_PAGE)
        tcpClisock.sendall(FAIL_PAGE.encode())
        tcpClisock.close()
if __name__ == '__main__':
    HOST = ""
    PORT = 4004
    ADDR = (HOST, PORT)
    tcpSersock = socket(AF_INET, SOCK_STREAM)
    tcpSersock.bind(ADDR)
    tcpSersock.listen(5)
    print("waiting for connection......\n")
    while True:
        tcpClisock, addr = tcpSersock.accept()
        thread = threading.Thread(target=Server, args=(tcpClisock, addr))
        thread.start()
    tcpSersock.close()
