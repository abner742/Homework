import socket
import json
import os,sys
import time


class FloodingQuery:

    def __init__(self, config):
        self.__server_socket = socket.socket()
        self.__self_ip = config.get_self_ip()
        self.__self_command_port = config.get_self_command_port()
        self.__self_data_port = config.get_self_data_port()
        self.__neighbor_socket = config.get_neighbor_socket()
        self.__share_path = config.get_share_path()
        self.__last_recv = {"filename": str(), "query_time": float()}

    def __del__(self):
        self.__server_socket.close()

    def listen_command_port(self, max_connect=5):
        try:
            self.__server_socket.bind((self.__self_ip, self.__self_command_port))
            self.__server_socket.listen(max_connect)
        except:
            print('OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。请关闭冲突程序。Enter any key to exit')
            input()
            sys.exit(-1)

    def query_online(self, filename):
        query_msg = {}
        query_msg['is_query'] = True
        query_msg['filename'] = filename
        query_msg['request_ip'] = self.__self_ip
        query_msg['request_command_port'] = self.__self_command_port
        query_msg['request_data_port'] = self.__self_data_port
        query_msg['pass_peer'] = []
        query_msg['query_time'] = time.time()
        self.__send_query_buffer(query_msg)

    def recv_buffer(self, result_queue):
        while True:
            client_socket, client_addr = self.__server_socket.accept()
            recv_msg = client_socket.recv(1024).decode('utf8')
            recv_dict = json.loads(recv_msg)
            if recv_dict['is_query']:
                if self.__local_query(recv_dict['filename']):
                    self.__send_result_buffer(recv_dict)
                    print(recv_msg+' find')
                else:
                    self.__send_query_buffer(recv_dict)
                    print(recv_msg + 'not find')
            else:
                if self.__last_recv['filename'] == recv_dict['filename'] and self.__last_recv['query_time'] == \
                        recv_dict['query_time']:
                    continue
                self.__last_recv['filename'] = recv_dict['filename']
                self.__last_recv['query_time'] = recv_dict['query_time']
                result_queue.put(recv_dict)  # 生产者消费者模式，当获取到结果时生产数据加入queue，user_interface处queue负责消费数据
                print(recv_msg + ' result')
            client_socket.close()

    def __local_query(self, filename):
        for root, dirs, files in os.walk(self.__share_path):  # path 为根目录
            if filename in dirs or filename in files:
                return True
        return False

    def __send_query_buffer(self, query_msg):  # 向周围邻居发起洪泛
        for neighbor in self.__neighbor_socket:
            if neighbor not in query_msg['pass_peer']:
                query_msg['pass_peer'].append(neighbor)
                client_socket = socket.socket()
                try:
                    client_socket.connect((neighbor['peer_ip'],neighbor['peer_command_port']))
                    client_socket.send(json.dumps(query_msg).encode('utf-8'))
                except:
                    print('Can not connect '+str(neighbor))
                client_socket.close()

    def __send_result_buffer(self, recv_dict):
        result_msg = {}
        result_msg['is_query'] = False
        result_msg['filename'] = recv_dict['filename']
        result_msg['query_time'] = recv_dict['query_time']
        result_msg['target_ip'] = self.__self_ip
        result_msg['target_command_port'] = self.__self_command_port
        result_msg['target_data_port'] = self.__self_data_port
        client_socket = socket.socket()
        try:
            client_socket.connect((recv_dict['request_ip'], recv_dict['request_command_port']))
            client_socket.send(json.dumps(result_msg).encode('utf-8'))
        except:
            print('Can not connect ' + self.__self_ip + self.__self_command_port)
        client_socket.close()
