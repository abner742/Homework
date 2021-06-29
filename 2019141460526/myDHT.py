import socket
import codecs
import time
from time import sleep
from threading import Thread
from hashlib import sha1 #sha1哈希
from random import randint #随机生成整数
from collections import deque
import logging #日志
from struct import unpack #解包
from socket import inet_ntoa #提取网络层数据时对IP地址输出转换为点十分地址
import bencoder

#线程数
THREAD_NUMBER = 3
#host
SERVER_HOST = "0.0.0.0"
#端口
SERVER_PORT = 9090
#UDP报文缓冲区大小
UDP_RECV_BUFFSIZE = 65535
#每个节点长度，node = node_id(20位) + node_ip(4位) + node_port(2位)
PEER_NODE_LEN = 26
#节点 id 长度
PEER_NID_LEN = 20
#节点 id 和 ip 长度
PEER_NID_NIP_LEN = 24
#构造邻居随机结点
NEIGHBOR_END = 14
#双端队列容量
MAX_NODE_QSIZE = 10000
#磁力链接前缀
MAGNET_PER = "magnet:?xt=urn:btih:{}"
#执行bootstrap定时器间隔（秒）
PEER_SEC_BS_TIMER = 8
#接受udp等待时间
SLEEP_TIME1 = 1e-5
#线程持续时间
SLEEP_TIME2 = 60*10 #1min以上较好

#tracker
BOOTSTRAP_NODES = [
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://retracker.lanta-net.ru:2710/announce",
    "udp://bt.xxx-tracker.com:2710/announce",
    "http://retracker.telecom.by:80/announce",
    "http://retracker.mgts.by:80/announce",
    "https://tracker.nanoha.org:443/announce",
    "https://tracker.nitrix.me:443/announce",
    ("router.bittorrent.com", 6881),
    ("dht.transmissionbt.com", 6881),
    ("router.utorrent.com", 6881)
]

stdger = logging.getLogger("std_log")#终端
fileger = logging.getLogger("file_log")#文件

#日志实例初始化
def initialLog():
    stdLogLevel = logging.DEBUG
    fileLogLevel = logging.DEBUG
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    file_handler = logging.FileHandler("HASH.log")
    file_handler.setFormatter(formatter)
    logging.getLogger("file_log").setLevel(fileLogLevel)
    logging.getLogger("file_log").addHandler(file_handler)
    logging.getLogger("std_log").setLevel(stdLogLevel)
    logging.getLogger("std_log").addHandler(stdout_handler)


#生成随机的node id，长度为20位
#Kad DHT中取160-bit哈希空间来作为node id,sha1算法生成的值是长度是20byte即20*8=160bit,可以容纳2^160个节点
#实际上Bittorent下node id也是种子文件的InfoHash,对等双方的node id和info hash存在映射关系
#20byte=40个十六进制字符,infohash在磁力链接中以40个十六进制字符形式存在
#通过sha1生成node ID,返回摘要作为二进制数据字符流值(这里node id直接通过urandom生成，非十六进制)
def entropy(length):
    chars = []
    for i in range(length):
        chars.append(chr(randint(0, 255)))
    return "".join(chars)

def get_rand_id():
    hash = sha1()
    random = entropy(PEER_NID_LEN) #随机结点
    input = "12345678910111211314151617181920" #指定结点
    hash.update(random.encode("utf-8"))
    return hash.digest()

#生成随机target(目标节点 id)周边节点 id，在 Kademlia 网络中，距离是通过异或(XOR)计算的，
#结果为无符号整数,distance(A, B) = |A xor B|,值越小表示越近。
#这里以前缀匹配的方式表示,计算距离近的node id目标节点0-NEIGHBOR_END位+加上自身节点NEIGHBOR_END-末位
#NEIGHBOR_END取10-15,这样伪装成target的周边节点按规则每个节点对周边节点的感知能力较好,很可能将你记录在它的路由表上,使得它自己或引导其他节点主动向你通信
def get_neighbor(target):
    return target[:NEIGHBOR_END] + get_rand_id()[NEIGHBOR_END:]

