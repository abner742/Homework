import socket
from threading import Thread
import math
import re
import configparser

# online_conn维护一个在线用户
online_conn = list()
# conn2user存储socket连接和用户的对应关系
conn2user = dict()


# 发送带长度的字符串
def send_string_with_length(_conn, content):
    # 先发送内容的长度
    _conn.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
    # 再发送内容
    _conn.sendall(bytes(content, encoding='utf-8'))


def send_number(_conn, number):
    _conn.sendall(int(number).to_bytes(4, byteorder='big'))


def recv_number(_conn):
    return int.from_bytes(_conn.recv(4), byteorder='big')


# 获取定长字符串
def recv_string_by_length(_conn, len):
    return str(_conn.recv(len), "utf-8")


# 获取变长字符串
def recv_all_string(_conn):
    # 获取消息长度
    length = int.from_bytes(_conn.recv(4), byteorder='big')
    b_size = 3 * 1024  # 此处是因为utf8编码中汉字占3字节，英文占1字节
    times = math.ceil(length / b_size)
    content = ''
    for i in range(times):
        if i == times - 1:
            seg_b = _conn.recv(length % b_size)
        else:
            seg_b = _conn.recv(b_size)
        content += str(seg_b, encoding='utf-8')
    return content


# 校验用户名密码
def check_user(user, key):
    print("login:\n user: " + user + ", key: " + key)
    found_user = False
    
    user_or_key = True
    
    with open("userdata\\user.txt", 'r', encoding="utf-8") as user_data:
        for line in user_data:
            line = line.replace("\n", "")

            #先找到该用户
            if (user_or_key and line == user):
                found_user = True
            #再检查该用户的密码
            elif (not user_or_key) and found_user:
                return line == key

            user_or_key = not user_or_key
    return False


def add_user(user, key):
    try:
        print("register: user: " + user + ", key: " + key)
        
        with open("userdata\\user.txt", 'r', encoding="utf-8") as user_data:
            user_or_key = True
            for line in user_data:
                line = line.replace("\n", "")
                if user_or_key and line == user:
                    # 用户名存在
                    return "1"
                user_or_key = not user_or_key
        # 添加用户和密码
        with open("userdata\\user.txt", 'a', encoding="utf-8") as user_data:
            user_data.write(user + "\n")
            user_data.write(key + "\n")
        return "0"
    except Exception as e:
        print("adding user's data failed：" + str(e))
        return "2"


# 处理刷新列表的请求
def handle_online_list(_conn, addr):
    print("online_conn.__len__()=" + str(online_conn.__len__()))
    print("conn2user.__len__()=" + str(conn2user.__len__()))
    for con in online_conn:
        send_string_with_length(con, "#!onlinelist#!")
        # 先发送列表人数
        send_number(con, online_conn.__len__())
        for c in online_conn:
            send_string_with_length(con, conn2user[c])
    return True


# 处理登录请求
def handle_login(_conn, addr):
    user = recv_all_string(_conn)
    key = recv_all_string(_conn)
    check_result = check_user(user, key)
    if check_result:
        _conn.sendall(bytes("1", "utf-8"))
        conn2user[_conn] = user
        online_conn.append(_conn)
        handle_online_list(_conn, addr)
    else:
        _conn.sendall(bytes("0", "utf-8"))
    return True


# 处理注册请求
def handle_register(_conn, addr):
    user = recv_all_string(_conn)
    key = recv_all_string(_conn)
    _conn.sendall(bytes(add_user(user, key), "utf-8"))
    return True


# 处理消息发送请求
def handle_message(_conn, addr):
    content = recv_all_string(_conn)
    print(content)
    # 发送给所有在线客户端
    for client in online_conn:
        # 先发一个字符串告诉客户端接下来是消息
        
        send_string_with_length(client, "#!message#!")
        send_string_with_length(client, conn2user[_conn])
        send_string_with_length(client, content)

    return True

# 处理消息私聊
def handle_private(_conn, addr):
    content = recv_all_string(_conn)
    content2=content[content.rfind("#!"):content.rfind('!#')]
    send_to=content2[2:]
    

    send_from=conn2user[_conn]
    content3=content[content.rfind('!#'):]
    content4=content3[2:]
    msg="来自"+send_from+"的私聊： "+content4

    
    for client in online_conn:
        # 先发一个字符串告诉客户端接下来是消息
        
        if(conn2user[client]==send_to):
            send_string_with_length(client, "#!message#!")
            send_string_with_length(client, conn2user[_conn])
            send_string_with_length(client, msg)

    return True

# 处理请求线程的执行方法
def transaction(_conn, addr):
    try:
        while True:
            # 获取请求类型
            transac_type = str(_conn.recv(1), "utf-8")
            # 是否继续处理
            result = True
            if transac_type == "1":  # 处理登录请求
                print("handle_login")
                result = handle_login(_conn, addr)
            elif transac_type == "2":  # 处理注册请求
                print("handle_register")
                result = handle_register(_conn, addr)
            elif transac_type == "3":  # 处理发送消息
                print("handle_message")
                result = handle_message(_conn, addr)
            elif transac_type == "4":  # 发送在线好友列表
                print("handle_online_list")
                result = handle_online_list(_conn, addr)
            elif transac_type == "5":  # 发送在线好友列表
                print("handle_private")
                result = handle_private(_conn, addr)
            if not result:
                break
    except Exception as e:
        print(str(addr) + " exception throwed, disconnecting: " + str(e))
    finally:
        try:
            _conn.close()
            online_conn.remove(_conn)
            conn2user.pop(_conn)
            handle_online_list(_conn, addr)
        except:
            print(str(addr) + " Connection closing error")


# main
if __name__ == "__main__":
    try:
        cf=configparser.ConfigParser()
        cf.read("userdata\\config.ini")
        secs=cf.sections()
        opts=cf.options("sec_a")
        items=cf.items("sec_a")
        val=cf.get("sec_a","server_ip")

        sk = socket.socket()
        sk.bind((val, 8080))
    
        # 最大挂起客户数
        sk.listen(10)
        print("server set up, listening...")
        while True:
            conn, addr = sk.accept()
            #交给线程处理
            Thread(target=transaction, args=(conn, addr)).start()
    except Exception as e:
        print("exception throwed: " + str(e))
