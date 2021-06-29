import threading# In order to terminate the program
from socket import *


def server(connectionsocket, addr):
    try:
        message = connectionsocket.recv(1024).decode()
        print('thread'+str(threading.get_ident())+'receiving a new request')
        filename = message.split()[1]
        f = open(filename[1:], 'rb')
        outputdata = f.read()
        connectionsocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        connectionsocket.send(outputdata[0:])  # .encode())
        connectionsocket.close()
    except IOError:
        connectionsocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionsocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionsocket.close()


if __name__ == '__main__':
    # Create a TCP server socket
    #(AF_INET is used for IPv4 protocols)
    #(SOCK_STREAM is used for TCP)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Assign a port number
    serverPort = 6789
    # Bind the socket to server address and server port
    serverSocket.bind(("", serverPort))
    # Listen to at most 100 connection at a time
    serverSocket.listen(100)
    # Server should be up and running and listening to the incoming connections
    while True:
        # Set up a new connection from the client
        connectionSocket, addr = serverSocket.accept()
        thread = threading.Thread(target=server, args=(connectionSocket, addr))
        thread.start()
