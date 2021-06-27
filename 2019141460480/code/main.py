import multiprocessing as mp
import os
import process
import config
import time
import judge

if __name__ == '__main__':
    attr_num = 7
    peer_num = config.Config().get_peer_num()
    # 如果不加这一句，Python多进程multiprocessing在windows的Dos或者idle下运行不了会报错
    mp.freeze_support()
    print()
    print("Query-flooding-based Resource Sharer by LHL")
    while True:
        print()
        print('**********************************')
        while True:
            role = input(">请输入peer的序号:")
            if judge.is_number(role):
                if 0 <= int(role) < int(peer_num):
                    break
                else:
                    print("请输入存在的peer的序号！(如果不知道可以再config.ini里查看)")
            else:
                print("请输入数字！(如果不知道可以再config.ini里查看)")
        opt = input(">请输入选项(如果不知道可以输入help):")
        print()
        if opt.split()[0] == 'get':
            print('Parent process %s.' % os.getpid())
            p = mp.Pool(7)
            for i in range(peer_num):
                # 服务器初始化
                p.apply_async(process.tcp_server, args=(i,))
            print('Waiting for all subprocesses done...')
            time.sleep(1)
            # 创建查询并下载文件的进程
            temp = mp.Process(target=process.tcp_client, args=(role, opt.split()[1]))
            temp.start()
            temp.join()
            # 在我的电脑上，15秒是完全足够的（如果不行可以增加等待时间）
            time.sleep(15)
            p.terminate()
            p.join()
            print('All subprocesses done.')
        elif opt.split()[0] == 'config':
            with open("config.ini", 'r') as f:
                line_num = 0
                while True:
                    line = f.readline()
                    line_num += 1
                    if attr_num * int(role) <= line_num <= attr_num * int(role) + 6:
                        print(line, end="")
                    if line_num > attr_num * int(role) + 6:
                        break
        elif opt.split()[0] == 'modify':
            mod_conf = config.Config()
            attr_mod = mod_conf.get_attr(role)
            mod_conf.set_attr(role, attr_mod)
            if opt.split()[1] == 'ip':
                attr_mod['ip_addr'] = opt.split()[2]
            elif opt.split()[1] == 'serverport':
                attr_mod["server_port"] = opt.split()[2]
            elif opt.split()[1] == 'clientport':
                attr_mod['client_port'] = opt.split()[2]
            elif opt.split()[1] == 'sharedir':
                attr_mod['share_dir'] = opt.split()[2]
            elif opt.split()[1] == 'peerlist':
                attr_mod['peer_list'] = opt.split()[2].split('/')
                print(attr_mod['peer_list'])
                attr_mod['peer_list'] = [int(i) for i in attr_mod['peer_list']]
            else:
                print("Input Error. Please check again.")
            print(mod_conf.set_attr(role, attr_mod))
        elif opt.split()[0] == 'help':
            with open("help.txt", 'r', encoding='utf-8') as f:
                while True:
                    line = f.readline()
                    print(line, end="")
                    if not line:
                        break
        elif opt.split()[0] == 'exit':
            print("再见！")
            exit()
        else:
            print("Invalid input. Please check your input again.")
