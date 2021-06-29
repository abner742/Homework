#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import threading

from search import search
from client import client
from listen import listen_query
from listen import listen_get


def main():
    client_thread = threading.Thread(target=client)
    udp_thread = threading.Thread(target=listen_query)
    tcp_thread = threading.Thread(target=listen_get)
    client_thread.start()
    udp_thread.start()
    tcp_thread.start()
    

if __name__ == "__main__":
    main()
