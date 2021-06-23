# SCU聊天室 --《计算机网络》课程项目

scu聊天室是一个具有实时通讯功能的多人聊天室Python程序



### 使用说明

- 本程序包含五个.py文件以及一个user.txt，一个config.ini配置 文件，请保持目录结构不被修改。

- 如果您想在多台主机上运行客户端程序，请首先进行ipconfig查询您想运行服务器端的主机的ip地址，并修改config.ini的server_ip值为服务器端主机ip地址，如下图所示：

![image-20210623193201009](C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210623193201009.png)

- 首先运行Server.py，接着运行Client.py，接下来您可以选择注册或登录进入聊天室进行聊天。








### 实现的功能

- ##### 注册

  用户首次使用聊天室要进行注册

  <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618102707934.png" alt="image-20210618102707934" style="zoom:33%;" />

  

  

  

  

  

  一些错误处理：输入纯数字密码或、两次密码不一致或用户名被注册，错误处理如下：

  <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618103240985.png" alt="image-20210618103240985" style="zoom: 25%;" /><img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618103300155.png" alt="image-20210618103300155" style="zoom: 25%;" /><img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618103844604.png" alt="image-20210618103844604" style="zoom: 25%;" />




- ##### 登录

  用户登录进入聊天室：

  <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618103542560.png" alt="image-20210618103542560" style="zoom:33%;" />

  若用户名或密码错误，则提示错误信息：

  <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618103519763.png" alt="image-20210618103519763" style="zoom:33%;" />

  

- ##### 发送、接受消息

  - 在输入框中输入消息内容，点击发送可发送消息，点击清空可以清空输入框

  <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618104528190.png" alt="image-20210618104528190" style="zoom: 33%;" />

  - 在消息框中可以查看所有人的聊天内容，包括用户名称、发送消息时间、消息内容，

  本人消息与他人消息用不同颜色标注

  <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618104754592.png" alt="image-20210618104754592" style="zoom:33%;" />

  

  - 私聊功能：

    用户通过在消息框中输入#!(想要私聊的人)!#+消息内容，可以私聊聊天室中的某一个成员，其他成员不会收到消息。

    王五给张三发私信，张三看到的：

    <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210623212640828.png" alt="image-20210623212640828" style="zoom: 25%;" />

    李四看到的：

    <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210623212703013.png" alt="image-20210623212703013" style="zoom:25%;" />

  

- ##### 查看在线用户

  每当有新用户加入聊天室，在线用户列表会自动更新

  <img src="C:\Users\kim\AppData\Roaming\Typora\typora-user-images\image-20210618104315631.png" alt="image-20210618104315631" style="zoom:33%;" />



