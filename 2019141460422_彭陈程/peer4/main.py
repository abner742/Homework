import threading
from client import client
from listen import listen_query
from listen import listen_download

def main():
    client_thread=threading.Thread(target=client)
    udp_query_thread=threading.Thread(target=listen_query)
    tcp_download_thread=threading.Thread(target=listen_download)

    client_thread.start()
    udp_query_thread.start()
    tcp_download_thread.start()

if __name__=='__main__':
    main()


