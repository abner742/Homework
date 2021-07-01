 #pragma comment(lib,"ws2_32.lib")
#include<winsock2.h>
#include<stdio.h>
#include<string.h>
#include<time.h>
#define MAX_NUM  50
#define PORT 5000
#define MSG_MAX_SIZE 1000
int main()
{
	int sendbyte,j,m,people=0;
	char MesAll[MAX_NUM][MSG_MAX_SIZE+25];
	int first[MAX_NUM]={0};
	char name[MAX_NUM][25];
	char buf[MAX_NUM][MSG_MAX_SIZE];
	time_t   timenow;  
	WSADATA wsadata;
	int err = WSAStartup(WINSOCK_VERSION,&wsadata);
	if(err != 0)
	{
		printf("WSAStartup() failed :%d\n",WSAGetLastError());
		return -1;
	}

	SOCKET sock = socket(AF_INET,SOCK_STREAM,0);
	if(sock == INVALID_SOCKET)
	{
		printf("socket() failed:%d\n",WSAGetLastError());
		WSACleanup();
		return -1;
	}

	sockaddr_in localaddress;
	localaddress.sin_family = AF_INET;
	localaddress.sin_port = htons(PORT);
	localaddress.sin_addr.S_un.S_addr = htonl(INADDR_ANY);

	err = bind(sock,(sockaddr *)&localaddress,sizeof(localaddress));
	if(err == INVALID_SOCKET)
	{
		printf("bind() failed:%d\n",WSAGetLastError());
		closesocket(sock);
		WSACleanup();
		return -1;
	}

	err=listen(sock,6);
	if(err == INVALID_SOCKET)
	{
		printf("listen() failed:%d\n",WSAGetLastError());
		closesocket(sock);
		WSACleanup();
		return -1;
	}
	SOCKET client[MAX_NUM];
	for(int i = 0;i<MAX_NUM;i++)
	{
		client[i] = INVALID_SOCKET;
	}

	fd_set rset,allset;
	FD_ZERO(&allset);
	FD_SET(sock,&allset);
	while(1)
	{
		rset=allset;
		int ret = select(0,&rset,NULL,NULL,NULL);
		if(ret == SOCKET_ERROR)
		{
			printf("select() failed:%ld\n",WSAGetLastError());
			break;
		}


		if(ret == 0){
			continue;
		}

		if(FD_ISSET(sock,&rset))
		{
			sockaddr_in clientaddr;
			int len = sizeof(clientaddr);
			SOCKET sockconn = accept(sock,(sockaddr *)&clientaddr,&len);
			if(sockconn == INVALID_SOCKET)
			{
				printf("accept() failed:%d\n",WSAGetLastError());
				break;
			}
			printf("Client's IP：%s Port：%d",inet_ntoa(clientaddr.sin_addr),clientaddr.sin_port);
			int i;
			for(i=0;i<MAX_NUM;i++)
			{
				if(client[i] == INVALID_SOCKET)
				{
					client[i] = sockconn;
					break;
				}
			}
			if(i<MAX_NUM)
			{
				FD_SET(sockconn,&allset);
			}

			else{
				printf("too many client");
				closesocket(sockconn);
			}

		}
		for(int i=0;i<MAX_NUM;i++)
		{
			if((client[i]!=INVALID_SOCKET)&&FD_ISSET(client[i],&rset))
			{
				memset(buf[i],0,MSG_MAX_SIZE);
				int recbyte = recv(client[i],buf[i],MSG_MAX_SIZE,0);//收到数据
				if(recbyte == SOCKET_ERROR)
				{
					first[i]=0;//若退出，则将客户信息置为初始值
					people=0;
                    for(m=0;m<MAX_NUM;m++)
						if(first[m]==1)
							people++;
					printf("%s exit the chat room.目前在线人数：%d.\n",name[i],people);
                    strcpy(MesAll[i],"From server: ");
					strcat(MesAll[i],name[i]);
					strcat(MesAll[i]," 下线.");
					FD_CLR(client[i],&allset);
					closesocket(client[i]);
					client[i] = INVALID_SOCKET;
					//告诉其他客户有人下线
					for(j=0;j<MAX_NUM;j++)
					{
						if((client[j]!=INVALID_SOCKET) )
						{   
							sendbyte = send(client[j],MesAll[i],1024,0);
						    if(sendbyte == SOCKET_ERROR)
							{
								printf("send() failed:%d\n",WSAGetLastError());
							}
						    
						}
					}	
					continue;
				}
				//如果有新人进入，则给客户端发送提示消息
				if(!first[i])
				{
                    strcpy(MesAll[i],"From server: ");
					strcat(MesAll[i],buf[i]);
					strcat(MesAll[i]," 上线.");
				}
				else
				{
					strcpy(MesAll[i],name[i]);
				    strcat(MesAll[i],": ");
				    strcat(MesAll[i],buf[i]);
				}
				for(j=0;j<MAX_NUM;j++)
				{
					if((client[j]!=INVALID_SOCKET) )
					{   
					    sendbyte = send(client[j],MesAll[i],1000,0);
						if(sendbyte == SOCKET_ERROR)
						{
							printf("send() failed:%d\n",WSAGetLastError());
						}
						
					}
				}
				time(&timenow);
				//服务器端显示新进客户的信息
				if(!first[i])
				{
					people=0;
					for(m=0;m<MAX_NUM;m++)
						if(first[m]==1)
							people++;
					strcpy(name[i],buf[i]);
					printf("  NAME:%s  TIME:%s",buf[i],asctime(localtime(&timenow)));
					printf("目前在线人数：%d\n",people+1);
					first[i]=1;
				}
				else
				printf("%s:%s%s\n",name[i],asctime(localtime(&timenow)),buf[i]);
			}
		}
		
	}
	closesocket(sock);
	WSACleanup();
	return 0;
}
