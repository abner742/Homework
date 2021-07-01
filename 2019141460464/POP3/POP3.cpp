
#pragma warning(disable : 4996)
#include<windows.h>
#include<stdio.h>
#include<WinSock.h>
#include<iostream>
#include<string>
#include"f.h"
using namespace std;
#pragma comment(lib,"ws2_32.lib")
int main()
{
    int sockfd = { 0 };
    char buf[1500] = { 0 };
    char rbuf[1500] = { 0 };
    char login[128] = { 0 };
    char pass[128] = { 0 };
    WSADATA WSAData;
    struct sockaddr_in their_addr = { 0 };
    WSAStartup(MAKEWORD(2, 2), &WSAData);
    memset(&their_addr, 0, sizeof(their_addr));
    their_addr.sin_family = AF_INET;
    their_addr.sin_port = htons(110);
    hostent* hptr = gethostbyname("pop3.163.com");
    memcpy(&their_addr.sin_addr.S_un.S_addr, hptr->h_addr_list[0], hptr->h_length);
    printf("IP of pop3.163.com is : %d:%d:%d:%d\n",
        their_addr.sin_addr.S_un.S_un_b.s_b1,
        their_addr.sin_addr.S_un.S_un_b.s_b2,
        their_addr.sin_addr.S_un.S_un_b.s_b3,
        their_addr.sin_addr.S_un.S_un_b.s_b4);

    sockfd = OpenSocket((struct sockaddr*)&their_addr);
    cout << "look:" << sockfd << endl;
    memset(rbuf, 0, 1500);
    while (recv(sockfd, rbuf, 1500, 0) == 0)
    {
        cout << "重新连接..." << endl;
        Sleep(5);
        sockfd = OpenSocket((struct sockaddr*)&their_addr);
        memset(rbuf, 0, 1500);
    }
    cout << rbuf << endl;

    memset(buf, 0, 1500);
    sprintf(buf, "%s\r\n", "user gggjjj2021@163.com");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    sprintf(buf, "%s\r\n", "pass GROFRKYAPKSODGGV");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
 
    memset(buf, 0, 1500);
    sprintf(buf, "%s\r\n", "list");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
 
    string input;
    cout << "请输入查询命令:" << endl;
    getline(cin, input);
    sprintf(buf, "%s\r\n", input.c_str());
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    sprintf(buf, "QUIT\r\n");
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << "Quit Receive: " << rbuf << endl;

    closesocket(sockfd);
    WSACleanup();
    return 0;
}


