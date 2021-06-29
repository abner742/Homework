import configparser
import ipaddress
import os


class Config:
    __cf = configparser.ConfigParser()
    __ttl = 0

    def __init__(self):
        self.__cf.read("config.ini")
        self.__ttl = 4

    def get_ttl(self):
        return self.__ttl

    @staticmethod
# 每个peer有6行，还有1行空格
    def get_peer_num():
        with open("config.ini", "r") as f:
            count = 0
            for line in f:
                count += 1
        return int((count + 1) / 7)

    def get_attr(self, i):
        """
        参数i: 要获取的peer的序号
        返回值: dict {'ip_addr': ip, 'server_port': server_port, 'client_port': client_port,
        'share_dir': share_dir, 'peer_list': peer_list}
        """
        while True:
            try:
                peer = dict()
                peer['ip_addr'] = self.__cf.get("Peer-%s" % i, "ip_addr")
                peer['server_port'] = self.__cf.get("Peer-%s" % i, "server_port")
                peer['client_port'] = self.__cf.get("Peer-%s" % i, "client_port")
                peer['share_dir'] = self.__cf.get("Peer-%s" % i, "share_dir")
# 以下操作是为了去掉peer_list中的单引号
                peer_str = self.__cf.get("Peer-%s" % i, "peer_list")
                peer_str = peer_str[1:len(peer_str) - 1]
                peer_list = peer_str.split(', ')
# 如果peer_list为空，则不执行任何操作，否则执行else里的语句
                if not peer_list:
                    for i in range(len(peer_list)):
                        peer_list[i] = int(peer_list[i])
                else:
                    peer_list = [int(i) for i in peer_list]
                peer['peer_list'] = peer_list
                break
            except:
                pass
        return peer

# 这个函数首先判断新值是否与旧值一样，以及是否冗余；如果不一样且不冗余就调用modify方法进行修改
    def set_attr(self, i, new_attr):
        """
        参数i: 要判断的peer的序号
        参数new_attr: 新的peer
        返回值: modify info
        """
        self.__init__()
# 将原来的peer与新的进行比较
        old_attr = self.get_attr(i)
        diff_val = [(k, old_attr[k], new_attr[k]) for k in old_attr if old_attr[k] != new_attr[k]]
        if not diff_val:
            return "没有找到与原来不同的地方！"
        for t in diff_val:
            temp = []
            for j in range(self.get_peer_num()):
                temp1 = self.get_attr(j)
                temp.append(temp1[t[0]])

            if t[2] in temp:
                return "%s冗余！" % t[0]

            if t[0] == 'ip_addr':
                if not ipaddress.ip_address(t[2]):
                    return "不合理的ip_addr！"
            elif t[0] == 'share_dir':
                if not os.path.isdir(t[2]):
                    return "不合理的share_dir！"
# 如果路径最后不是以分隔符结束，则添上分隔符；
# os.sep表示根据操作系统所选择的分隔符（windows和linux下分隔符是不同的，前者是'\'，后者是'/'）
                if t[2][-1] != os.sep:
                    t[2] += os.sep
        print("将会修改的是（属性名，旧值，新值）：")
        print(diff_val)
        self.modify(i, new_attr)
        return "修改成功！"

    @staticmethod
    def modify(i, new_attr):
        """
        参数i: 要修改的peer的序号
        参数new_attr: 新的peer
        返回值: modify info
        """
        data = ""
        flag = 0
# peer里的peer_list属性需要转换类型，其他属性不需要
        new_attr["peer_list"] = str(new_attr["peer_list"])
        with open("config.ini", "r") as f:
            for line in f:
                if flag > 0:
                    flag -= 1

                if "Peer-%s" % i in line:
                    flag = 6

                if flag == 5:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], new_attr["ip_addr"])
                elif flag == 4:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], new_attr["server_port"])
                elif flag == 3:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], new_attr["client_port"])
                elif flag == 2:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], new_attr["share_dir"])
                elif flag == 1:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], new_attr["peer_list"])

                data += line
        with open("config.ini", "w") as f:
            f.write(data)








