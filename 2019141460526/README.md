# 计算机网络课程设计-DHT嗅探器

## 一.作业概述

### 1.1 背景简述

在P2P网络中，要通过种子文件下载一个资源，需要知道整个P2P网络中有哪些计算机正在下载/上传该资源。这里将这些提供某个资源下载的计算机定义为peer。传统的P2P网络中，存在一些tracker服务器，这些服务器的作用主要用于跟踪某个资源有哪些关联的peer。下载这个资源当然得首先取得这些peer。

DHT的出现用于解决当tracker服务器不可用时，P2P客户端依然可以取得某个资源的peer。DHT解决这个问题，是因为它将原来tracker上的资源peer信息分散到了整个网络中。这里将实现了DHT协议的计算机定义为节点(node)。通常一个P2P客户端程序既是peer也是节点。DHT网络有多种实现算法，例如Kademlia。

当某个P2P客户端通过种子文件下载资源时，如果没有tracker服务器，它就会向DHT网络查询这个资源对应的peer列表。资源的标识在DHT网络中称为infohash，它是每个种子文件的一个唯一标识码，是种子中所有info信息B编码后的SHA-1哈希值：20个字节，即40个16进制码，根据这串码就能找到对应的种子文件。在除了单纯的Torrent下载方式，还有磁力链接的形式，具体由部分参数与infohash组成，以magnet:?xt=urn:btih:{infohash}的形式存在。

### 1.2 作业简述

作业是基于分布式哈希表即DHT的infohash嗅探器，主要核心遵循面向P2P的Bittorrent协议下的Mainline DHT (Kademlia即Kad DHT)，通过DHT网络获取infohash，实现了DHT网络的部分功能。具体见下文。



## 二.功能说明

### 2.1 实现

作业遵循Bittorrent的BEP-5的DHT Protocol，具体实现如下：

- node结点与简化的DHT的构造
- 简化异或计算寻找邻近结点
- 利用大型tracker加入DHT网络
- 非完整的KRPC协议与3种消息(请求/回复/错误)
- KRPC协议: find_node请求
- KRPC协议: get_peers请求
- KRPC协议: announce_peer请求

实现思路：思路是伪装成一个DHT节点。初始化时，给自己随机生成一个20位的ID，通过大的tracker服务器（如router.bittorrent.com）获取其他节点的地址信息(find_node操作)，进入DHT网络，利用KRPC协议传输B编码的字典信息，即DHT查询信息与DHT网络中的其他节点互相通信，从而获取infohash。

- Kademlia基于两个节点之间的距离计算，该距离是两个网络节点node id的异或，计算的结果最终作为整型数值返回。资源的infohash和node id有同样的格式和长度，因此可以使用同样的方法计算资源infohash和节点node id之间的距离。节点ID一般是一个大的随机数，选择该数的时候所追求的一个目标就是它的唯一性即希望在整个网络中该节点node id是唯一的。


- 在初始化时已经从大的Tracker服务器获取了节点信息(`bootstrap`)，接下来向这些节点发送find_node请求，参数中:
  - 将自己的node id构造成被请求节点的按异或相近的node id(`get_neighbor()`)。
  - 要查找的node id随机生成(`get_rand_id()`)或自行指定，大部分随机生成的node id是不可能直接查找到的，被请求节点会返回另一批节点信息，在接受到返回的新节点信息后向新节点继续发送请求，不断迭代进行，目的是不断让其他节点认识(`send_find_node_forever()`)。这里维护了一个有限长的双端队列(`self.nodes`)存储节点，节点不断从队首取出向其发送find_node请求，收到的应答中的新节点不断被添加到队尾，如果队列为空则重新初始化一下(`self.bootstrap()`)。
- 一旦很多节点认识了本节点就会有不断的查询请求从其他节点发送过来，此时get_peers和announce_peer请求包含了所需的infohash信息。
  - get_peers是一个节点向另一个节点发出的查询与info_hash相关的下载者信息，以一个token（自己以一定方式生成，不固定，用来校验的）与一个空的nodes参数回应(`on_get_peers_request`)。
  - 这个向本节点查询的节点如果最终通过其他节点找到了资源（其他下载者即peer），而控制该节点的下载者开始下载资源了，该节点很可能向本节点发送announce_peer消息，该消息包含它的下载者信息，以本本节点的node id返回(`on_announce_peer_request`)。

### 2.2 具体功能

具体功能主要是通过脚本加入DHT网络嗅探infohash，其中具体的功能及叙述如下所示：

- infohash嗅探：可以大量获取DHT网络中各结点的infohash
- 多线程：高效，可以充分利用资源，提高运行效率与时间
- 日志输出及保存：替代数据库，更轻量，便于记录读取，在终端输出上也更规整



## 三.使用与操作

### 3.1准备

安装依赖

```python
pip install -r requirements.txt
```

在myDHT.py中设置参数

```python
#线程数
THREAD_NUMBER = 3
#线程持续时间
SLEEP_TIME2 = 60*10 
```

其他参数可视需求设置

### 3.2运行

在相应目录下运行终端，最好不要在代理下运行，不要在内网下运行

```
python myDHT.py
```

预计等待30秒会得到结果，视网络情况而定

### 3.3结果

当时间截至，断开与DHT网络的链接，在同一目录下会生成HASH.log文件, 记录了嗅探到的infohash，以磁力链接的形式存在。

具体形式为:

```
#时间 - file_log - DEBUG - magnet:?xt=urn:btih:infohash from host:port
2021-06-23 22:44:27,794 - file_log - DEBUG - magnet:?xt=urn:btih:673b35e24aa1bc3877628b8af7878b33fe07602e from 188.190.177.83:6881
```



## 参考

1. [BitTorrent DHT 协议中文翻译](https://www.jianshu.com/p/ffeed4801b0e)
2. [P2P中DHT网络介绍](https://damogame.cn/wordpress/?p=5212)
3. [P2P 网络核心技术：Kademlia 协议](https://zhuanlan.zhihu.com/p/40286711)
4. [Kademlia、DHT、KRPC、BitTorrent 协议、DHT Sniffer](https://blog.csdn.net/weixin_34297704/article/details/85881799)
5. [【一步一步教你写BT种子嗅探器】](https://github.com/shiyanhui/dht/wiki/%E3%80%90%E4%B8%80%E6%AD%A5%E4%B8%80%E6%AD%A5%E6%95%99%E4%BD%A0%E5%86%99BT%E7%A7%8D%E5%AD%90%E5%97%85%E6%8E%A2%E5%99%A8%E3%80%91DHT%E7%AF%87)
6. [DHT 公网嗅探器](https://github.com/lyyyuna/DHT_sniffer)
7. [py-libp2p](https://github.com/libp2p/py-libp2p)
8. [Maga](https://github.com/whtsky/maga)
9. [DHT 网络磁力种子采集器](https://github.com/chenjiandongx/magnet-dht)
10. [Python Distributed Hash Table](https://github.com/bmuller/kademlia)
11. [simDHT](https://github.com/wuzhenda/simDHT)

