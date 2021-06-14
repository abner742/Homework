# 基于多线程服务器的邮件发送系统   

## 实现的功能

**1.多线程服务器**

**2.邮件发送功能**

**3.前端格式自动校对**

**4.不同文件类型的收发**（html,css,js,png,jpg,json）

**5.get,post等等的请求方法处理**



## 使用说明

**1.安装依赖**

在项目目录下运行 

```
pip install -r requirements.txt
```

**2.配置配置文件**

在config.py中配置服务器的ip地址，端口等等

**2.启动服务器**

运行 Multi_Thread_web_server.py 文件

**3.运行web端**

打开任意浏览器，键入 http://MULTI_SERVER_ADDRESS:MULTI_SERVER_PORT/index.html，其中MULTI_SERVER_ADDRESS，MULTI_SERVER_PORT均为自己配置。

运行正常可以看到这个界面：



![image-20210614141113190](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20210614141113190.png)



**4.登录**

键入qq邮箱和授权码，可以进行登录。前端会提示是否登录成功

**5.发送邮件**

登录成功后，可以发送邮件

![image-20210614141410848](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20210614141410848.png)



**5.发送成功后会跳转到发送成功界面**

![image-20210614141449497](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20210614141449497.png)



