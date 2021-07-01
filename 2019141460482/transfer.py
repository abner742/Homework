import json
import socket
import zipfile
import os,sys


class Transfer:

    def __init__(self, config):
        self.__server_socket = socket.socket()
        self.__self_ip = config.get_self_ip()
        self.__self_command_port = config.get_self_command_port()
        self.__self_data_port = config.get_self_data_port()
        self.__neighbor_socket = config.get_neighbor_socket()
        self.__share_path = config.get_share_path()
        self.__root_path = config.get_root_path()

    def __del__(self):
        self.__server_socket.close()

    def listen_data_port(self, max_connect=5):
        try:
            self.__server_socket.bind((self.__self_ip, self.__self_data_port))
            self.__server_socket.listen(max_connect)
        except:
            print('OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。请关闭冲突程序。Enter any key to exit')
            input()
            sys.exit(-1)

    def send_download_file_request(self,request_msg):
        client_socket = socket.socket()
        if client_socket.connect((request_msg['target_ip'], request_msg['target_data_port'])) != socket.error:
            client_socket.send(json.dumps(request_msg).encode('utf-8'))
            self.__recv_file(client_socket)
        else:
            print('Can not connect ' + str(request_msg))
        client_socket.close()

    def recv_download_file_request(self):
        while True:
            client_socket, client_addr = self.__server_socket.accept()
            recv_msg = client_socket.recv(1024).decode('utf8')
            recv_dict = json.loads(recv_msg)
            self.__send_file(client_socket, recv_dict['filename'])
            client_socket.close()

    def __send_file(self, server_socket, filename):
        zip_path = self.__root_path + '/' + filename + '.zip'
        for root, dirs, files in os.walk(self.__share_path):  # path 为根目录
            if filename in dirs:
                filepath = root.replace('\\', '/') + '/' + filename
                file_zip = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
                for root_path, dir_names, filenames in os.walk(filepath):
                    file_path = root_path.replace(filepath, '')
                    for file in filenames:
                        file_zip.write(os.path.join(root_path, file), os.path.join(file_path, file))
                file_zip.close()
            elif filename in files:
                filepath = root.replace('\\', '/') + '/' + filename
                file_zip = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
                file_zip.write(os.path.join(root, filename),filename)
                file_zip.close()
        zip_size = os.path.getsize(zip_path)
        zip_msg = {'filename': filename, 'file_size': zip_size}
        server_socket.send(json.dumps(zip_msg).encode('utf-8'))
        with open(zip_path, 'rb') as zip_file:
            zip_data = zip_file.read()
            server_socket.sendall(zip_data)
        os.remove(zip_path)

    def __recv_file(self, client_socket):
        zip_msg = json.loads(client_socket.recv(1024).decode('utf-8'))
        recv_size = 0
        print(json.dumps(zip_msg))
        zip_path = self.__share_path+'/'+zip_msg['filename'] + '.zip'
        zip_file = open(zip_path, 'wb')
        while recv_size < zip_msg['file_size']:
            if zip_msg['file_size'] - recv_size > 1024:
                recv_buffer = client_socket.recv(1024)
                recv_size += 1024
            else:
                recv_buffer = client_socket.recv(zip_msg['file_size']-recv_size)
                recv_size += zip_msg['file_size']-recv_size
            zip_file.write(recv_buffer)
        zip_file.close()
        zip_file = zipfile.ZipFile(zip_path,'r', zipfile.ZIP_DEFLATED)
        file_dir = self.__share_path+'/'+zip_msg['filename']
        if os.path.isdir(file_dir):
            pass
        else:
            try:
                os.mkdir(file_dir)
            except FileExistsError:
                file_dir = self.__share_path
                pass
        for names in zip_file.namelist():
            zip_file.extract(names, path=file_dir)
        zip_file.close()
        os.remove(zip_path)
