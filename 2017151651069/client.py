# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 17:50:48 2021

@author: liqian
"""

import sys
import socket
import select
import pickle
import struct
import random
from threading import Thread
from os import curdir, sep
import time
flag = 0
name = ''

def password(s):
	password = input("Enter Password: ")
	s.send(password)
'''
Function to find dat between two characters:
'''
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

'''
chat_client function:
''' 
def chat_client():
    if(len(sys.argv) < 3) :
        print('Usage : python client.py hostname port' )
        sys.exit()
    #name = sys.argv[1]
    host = sys.argv[1]
    port = int(sys.argv[2])
    name2 = ""
    flag = 0
    name = ""
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    cl.settimeout(2)
    r = random.randint(49152, 65535)
    add = tuple(['localhost']+[r])
    cl.bind(add) 
    cl.listen(5)
     
    # 连接server
    try :
        s.connect((host, port))
        print("WELCOME PEER-TO-PEER CHAT AND FILE SHARING SERVICE" )
        print("Please wait while service loads.......")
    except IOError as e:
        print('Unable to connect')
        print(e)
        sys.exit()

    socket_list = [sys.stdin, s, cl]
    while 1:
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:
           #连接server成功          
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from chat server' )
                    sys.exit()
                else :
                    #连接在线用户成功
                    if("CLIENT_INFO" in data):
                        data = find_between(data, "<", ">")
                        array = data.split(',')
                        host = array[0].strip().strip('(').strip("'")
                        port = array[1].strip().strip(')')
                        try:
                            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            cs.settimeout(2)
                            cs.connect((host,int(port)))
                            socket_list.append(cs)
                            s.send(name+":"+name2)
                            print("Connection established with requested client. You can start sending him messages.")
                            cs.send("You are connected to "+name+"\n")
                            flag = 1
                        except IOError as e:
                            print('Client unavailable. Kindly enter another client')
            				#print e
                    if(data == "connection"):
                        d = s.recv(4096)
                        while(1):
                            ans = raw_input(str(d))
                            if ans == 'N':
                                s.send(ans)
                                while(1):
                                    username = raw_input("Enter Username: ")
                                    name = username
                                    s.send(username)
                                    if (s.recv(4096) == "False"):
                                        print("Sorry, You can take this username" )
                                    else:
                                        time.sleep(1)	
                                        password = raw_input("Enter Password: ")
                                        s.send(password)
                                        time.sleep(1)
                                        print('You are connected to server')
                                        print('Service usage description.')
                                        print('1. Enter "GET_CLIENT_LIST" to request list of active clients.')
                                        print('2. Enter "GET_CLIENT_INFO <username>", with username of a client to connect to')
                                        print('3. CLIENT_LIST<name1, name2, ... > tells names of active clients')
                                        print('4. Enter "SEND_FILE<file path>" to send any file from respective path')
                                        print('5. Enter "CLOSE_SESSION" to stop communicating with any client')
                                        print('6. Enter "DISCONNECT_CLIENT" to disconnect from chat service')
                                        print('7. Enter "#HELP" anytime to read instructions again')
                                        s.send(str(add))
                                        break
                                break
						
                            elif ans == 'R':
                                s.send(ans)
                                username = raw_input("Enter Username: ")
                                name = username
                                s.send(username)
                                if (s.recv(4096) == "True"):
            		        #password(s), debug用
                                        password = raw_input("Enter Password: ")
                                        s.send(password)
                                        for i in range(0, 3):
                                            if (s.recv(4096) == "True"):
                                                print('You are connected to server')
                                                print('Service usage description.')
                                                print('1. Enter "GET_CLIENT_LIST" to request list of active clients.')
                                                print('2. Enter "GET_CLIENT_INFO <username>", with username of a client to connect to')
                                                print('3. CLIENT_LIST<name1, name2, ... > tells names of active clients')
                                                print('4. Enter "SEND_FILE<file path>" to send any file from respective path')
                                                print('5. Enter "CLOSE_SESSION" to stop communicating with any client')
                                                print('6. Enter "DISCONNECT_CLIENT" to disconnect from chat service')
                                                print('7. Enter "#HELP" anytime to read instructions again')
                                                s.send(str(add))
                                                break
                                            else:
                                                print("Incorrect password: Enter Again Below")
                                                password = raw_input("Enter Password: ")
                                                s.send(password)
                                        if(i==2):
                                            print("Sorry, You have exceeded number of attempts")
                                            sys.exit()
                                        break	
                                else:
                                    print("Sorry, You can not use this service")
                                    sys.exit()
                            else:
                                print('Invalid Input, Enter again')	
                    else:
                        sys.stdout.write(data+"\n")
                        sys.stdout.flush()

            elif sock ==  cl:
	#print 'Hi'
                client, address = sock.accept()
                socket_list.append(client)
                flag = 2
            
            elif sock == sys.stdin:
                msg = sys.stdin.readline()
                if "SEND_FILE" in msg and flag != 0:
                    data = find_between(msg, "<", ">")
                    if data == '':
                        msg = "Please enter the filename: SEND_FILE<filename>\n"
                        if flag == 1:
                            print('Please enter the filename: SEND_FILE<filename>')
                            cs.send(name+":"+msg)
                        else:
                            print('Please enter the filename: SEND_FILE<filename>')
                            client.send(name+":"+msg)
                    else:
                        try:
                            f = open(curdir + sep + data, 'rb')
                            if flag == 1:
                
                                cs.send("START_FILE_TRANSFER<"+data+">")
                            else:
                                client.send("START_FILE_TRANSFER<"+data+">")
                            l = f.read(9999)
                            if flag == 1:
                                cs.send(l)
                            else:
                                client.send(l)
					#while (l):	
					#	if flag == 1:
					#		cs.send(l)
					#	else:
					#		client.send(l)
    					#	l = f.read(1024)
                            print("File Sent")
                            f.close()
                        except IOError:
                            print("File not found")
	
                elif "DISCONNECT_CLIENT" in msg:
                    s.send(msg+"<"+name+">")
                    print("DISCONNET REQUEST SENT "+msg+"<"+name+">")
                    sys.exit()
		
                elif "#HELP" in msg:
                    print( 'Service usage description.')
                    print( '1. Enter "GET_CLIENT_LIST" to request list of active clients.')
                    print( '2. Enter "GET_CLIENT_INFO <username>", with username of a client to connect to')
                    print( '3. CLIENT_LIST<name1, name2, ... > tells names of active clients')
                    print( '4. Enter "SEND_FILE<file path>" to send any file from respective path')
                    print( '5. Enter "CLOSE_SESSION" to stop communicating with any client')
                    print( '6. Enter "DISCONNECT_CLIENT" to disconnect from chat service')
                    print( '7. Enter "#HELP" anytime to read instructions again')
                else:
                    if "GET_CLIENT_INFO" in msg:
                        name2 = find_between(msg, "<", ">")
                    if flag == 1:
                        cs.send(name+":"+msg)
                    elif flag ==2:
                        client.send(name+":"+msg)
                    else:
                        if "GET_CLIENT_INFO" in msg:
                            name2 = find_between(msg, "<", ">")
                            if name2 == name:
                                print("You cannot connect to yourself")
                            else:
                                s.send(msg)
                        else:
                            s.send(msg)
               		#sys.stdout.write(name+": "); sys.stdout.flush() 
	      
            else :
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
			
                    if "START_FILE_TRANSFER" in data:
                        data = find_between(data, "<", ">")
                        if "." in data:
                            filename = data.split(".")[0]
                            extension = data.split(".")[1]
                            f = open('Received_'+filename+"."+extension,'wb')
                        else:
                            f = open('Received_'+data,'wb')
                        l = sock.recv(9999)
                        f.write(l)
				#try:
				#	l = sock.recv(1024)
        			#	while (l):
                		#		f.write(l)
                		#		l = sock.recv(1024)
				#except socket.timeout:
                        f.close()
                        print( "A file is received")
			#If close session request is received by other client
                    elif "CLOSE_SESSION" in data:
                        print( "Your session has been closed")
                        if flag == 1:
                            cs.send("Your session has been closed\n")
                            flag = 0
                        elif flag ==2:
                            client.send("Your session has been closed\n")
                            flag = 0
                        socket_list.remove(sock)
                        sock.close()
				#print "SESSION_END_NOTIFICATION<"+name2+">"
                        s.send("SESSION_END_NOTIFICATION<"+name+">")
			
                    elif "Your session has been closed" in data:
                        flag = 0
                        socket_list.remove(sock)
                        sock.close()
                        sys.stdout.write(data)
                        sys.stdout.flush()
                    else:
                        sys.stdout.write(data)
                        sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(chat_client())
