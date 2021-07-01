#pragma comment(lib,"ws2_32.lib")
#include<winsock2.h>
#include<stdio.h>
#include<string.h>
#include<windows.h>
#include<PROCESS.H>
#include <process.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h> 
#define PORT 5000
int first=1;
//监视输入的线程函数
void  getInput(void * param)
{
	SOCKET sock =(SOCKET)param;
	while(1)
	{
		char buf[1024];
		gets(buf);
		int sendbyte = send(sock,buf,strlen(buf),0);
		if(sendbyte == SOCKET_ERROR)
		{
			printf("send() failed:%d\n",WSAGetLastError());
		}
	}
}
int main()
{
	char flag,flag1;	
	int loginmax=3;
	int connectmax=5;
	int i=1;
	int flag2;
	int flag3=0;
	time_t timenow;
	WSADATA wsadata1;
	char name[15];
	char password[30];
	flag1='y';
	//输口令
	do{
		printf("Please input the password:");
        gets(password);
	    if(strcmp(password,"123")==0)
			break;
		else
		{
			loginmax-=1;
			if(loginmax)
				printf("You have %d times to change the password!\n",loginmax);
			else
				printf("The system will be closed!\n");
		}
	}while(loginmax);
	if(loginmax)
	{
	printf("Please input your name:");
	gets(name);
	do{	
		printf("Do you want to establish a connection with the server?(y/n):");
        scanf("%c",&flag);
	    //建立连接
	    if(flag=='y')
		{
			connectmax--;
			printf("connecting...\n");
			i=0;
	        int err = WSAStartup(WINSOCK_VERSION,&wsadata1);
	        if(err != 0)
			{
				printf("WSAStartup() failed :%d\n",WSAGetLastError());
		        return -1;
			}
			SOCKET sock = socket(AF_INET,SOCK_STREAM,0);
			if(sock == INVALID_SOCKET)
			{
				printf("socket() failed:%d.Please check your computer!\n",WSAGetLastError());
	        	WSACleanup();
		        return -1;
			}
			sockaddr_in serveraddress;
			serveraddress.sin_family = AF_INET;
			serveraddress.sin_port = htons(PORT);
			serveraddress.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
			do{	
				if(flag3)
				{
					connectmax--;
					if(connectmax)
						printf("connecting...\n");
					else
					{
						printf("There must be some wrong with the server!System will exit.\n");
						return -1;
					}
				}
				flag3=1;
				err=connect(sock,(sockaddr *)&serveraddress,sizeof(serveraddress));
			    if(err == INVALID_SOCKET)
				{
					getchar();
					printf("connect() failed:%d\n",WSAGetLastError());
			   	    printf("If you want to try again,please press 'y':");
			        scanf("%c",&flag1);
			    	if(flag1=='y')	
						continue;
					else
					{
						closesocket(sock);
					    WSACleanup();
				        return -1;
					}
				}
				else 
					break;
			}while(flag1=='y');
			//连接成功
			send(sock,name,strlen(name),0);
			flag2=recv(sock,name,100,0);
			if(flag2==SOCKET_ERROR)
			{
				printf("recv() failed:%d.Please check the server.\n",WSAGetLastError());
				return -1;
			}
			system("cls");  
	        printf("Welcome to the chatroom!\n");
        	_beginthread(getInput,0,(void*)sock);
	        Sleep(1000);
			char rbuf[1024];
			while(1)
			{
				memset(rbuf,0,1024);
				int recbyte =recv(sock,rbuf,1000,0);
				if(recbyte == SOCKET_ERROR)
				{
					printf("recv() failed:%d.Please check the server.\n",WSAGetLastError());
			        closesocket(sock);
			        WSACleanup();
			        return -1;
				}
				timenow=time(NULL);
				if(first)
				{
					first=0;
				    continue;
				}
		        printf("%s%s\n",ctime(&timenow),rbuf);
		        Sleep(1000);
			}
			closesocket(sock);
	        WSACleanup();
	        return 0;
		}
		else if(flag=='n')
			return 0;
		else 
		{
			printf("Input error,please input again!\n");
			getchar();
		}
	}while(i);
	}
}
