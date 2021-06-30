#ifndef _max_H_
#define _max_H_
#pragma once
#pragma warning(disable : 4996)
#include<windows.h>
#include<stdio.h>
#include<WinSock.h>
#include<iostream>
#include<string>
using namespace std;
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
#endif
