import json
import ipaddress
import sys,os


class Config:
    def __init__(self):
        self.__self_id = str()
        self.__self_ip = str()
        self.__self_command_port = int()
        self.__self_data_port = int()
        self.__neighbor_socket = []
        self.__share_path = str()
        self.__root_path = os.getcwd()

    def read_config(self, path):
        try:
            config_file = open(path, 'r', encoding='utf8')
            config_json = json.load(config_file)
            self.__self_id = config_json['self_configs']['peer_id']
            self.__self_ip = config_json['self_configs']['peer_ip']
            self.__self_command_port = config_json['self_configs']['peer_command_port']
            self.__self_data_port = config_json['self_configs']['peer_data_port']
            self.__share_path = config_json['share_path']
            for neighbor in config_json['neighbor_configs']:
                self.__neighbor_socket.append(neighbor)
        except:
            print("Failed to read json config.Enter any key to exit.")
            input()
            sys.exit(-1)

    def get_self_id(self):
        return self.__self_id

    def get_self_ip(self):
        if ipaddress.ip_address(self.__self_ip):
            return self.__self_ip
        else:
            print("Invalid ip address.Enter any key to exit.")
            input()
            sys.exit(-1)

    def get_self_command_port(self):
        if 1024 <= self.__self_command_port <= 65355:
            return self.__self_command_port
        else:
            print("Invalid command port.Enter any key to exit.")
            input()
            sys.exit(-1)

    def get_self_data_port(self):
        if 1024 <= self.__self_data_port <= 65355:
            return self.__self_data_port
        else:
            print("Invalid data port.Enter any key to exit.")
            input()
            sys.exit(-1)

    def get_neighbor_socket(self):
        for neighbor in self.__neighbor_socket:
            if ipaddress.ip_address(neighbor['peer_ip']) and 1024 <= neighbor['peer_command_port'] <= 65355 and \
                    1024 <= neighbor['peer_data_port'] <= 65355:
                continue
            else:
                print("Invalid peer socket.Enter any key to exit.")
                input()
                sys.exit(-1)
        return self.__neighbor_socket

    def get_share_path(self):
        return self.__share_path

    def get_root_path(self):
        return self.__root_path