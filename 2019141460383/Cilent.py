

import configparser
import os
import socket
import threading



def recv(sock, addr):

    sock.sendto(name.encode('utf-8'), addr)
    while True:
        data = sock.recv(1024)
        print(data.decode('utf-8'))


        
        
def send(sock, addr):
    '''
        发送数据
            sock：定义一个实例化socket对象
            server：传递的服务器IP和端口
    '''
    while True:
        string = input('')
        message = name + ' : ' + string
        data = message.encode('utf-8')
        sock.sendto(data, addr)
        if string.lower() == 'EXIT'.lower():
            break

            
            

def main():

  
    # 通过多线程来实现多个客户端之间的通信
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    
    # 获取服务器ip和端口号
    curPath = os.path.dirname(os.path.realpath(__file__))
    cfgPath = os.path.join(curPath, "config.ini")
    conf = configparser.ConfigParser()
    conf.read(cfgPath, encoding="utf-8")

    
    ip = conf.get("test1", "local_IP")
    port = int(conf.get("test1", "port1"))

    

    server = (ip, port)

    
    tr = threading.Thread(target=recv, args=(s, server), daemon=True)
    
    ts = threading.Thread(target=send, args=(s, server))
    
    tr.start()
    
    ts.start()
    
    ts.join()
    
    s.close()

    

if __name__ == '__main__':
  
    print("-----Welcome to zChat-----")
    
    print("输入EXIT退出")
    
    name = input('Please input your name:')
    
    print('-----------------%s------------------' % name)
    
    main()
