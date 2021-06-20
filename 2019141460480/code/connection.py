import socket
import threading
import os
import struct
import json
import config
import zipfile
import filemd5
import time


class Connection:
    # 自身属性
    __num = None
    __ip_addr = None
    __server_port = None
    __client_port = None
    __peer_list = None
    __share_dir = None
    __peer_num = 0
    __query_res = dict()
    __path_list = dict()
    __request_flag = dict()
    # 当前对等方所有邻居的信息
    __peer_attr = []
    # 服务器端收到的命令
    __cmd = []

    __source_ip = None
    __source_port = None

    def set_num(self, num):
        self.__num = int(num)

    def set_ip(self, ip_addr):
        self.__ip_addr = ip_addr

    def set_server_port(self, server_port):
        self.__server_port = int(server_port)

    def set_client_port(self, client_port):
        self.__client_port = int(client_port)

    def set_peer_list(self, peer_list):
        self.__peer_list = peer_list

    def set_share_dir(self, share_dir):
        self.__share_dir = share_dir

    # 该函数的作用是查询根目录root下是否包含filename文件，是一个递归查询
    def query(self, root, filename):
        items = os.listdir(root)
        for item in items:
            path = os.path.join(root, item)
            # windows的分隔符要注意转义
            if path.split('\\')[-1] == filename or path.split('/')[-1] == filename:
                self.__query_res[filename] = 1
                self.__path_list[filename] = path
            elif os.path.isdir(path):
                self.query(path, filename)

    # 要处理的是“get”、“found”和“request”三个类型的msg，分别代表“文件查询请求”、“文件已找到”和“文件传输请求”
    def tcp_handler(self, conn, addr):
        while True:
            try:
                res = conn.recv(1024)

                # 格式为：[[ordertype], [filename], [port], [ip], [ttl]]

                if not res:
                    continue
                else:
                    self.__cmd = res.decode('utf-8').split()

                    if self.__cmd[0] == 'get':
                        res = self.update_ttl(res)
                        self.__source_port = self.__cmd[2]
                        self.__source_ip = self.__cmd[3]
                        self.__query_res[self.__cmd[1]] = 0
                        self.query(self.__share_dir, self.__cmd[1])
                        # print("%s: 本地查询 %s" % (self.__num, self.__cmd[1]))

                        # 本地未找到，查询邻居节点
                        if self.__query_res[self.__cmd[1]] == 0:
                            if int(self.__cmd[-1]) >= 0:
                                # print("%s: 本地未找到, 查询邻居节点" % self.__num)
                                for i in self.__peer_attr:
                                    if i['server_port'] == self.__cmd[2]:
                                        continue
                                    else:
                                        # print("%s: 查询邻居" % self.__num)
                                        self.tcp_client_notice(i['ip_addr'], i['server_port'], res)
                            else:
                                # print("Over ttl!")
                                pass

                        # 本地找到，向请求源server发送成功消息
                        else:
                            msg = "found %s at %s %s %s" % (
                                self.__cmd[1], self.__num, self.__ip_addr, self.__server_port)
                            self.tcp_client_notice(self.__source_ip, self.__source_port, msg)

                    # 收到“found filename at x [ip] [port]”消息，即向x的server发送请求
                    elif self.__cmd[0] == 'found':
                        self.__source_ip = self.__cmd[4]
                        self.__source_port = self.__cmd[5]
                        msg = 'request %s %s %s' % (self.__cmd[1], self.__ip_addr, self.__server_port)
                        self.tcp_client_notice(self.__source_ip, self.__source_port, msg)

                    # 收到“request filename [ip] [port]”消息，即向请求源发送文件
                    elif self.__cmd[0] == 'request':
                        self.__request_flag[self.__cmd[1]] = 1
                        self.__send(conn, self.__cmd[1])

                    # 过滤其它命令
                    else:
                        msg = "不合理的内容！"
                        conn.send(msg.encode())

            except ConnectionResetError:
                print("connect abort")
                break
        # conn.close()

    def tcp_server(self):
        # 参数说明：socket.AF_INET:服务器间网络通信, socket.SOCK_STREAM:流式socket(for TCP), socket.SOL_SOCKET:基本套接口，
        # socket.SO_REUSEADDR:允许重用本地地址和端口
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind(("", self.__server_port))
        tcp_server.listen(5)
        print(self.__server_port, "OK")
        while True:
            try:
                conn, addr = tcp_server.accept()
            except ConnectionAbortedError:
                print("server except")
                continue
            t = threading.Thread(target=self.tcp_handler, args=(conn, addr))
            # 这里为了防止线程处理不过来，所以加了等待
            time.sleep(0.3)
            t.start()

    def __send(self, conn, filename):
        true_name = filename
        filepath = self.__path_list[filename]
        if filename.find('.') != -1:
            filename = filename[0:filename.find('.')] + ".zip"
        else:
            filename = filename + ".zip"
        z = zipfile.ZipFile(filename, 'w')
        if os.path.isdir(filepath):
            for d in os.listdir(filepath):
                z.write(filepath + os.sep + d, d)
        else:
            z.write(filepath, true_name)
        z.close()

        header_dic = {
            'filename': filename,
            'md5': filemd5.get_file_md5(filename),
            'file_size': z.infolist()[0].file_size
        }
        header_json = json.dumps(header_dic)
        header_bytes = header_json.encode('utf-8')

        # 打包文件头
        conn.send(struct.pack('i', len(header_bytes)))

        # 发送头
        conn.send(header_bytes)

        # 发送数据
        send_size = 0
        with open(filename, 'rb') as f:
            for b in f:
                conn.send(b)
                send_size += len(b)
        while True:
            try:
                os.remove(filename)
                break
            except:
                continue

    def __save(self, conn):
        obj = conn.recv(4)
        header_size = struct.unpack('i', obj)[0]
        # 接收头
        header_bytes = conn.recv(header_size)

        # 解包头
        header_json = header_bytes.decode('utf-8')
        header_dic = json.loads(header_json)
        total_size = header_dic['file_size']
        filename = header_dic['filename']
        cur_md5 = header_dic['md5']

        # 接收数据
        with open('%s%s' % (self.__share_dir, filename), 'wb') as f:
            recv_size = 0
            while recv_size < total_size:
                res = conn.recv(1024)
                f.write(res)
                recv_size += len(res)
            print("total size: %s, already downloaded: %s" % (total_size, recv_size))
        if filemd5.compare_file_md5('%s%s' % (self.__share_dir, filename), cur_md5) == 1:
            z = zipfile.ZipFile("%s%s" % (self.__share_dir, filename), 'r')
            z.extractall("%s" % self.__share_dir)
            z.close()
        else:
            print("file corrupt during transmission")
        while True:
            try:
                os.remove("%s%s" % (self.__share_dir, filename))
                break
            except:
                continue

    def tcp_client_notice(self, ip, port, msg):
        time.sleep(0.1)
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((ip, int(port)))
        tcp_client.send(msg.encode())

        if msg.split()[0] == 'request':
            self.__save(tcp_client)
        tcp_client.shutdown(2)
        tcp_client.close()

    def update_peer_attr(self):
        conf = config.Config()
        l1 = []
        for i in self.__peer_list:
            l1.append(conf.get_attr(i))
            self.__peer_num += 1
        self.__peer_attr = l1
        return self.__peer_attr

    @staticmethod
    # ttl减1，以防止循环查询等引起网络拥塞
    def update_ttl(msg):
        msg = msg.decode().split()
        msg[-1] = str(int(msg[-1]) - 1)
        new_msg = " ".join(msg)
        return new_msg

    def get_peer_num(self):
        return self.__peer_num

    def get_peer_list(self):
        return self.__peer_list

    def get_num(self):
        return self.__num
