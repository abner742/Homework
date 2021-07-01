import peer_config
import flooding_query
import transfer
from threading import Thread
from queue import Queue,Empty
import sys



class UserInterface:

    def __init__(self):
        self.config = peer_config.Config()
        self.config .read_config('config.json')

        self.flooding = flooding_query.FloodingQuery(self.config)
        self.flooding.listen_command_port()
        self.transfers = transfer.Transfer(self.config)
        self.transfers.listen_data_port()

        self.transfer_thread = Thread(target=self.transfers.recv_download_file_request)
        self.transfer_thread.start()

        self.request_queue = Queue()
        self.flooding_thread = Thread(target=self.flooding.recv_buffer, args=(self.request_queue,))
        self.flooding_thread.start()

        self.__menu()

    def __menu(self):
        print("Flooding Query Ver 1.0")
        print("User: "+self.config.get_self_id())
        print("Type‘help’for more information.")
        while True:
            print(">>>", end=" ")
            command = input()
            if command == 'help':
                print('COMMAND')
                print('\t ipconfig. . . . . . . . . . . .:  get host peer ipconfig')
                print('\t search [filename]. . . . . . . :  search target file online (filename only)')
                print('\t exit. . . . . . . . . . . .. . :  exit program')
            elif command == 'ipconfig':
                print("Peer IP config\n")
                print("\tIP Address. . . . . . . . . . . .:  "+self.config.get_self_ip())
                print("\tCommand Port. . . . . . . . . . .:  "+str(self.config.get_self_command_port()))
                print("\tData Port. . . . . . . . . . . . :  "+str(self.config.get_self_data_port()))
            elif 'search' in command:
                try:
                    filename = command.split(' ')[1]
                    self.flooding.query_online(filename)
                    try:
                        flooding_result = self.request_queue.get(timeout=3)
                        print('Get file \''+filename+'\' in \n\tIP:'+flooding_result['target_ip']+' \n\tCommand Port:'
                              + str(flooding_result['target_command_port'])+' \n\tData Port:' +
                              str(flooding_result['target_data_port']))
                        print('Download this file or not?(Y/N)',end="")
                        choose = input()
                        if choose == 'Y' or choose == 'y':
                            try:
                                self.transfers.send_download_file_request(flooding_result)
                                print('Success download this file in '+self.config.get_share_path())
                            except:
                                print('Download failed.Please Try again.')
                        else:
                            print('Cancel download this file.')
                    except Empty:
                        print(filename + ' not exist online.')
                except IndexError:
                    print('Error Input. Example: search [filename]')
            elif command == 'exit':
                print("Bye.Enter any key to exit.")
                input()
                sys.exit(-1)
            else:
                print('Invalid input.')


if __name__ == '__main__':
    UserInterface()