#解析find_node回复中nodes节点的信息
def get_nodes_info(nodes):
    length = len(nodes)
    if (length % PEER_NODE_LEN) != 0:
        return []
    for i in range(0, length, PEER_NODE_LEN):
        nid = nodes[i : i + PEER_NID_LEN]
        #利用 inet_ntoa 可以返回节点 ip
        ip = inet_ntoa(nodes[i + PEER_NID_LEN : i + PEER_NID_NIP_LEN])
        #解包返回节点端口
        port = unpack("!H", nodes[i + PEER_NID_NIP_LEN : i + PEER_NODE_LEN])[0]
        yield (nid, ip, port)

#结点
class HNode:
    def __init__(self, nid, ip=None, port=None):
        self.nid = nid
        self.ip = ip
        self.port = port

#DHT服务
class DHT(Thread):
    def __init__(self, bind_ip, bind_port, process_id, master):
        Thread.__init__(self)
        self.isWorking = True
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.process_id = process_id
        self.nid = get_rand_id()
        #没有实现包含K桶的完整路由表,为了认识更多的节点向node发送一次find_node请求之后即可删除该数据,构造为双端队列
        self.nodes = deque(maxlen=MAX_NODE_QSIZE)
        #KRPC协议是由bencode编码组成的一个简单的 RPC结构，使用 UDP 报文发送。
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        #UDP地址绑定
        self.udp.bind((self.bind_ip, self.bind_port))
        #多线程
        self.sfnf_thread = Thread(target=self.send_find_node_forever)
        self.rrf_thread = Thread(target=self.receive_response_forever)
        self.bst_thread = Thread(target=self.bs_timer)
        self.master = master

    #利用 tracker服务器，伪装成DHT节点，加入DHT网络
    def bootstrap(self):
        for address in BOOTSTRAP_NODES:
            self.send_find_node(address)

    #定时执行 bootstrap()
    def bs_timer(self):
        t = 1
        while True:
            if t % PEER_SEC_BS_TIMER == 0:
                t = 1
                self.bootstrap()
            t += 1
            time.sleep(1)

    #发送krpc协议,msg:发送UDP报文信息,address:发送地址即(ip, port)元组
    def send_krpc(self, msg, address):
        try:
            # msg要经过bencode编码
            self.udp.sendto(bencoder.bencode(msg), address)
        except:
            pass

    #发送错误回复
    def send_error(self, tid, address):
        msg = dict(t=tid, y="e", e=[202, "Server Error"])
        self.send_krpc(msg, address)

    #发送find_node请求
    #find_node被用来查找给定node id的节点的联系信息。这时 KPRC 协议中的"q" == "find_node"。
    #find_node请求包含2个参数，第一个参数是id包含了请求节点的node id;第二个参数是target包含了请求者正在查找的节点的node id
    #当一个节点接收到了find_node的请求，它应该给出对应的回复：回复中包含2个关键字id和nodes
    #nodes是字符串类型，包含了被请求节点的路由表中最接近目标节点的K(8)个最接近的节点的联系信息。
    def send_find_node(self, address, nid=None):
        nid = get_neighbor(nid) if nid else self.nid #如果nid不存在则为本身的nid;将自己的node id构造成被请求节点的(按异或)相近node id
        tid = get_rand_id()
        msg = dict(
            t=tid,
            y="q",
            q="find_node",  #指定请求为find_node
            a=dict(id=nid, target=get_rand_id()),
        )
        self.send_krpc(msg, address)

    #循环发送find_node请求(DHT-Client),即不断让其他结点认识你
    def send_find_node_forever(self):
        while self.isWorking:
            try:
                #弹出一个节点：节点不断从队首取出，向其发送find_node请求，收到的应答中的新节点不断被添加到队尾
                node = self.nodes.popleft()
                self.send_find_node((node.ip, node.port), node.nid)
            except IndexError:
                #一旦节点队列为空，则重新加入 DHT 网络
                self.bootstrap()

    #负责返回信息的处理，msg:报文信息，address:报文地址
    def on_message(self, msg, address):
        try:
            # `回复`
            # 对应于 KPRC 消息字典中的 y 关键字的值是 r，包含了一个附加的关键字 r。
            # 关键字 r 是字典类型，包含了返回的值。发送回复消息是在正确解析了请求消息的基础上完成的。
            if msg[b"y"] == b"r":
                # nodes是字符串类型，包含了被请求节点的路由表中最接近目标节点的K个最接近的节点的联系信息。
                if msg[b"r"].get(b"nodes", None):
                    self.on_find_node_response(msg)
            # `请求`
            # 对应于 KPRC 消息字典中的 y 关键字的值是 q，它包含2个附加的关键字
            # q 和 a：关键字 q 是字符串类型，包含了请求的方法名字。关键字 a 一个字典类型包含了请求所附加的参数。
            # 而实际上我们只需要获取这两者中的 info hash，用于构造磁力链接进而获取torrent文件
            elif msg[b"y"] == b"q":
                # get_peers与torrent文件的info_hash 有关。这时 KPRC 协议中的"q" = "get_peers"。
                # get_peers 请求包含 2 个参数:第一个参数是 id包含了请求节点的node id;第二个参数是info_hash它代表 torrent文件的info_hash
                if msg[b"q"] == b"get_peers":
                    self.on_get_peers_request(msg, address)
                # announce_peer 表明请求的节点正在某个端口下载 torrent文件。
                # announce_peer 包含 4 个参数。第一个参数是 id，包含了请求节点的node id;第二个参数是info_hash包含了torrent文件的 info_hash；
                # 第三个参数是port包含了整型的端口号表明 peer在哪个端口下载;第四个参数数是 token这是在之前的get_peers请求中收到的回复中包含的
                elif msg[b"q"] == b"announce_peer":
                    self.on_announce_peer_request(msg, address)
        except KeyError:
            pass

    #解码nodes节点信息，并存储在双端队列
    def on_find_node_response(self, msg):
        nodes = get_nodes_info(msg[b"r"][b"nodes"])
        for node in nodes:
            nid, ip, port = node
            #进行节点有效性判断
            if len(nid) != PEER_NID_LEN or ip == self.bind_ip:
                continue
            #将节点加入双端队列
            self.nodes.append(HNode(nid, ip, port))

    #处理get_peers请求,获取info hash
    def on_get_peers_request(self, msg, address):
        tid = msg[b"t"]
        try:
            info_hash = msg[b"a"][b"info_hash"]
            self.master.log(info_hash, address)
        except KeyError:
            #没有对应的info hash，发送错误回复
            self.send_error(tid, address)

    #处理announce_peer请求,获取info hash
    def on_announce_peer_request(self, msg, address):
        tid = msg[b"t"]
        try:
            info_hash = msg[b"a"][b"info_hash"]
            self.master.log(info_hash, address)
        except KeyError:
            #没有对应的 info hash,发送错误回复
            self.send_error(tid, address)

    #循环接受udp数据(DHT-Server)
    def receive_response_forever(self):
        #首先加入到 DHT 网络
        self.bootstrap()
        while self.isWorking:
            try:
                #接受返回报文
                data, address = self.udp.recvfrom(UDP_RECV_BUFFSIZE)
                #使用 bdecode 解码返回数据
                msg = bencoder.bdecode(data)
                #处理返回信息
                self.on_message(msg, address)
                time.sleep(SLEEP_TIME1)
            except Exception:
                pass

    #启动多线程
    def start(self):
        self.sfnf_thread.start()
        self.rrf_thread.start()
        self.bst_thread.start()
        Thread.start(self)
        return self

    #停止
    def stop(self):
        self.isWorking = False

#log控制输出
class Master(object):
    def log(self, info_hash, address=None):
        stdger.debug("%s from %s:%s" % (MAGNET_PER.format(codecs.getencoder("hex")(info_hash)[0].decode()), address[0], address[1]))
        fileger.debug('%s from %s:%s' % (MAGNET_PER.format(codecs.getencoder("hex")(info_hash)[0].decode()), address[0], address[1]))

if __name__ == "__main__":
    initialLog()
    threads = []
    for i in range(THREAD_NUMBER):
        port = i + SERVER_PORT #从端口9090开始
        stdger.debug("start thread %d with port %d" % (i, port))
        dht=DHT(SERVER_HOST, port, "thread-%d" % i, Master())
        dht.start()
        threads.append(dht)
        sleep(1)

    sleep(SLEEP_TIME2)

    k = 0
    for i in threads:
        stdger.debug("stop thread %d" % k)
        i.stop()
        i.join()
        k=k+1

