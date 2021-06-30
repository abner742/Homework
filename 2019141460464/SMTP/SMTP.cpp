#include"functions.h"
void SendMail(char* email, char* body);
int OpenSocket(struct sockaddr* addr);
void main()
{
    char EmailTo[] = "gggjjj2021@163.com";
    char EmailContents[1000];
    char info[100];
    sprintf(info, "Subject: %s:\r\n", "测试标题");
    sprintf(EmailContents, "From: \"163邮箱\"<jlc1233212021@163.com>\r\n" "To: \"163邮箱\"<gggjjj2021@163.com>\r\n" "%s\r\n" "SMTPandPOP3", info);
    SendMail(EmailTo, EmailContents);
}

