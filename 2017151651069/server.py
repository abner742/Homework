# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 18:24:45 2021

@author: liqian
"""

import sys
import socket
import select
import pickle
import socket
import struct
import time

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9090
activeUsers = {}
listActive = []
returningUsers = {"user1": "1234", "user2": "1234", "user3": "1234", "user4": "1234"} #模拟旧用户，"用户名":"密码"
activeSessions = {}
new = {}

'''
Function to find data between two characters:
'''
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

'''
Server Function:
''' 
def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#select函数阻塞进程，直到inputs中的套接字被触发（在此例中，套接字接收到客户端发来的握手信号，从而变得可读，满足select函数的“可读”条件），rs返回被触发的套接字（服务器套接字）
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    SOCKET_LIST.append(server_socket)
 
    print ("Chat server started on port " + str(PORT))
    activeSessions = {}
    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)  
        for sock in ready_to_read:
            # 新的用户发起登录请求...
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                sockfd.send("connection")
                time.sleep(1)
                sockfd.send("Enter N, If you are a new user or R, If you are a returning user\n")
                # 判断是新用户还是老用户...
                ans = sockfd.recv(RECV_BUFFER)
                # print(ans) debug时用
                # 如果是老用户...
                if  str(ans)== 'R':
                    username = sockfd.recv(RECV_BUFFER)
                    username = username.strip()
                    if username in activeUsers:
                        sockfd.send("False")
                    else:
                        if username in returningUsers:
                            sockfd.send("True")
                            for i in range(0,4):
                                password = sockfd.recv(RECV_BUFFER)
                                password = password.strip()
                                if(returningUsers[username] == password):
                                    sockfd.send("True")
                                    SOCKET_LIST.append(sockfd)
                                    print("Client (%s, %s) connected to server" % addr)
                                    add = sockfd.recv(RECV_BUFFER)
                                    print("Listening port assigned is "+add) 
                                    activeUsers[username] = add
                                    break
                                else:
                                    sockfd.send("False")
                                    print("Incorrect Password Entered")
                        else:
                            sockfd.send("False")
                # 如果是新用户...
                else:
                    while(1):
                        username = sockfd.recv(RECV_BUFFER)
                        if username in activeUsers:
                            sockfd.send("False")
                        elif username in returningUsers:
                            sockfd.send("False")
                        else:
                            sockfd.send("True")
                            password = sockfd.recv(RECV_BUFFER)
                            returningUsers[username] = password 
                            SOCKET_LIST.append(sockfd)
                            print("Client (%s, %s) connected to server" % addr)
                            add = sockfd.recv(RECV_BUFFER)
                            print("Listening port assigned is "+add )
                            activeUsers[username] = add
                            break        
                
            # 登陆后处理用户请求...
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                    # 请求在线用户列表...
                        if "GET_CLIENT_LIST" in data:
                            print("Received GET_CLIENT_LIST request")
                            for key in activeUsers :
                                listActive.append(key)
                            str1 = ', '.join(listActive)
                            if not listActive:
                                sock.send("No other user is connected")
                            else:	
                                str1 = "CLIENT_LIST<"+str1+">\n"
                                sock.send(str1)
                            del listActive[:]
                    # 请求连接在线用户...
                        elif "GET_CLIENT_INFO" in data:
                            print("Received GET_CLIENT_INFO request")
                            data = find_between(data, "<", ">")
                            #print data，debug时用
                            if data == '':
                                sock.send("Please enter the username in your request\n")
                            else:
                                if data in activeUsers:
                                    #print msg 
                                    if data in activeSessions:
                                        sock.send("Requested user is in the session\n")
                                    else:
                                        str1 = str(activeUsers[data])
                                        str1 = "CLIENT_INFO <"+str1+">" 
                                        sock.send(str1)
            	                        #print str1，debug时用
                                        m = sock.recv(RECV_BUFFER)
                                        k = m.split(':')
                                        activeSessions[k[0]]= k[1]
                                        #print msg					
                                else:
                                    sock.send("Requested user is not available\n")
            	        # 断开连接请求...
                        elif "DISCONNECT_CLIENT" in data:
                            data = find_between(data, "<", ">")
                            del activeUsers[data]
                            SOCKET_LIST.remove(sock)
                        # 退出登录...
                        elif "SESSION_END_NOTIFICATION" in data:
                            data = find_between(data, "<", ">")
                            #print "HI "+data
                            for key, value in activeSessions.iteritems() :
                	#print key
                                if data == key:
                                    print( '')
                                elif data == value:
                                    print( '')
                                else:
                                    new[key] = value
        	            #print new
                            activeSessions = new
            				#print activeSessions
            				#activeSessions = [v for v in activeSessions]
            				#activeSessions = [ v for v in activeSessions if not any(data in s for s in activeSessions)]
                        else:
                            sock.send("Unknown Request")
                    else:
                            # 从socket列表中移除关闭的socket   
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                except IOError as e:
                    print(e)
                    continue

    server_socket.close()
    

if __name__ == "__main__":
    sys.exit(chat_server())         
