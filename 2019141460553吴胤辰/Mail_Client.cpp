
#include <iostream>
#include <string>
#include <WinSock2.h>
#include <stdio.h>
#include <sstream>
#include <iostream>
#include <fstream>
#include <windows.h>

using namespace std;
#pragma comment(lib, "ws2_32.lib") /*链接ws2_32.lib动态链接库*/

//获取路径
char* GetAppPath(char* AppPath, int nSize)
{
    int i;
    memset(AppPath, 0, nSize);
#ifdef UNICODE
    GetModuleFileNameA(NULL, AppPath, nSize);
#else
    GetModuleFileName(NULL, AppPath, nSize);
#endif
    for (i = strlen(AppPath) + 1; i >= 0; i--)
    {
        if (AppPath[i] == '\\')
        {
            break;
        }
    }
    AppPath[i] = 0;
    return AppPath;
}

int main()
{
    char app[1024] = { 0 };
    GetAppPath(app, sizeof(app));
    char filepath[1024] = { 0 };
    sprintf_s(filepath, "%s\\ID_and_AuthorizationCode.ini", app);
    char buf_1[1024] = { '\0' };
    char buf_2[1024] = { '\0' };
    GetPrivateProfileStringA("info", "ID", "TestData", buf_1, sizeof(buf_1), filepath);
    GetPrivateProfileStringA("info", "AuthorizationCode", "TestData", buf_2, sizeof(buf_2), filepath);
    buf_1[strlen(buf_1)] = '\r';
    buf_1[strlen(buf_1)] = '\n';
    buf_2[strlen(buf_2)] = '\r';
    buf_2[strlen(buf_2)] = '\n';

    char buff[10000]; //收到recv函数返回的结果
    string message;
    string info;//邮件内容
    string subject;//邮件主题
    WSADATA wsaData;//存储被WSAStartup函数调用后返回的Windows Sockets数据
    WORD wVersionRequested = MAKEWORD(2, 1);//创建一个无符号16位整型数
    //WSAStarup，即WSA(Windows SocKNDs Asynchronous，Windows套接字异步)的启动命令
    //使用Socket的程序在使用Socket之前必须调用WSAStartup函数，以后应用程序就可以调用所请求的Socket库中的其他Socket函数了
    int err = WSAStartup(wVersionRequested, &wsaData);//进行相应的socket库绑定
    SOCKADDR_IN addrServer; //服务端地址
    HOSTENT* pHostent;//hostent是host entry的缩写，该结构记录主机的信息，包括主机名、别名、地址类型、地址长度和地址列表
    SOCKET sockClient; //客户端的套接字
    /*
    使用 MAIL 命令指定发送者
    使用 RCPT 命令指定接收者，可以重复使用RCPT指定多个接收者
    */
    cout << "发送邮件请按“1”，查看邮件请按“2”：\n";
    int choose;
    cin >> choose;
    if (choose == 1)
    {
        sockClient = socket(AF_INET, SOCK_STREAM, 0); //建立socket对象
        //stmp为电子邮件发送协议
        pHostent = gethostbyname("smtp.163.com"); //得到有关于域名的信息,链接到qq邮箱服务器
        addrServer.sin_addr.S_un.S_addr = *((DWORD*)pHostent->h_addr_list[0]); //得到smtp服务器的网络字节序的ip地址
        addrServer.sin_family = AF_INET;//TCP/IP-IPv4
        addrServer.sin_port = htons(25); //连接端口25，端口25对应简单邮件传输服务器SMTP
        //int connect (SOCKET s , const struct sockaddr FAR *name , int namelen ); //函数原型
        //向服务器发送请求,用于建立客户端与服务器之间的连接
        err = connect(sockClient, (SOCKADDR*)&addrServer, sizeof(SOCKADDR));
        //不论是客户还是服务器应用程序都用recv函数从TCP连接的另一端接收数据
        //该函数的第一个参数指定接收端套接字描述符
        //recv()函数返回其实际copy的值接受，如果recv在copy时出错，那么它返回SOCKET_ERROR；如果recv在等待协议接收数据时网络中断了，那么它返回0
        buff[recv(sockClient, buff, 10000, 0)] = '\0';//buff指明一个缓冲区，存放recv函数接收到的数据，500指明缓冲区的长度
        /*
        登录邮件服务器
        */
        message = "ehlo 163.com\r\n";//ehol可以支持用户认证
        //send()向一个已经连接的socket发送数据，如果无错误，返回值为所发送数据的总数，否则返回SOCKET_ERROR
        //c_str()把string对象转换成c中的字符串样式
        //客户端发送ehlo命令,用来把客户的域名通知服务器
        //在TCP连接建立阶段，发送方和接收方都是通过他们的IP地址来告诉对方的
        send(sockClient, message.c_str(), message.length(), 0);
        buff[recv(sockClient, buff, 10000, 0)] = '\0';   //接收返回值
        //cout <<"1" <<  buff << endl;

        message = "auth login\r\n";//进行用户身份认证
        send(sockClient, message.c_str(), message.length(), 0);
        buff[recv(sockClient, buff, 10000, 0)] = '\0';
        // cout <<"2" <<  buff << endl;
        /*
        由于使用EHLO，需要发送base64加密的用户名、密码
        */
        message = buf_1;//base64加密的用户名
        send(sockClient, message.c_str(), message.length(), 0);
        buff[recv(sockClient, buff, 10000, 0)] = '\0';
        // cout <<"3" <<  buff << endl;


        message = buf_2;//base64加密的密码
        send(sockClient, message.c_str(), message.length(), 0);
        int datasize_1 = recv(sockClient, buff, 10000, 0);
        if (datasize_1 >= 0 && datasize_1 < 10000) {
            buff[datasize_1] = '\0';
            // cout <<"4" <<  buff << endl;
            string mail;
            cout << "请输入收件人邮箱：";
            cin >> mail;

            /*
            客户发送MAIL FROM报文介绍报文的发送者
            它包括发送人的邮件地址
            可以给服务器在返回差错或报文时的返回邮件地址
            */
            /*
            客户发送RCPT(收件人)报文，包括收件人的邮件地址
            RCPT命令的作用是：先弄清接收方系统是否已经准备好接受邮件的准备，然后才发送邮件
            这样做是为了避免浪费通信资源，不至于发送了很长的邮件之后才知道是因地址错误
            */
            message = "MAIL FROM:<w13096399062@163.com> \r\nRCPT TO:<";
            message.append(mail);
            message.append("> \r\n");
            send(sockClient, message.c_str(), message.length(), 0);
            buff[recv(sockClient, buff, 10000, 0)] = '\0';
            // cout <<"5" <<  buff << endl;
            /*
            客户发送DATA报文对报文的传送进行初始化
            DATA命令表示要开始传送邮件的内容了
            */
            message = "DATA\r\n";
            send(sockClient, message.c_str(), message.length(), 0);
            buff[recv(sockClient, buff, 10000, 0)] = '\0';
            // cout <<"6" <<  buff << endl;
            message = "From: w13096399062@163.com\r\nTo: " + mail + "\r\nsubject:";
            cout << "主题：";
            cin >> subject;
            message.append(subject);
            message.append("\r\n\r\n");
            cout << "内容：";
            cin >> info;
            message.append(info);
            message.append("\r\n.\r\n");

            send(sockClient, message.c_str(), message.length(), 0);//发送邮件内容
            // cout <<"7" <<  buff << endl;
            /*
            在报文传送成功后，客户就终止连接，包括如下步骤：
            1.客户发送QUIT命令
            2.服务器响应221（服务关闭）或其他代码
            在连接终止阶段，TCP连接必须关闭
            */
            message = "QUIT\r\n";
            send(sockClient, message.c_str(), message.length(), 0);
            buff[recv(sockClient, buff, 10000, 0)] = '\0';
            // cout <<"8" <<  buff << endl;
            cout << "发送成功！" << endl;
        }
        else {
            std::cout << "数据大小过大或接收失败 \n";
        }
    }
    else if (choose == 2)
    {
        sockClient = socket(AF_INET, SOCK_STREAM, 0); //建立socket对象
        //pop是邮件读取协议
        //const char *host_id = "pop3.126.com";//const定义只读变量的关键字
        pHostent = gethostbyname("pop.163.com");//得到有关于域名的信息,链接到163邮箱服务器
        int port = 110;//端口110是为pop3服务开放的。使用电子邮件客户端程序的时候，会要求输入POP3服务器地址，默认情况下使用的就是110端口
        addrServer.sin_addr.S_un.S_addr = *((DWORD*)pHostent->h_addr_list[0]); //得到smtp服务器的网络字节序的ip地址
        addrServer.sin_family = AF_INET;//TCP/IP-IPv4
        addrServer.sin_port = htons(port); //连接端口110
        //向服务器发送请求,用于建立客户端与服务器之间的连接
        err = connect(sockClient, (SOCKADDR*)&addrServer, sizeof(SOCKADDR)); //向服务器发送请求
        //不论是客户还是服务器应用程序都用recv函数从TCP连接的另一端接收数据
        //该函数的第一个参数指定接收端套接字描述符
        //recv()函数返回其实际copy的只接受，如果recv在copy时出错，那么它返回SOCKET_ERROR；如果recv在等待协议接收数据时网络中断了，那么它返回0
        buff[recv(sockClient, buff, 10000, 0)] = '\0';
        //cout <<"1" <<  buff << endl;
        message = "user w13096399062@163.com\r\n";
        send(sockClient, message.c_str(), message.length(), 0); //发送账号
        buff[recv(sockClient, buff, 10000, 0)] = '\0';   //接收返回值
        //std::cout << "Client : send name \nServer:"<< buff << std::endl;

        message = "pass DYXWIMHVPBFPMBKW\r\n";//授权码
        send(sockClient, message.c_str(), message.length(), 0); //发送授权码
        buff[recv(sockClient, buff, 10000, 0)] = '\0';   //接收返回值
        //std::cout << "Client : send authoriza code\nServer:"<< buff << std::endl;

        message = "stat\r\n";//查看总共多少封信件，多少字节
        send(sockClient, message.c_str(), message.length(), 0); //发送状态
        buff[recv(sockClient, buff, 10000, 0)] = '\0';   //接收返回值
        Sleep(1);
        std::cout << "Client : send stat \nServer : "
            << buff << std::endl;

        message = "list\r\n";//列出每封信件的字节数
        send(sockClient, message.c_str(), message.length(), 0); //发送状态
        buff[recv(sockClient, buff, 10000, 0)] = '\0';   //接收返回值
        Sleep(1);
        std::cout << "Client : send list \nServer :"
            << buff << std::endl;
        int number;
        std::cout << "请输入要查看的邮件的序号"
            << std::endl;
        cin >> number;
        stringstream ss;
        ss << number;
        string str_number = ss.str();//将数字number转换为字符串str

        //retr str_number 读取第str_number封信
        message = "retr " + str_number + "\r\n";
        send(sockClient, message.c_str(), message.length(), 0); //发送状态
        Sleep(1);
        std::cout << "Client : send retr (...) \n";

        memset(buff, 0, 10000);
        buff[recv(sockClient, buff, 10000, 0)] = '\0';   //接收返回值
        buff[recv(sockClient, buff, 10000, 0)] = '\0';
        Sleep(1);
        std::cout << "Server ：" << buff << std::endl;
        message = "quit\r\n";
        send(sockClient, message.c_str(), message.length(), 0);
        //buff[recv(sockClient, buff, 500, 0)] = '\0';
        //std::cout << "Client : send quit \nServer :"<< buff << std::endl;

        cout << "查询成功！" << endl;

    }
    else {
        cout << "输入错误！" << endl;
    }
}


