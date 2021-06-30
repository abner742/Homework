#ifndef _max_H_
#define _max_H_
#pragma warning(disable : 4996)
using namespace std;
#include<windows.h>
#include<stdio.h>
#include<WinSock.h>
#include<iostream>
#pragma comment(lib,"ws2_32.lib")

int OpenSocket(struct sockaddr* addr)
{
    int sockfd = 0;
    sockfd = socket(PF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
    {
        cout << "Open sockfd(TCP) error!" << endl;
        exit(-1);
    }
    if (connect(sockfd, addr, sizeof(struct sockaddr)) < 0)
    {
        cout << "Connect sockfd(TCP) error!" << endl;
        exit(-1);
    }
    return sockfd;
}
struct Base64Date6
{
    unsigned int d4 : 6;
    unsigned int d3 : 6;
    unsigned int d2 : 6;
    unsigned int d1 : 6;
};
char ConvertToBase64(char uc)
{
    if (uc < 26)
    {
        return'A' + uc;
    }
    if (uc < 52)
    {
        return'a' + (uc - 26);
    }
    if (uc < 62)
    {
        return'0' + (uc - 52);
    }
    if (uc == 62)
    {
        return'+';
    }
    if (uc == 63)
    {
        return '/';
    }
}
void  EncodeBase64(char* dbuf, char* buf128, int len)
{
    struct  Base64Date6* ddd = NULL;
    int i = 0;
    char buf[256] = { 0 }; //数组uf里面的值全部初始化为0
    char* tmp = NULL;
    char cc = '\0'; //对应的ASCII值为0，是字符串结束的标志
    memset(buf, 0, 256); //初始化函数。作用是将某一块内存中的内容全部设置为指定的值。memset()函数通常为新申请的内存做初始化工作。
    //这句的话意思是将buf中当前位置后面的256个字节用0替换并返回buf
    strcpy(buf, buf128);//这句话的意思是把从buf128地址开始且含有NULL结束符的字符串复制到以dest开始的地址空间
    for (i = 1; i <= len / 3; i++)
    {
        tmp = buf + (i - 1) * 3;
        cc = tmp[2];
        tmp[2] = tmp[0];
        tmp[0] = cc;
        ddd = (struct Base64Date6*)tmp;
        dbuf[(i - 1) * 4 + 0] = ConvertToBase64((unsigned int)ddd->d1);
        dbuf[(i - 1) * 4 + 1] = ConvertToBase64((unsigned int)ddd->d2);
        dbuf[(i - 1) * 4 + 2] = ConvertToBase64((unsigned int)ddd->d3);
        dbuf[(i - 1) * 4 + 3] = ConvertToBase64((unsigned int)ddd->d4);
    }
    if (len % 3 == 1)
    {
        tmp = buf + (i - 1) * 3;
        cc = tmp[2];
        tmp[2] = tmp[0];
        tmp[0] = cc;
        ddd = (struct Base64Date6*)tmp;
        dbuf[(i - 1) * 4 + 0] = ConvertToBase64((unsigned int)ddd->d1);
        dbuf[(i - 1) * 4 + 1] = ConvertToBase64((unsigned int)ddd->d2);
        dbuf[(i - 1) * 4 + 2] = '=';
        dbuf[(i - 1) * 4 + 3] = '=';
    }
    if (len % 3 == 2)
    {
        tmp = buf + (i - 1) * 3;
        cc = tmp[2];
        tmp[2] = tmp[0];
        tmp[0] = cc;
        ddd = (struct Base64Date6*)tmp;
        dbuf[(i - 1) * 4 + 0] = ConvertToBase64((unsigned int)ddd->d1);
        dbuf[(i - 1) * 4 + 1] = ConvertToBase64((unsigned int)ddd->d2);
        dbuf[(i - 1) * 4 + 2] = ConvertToBase64((unsigned int)ddd->d3);
        dbuf[(i - 1) * 4 + 3] = '=';
    }
    return;
}
void SendMail(char* email, char* body)
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
    their_addr.sin_port = htons(25);
    hostent* hptr = gethostbyname("smtp.163.com");
    memcpy(&their_addr.sin_addr.S_un.S_addr, hptr->h_addr_list[0], hptr->h_length);
    printf("IP of smpt.163.com is : %d:%d:%d:%d\n",
        their_addr.sin_addr.S_un.S_un_b.s_b1,
        their_addr.sin_addr.S_un.S_un_b.s_b2,
        their_addr.sin_addr.S_un.S_un_b.s_b3,
        their_addr.sin_addr.S_un.S_un_b.s_b4);
    sockfd = OpenSocket((struct sockaddr*)&their_addr);

    memset(rbuf, 0, 1500);
    while (recv(sockfd, rbuf, 1500, 0) == 0)
    {
        cout << "重新连接..." << endl;
        Sleep(5);
        sockfd = OpenSocket((struct sockaddr*)&their_addr);
        memset(rbuf, 0, 1500);
    }
    cout << rbuf << endl;


    // EHLO
    memset(buf, 0, 1500);
    sprintf(buf, "ehlo jlc1233212021@163.com\r\n");
    cout << buf << endl;
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // AUTH LOGIN
    memset(buf, 0, 1500);
    sprintf(buf, "auth login\r\n");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // USER
    memset(buf, 0, 1500);
    sprintf(buf, "jlc1233212021@163.com");
    memset(login, 0, 128);
    EncodeBase64(login, buf, strlen(buf));
    sprintf(buf, "%s\r\n", login);
    send(sockfd, buf, strlen(buf), 0);
    cout << "Base64 UserName: " << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // PASSWORD
    sprintf(buf, "XIUFIDDRUXMUWPGY");
    memset(pass, 0, 128);
    EncodeBase64(pass, buf, strlen(buf));
    sprintf(buf, "%s\r\n", pass);
    send(sockfd, buf, strlen(buf), 0);
    cout << "Base64 Password: " << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    memset(buf, 0, 1500);
    sprintf(buf, "mail from:<jlc1233212021@163.com>\r\n");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);

    cout << rbuf << endl;

    sprintf(buf, "rcpt to:<%s>\r\n", email);
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    sprintf(buf, "data\r\n");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    sprintf(buf, "%s\r\n.\r\n", body);
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    sprintf(buf, "quit\r\n");
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    closesocket(sockfd);
    WSACleanup();
    return;
}
#endif
