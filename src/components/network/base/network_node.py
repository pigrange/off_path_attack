# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 8:12 PM
# @Tool ：PyCharm

from abc import abstractmethod

from src.components.network.datagram.ip_datagram import IPDatagram
from src.util import looper


class NetworkNode:

    def __init__(self):
        self.next = None
        self.prev = None
        self.ip = None
        self.transpond_table = {}
        self.handler = looper.loop()
        pass

    # 其他网络节点调用
    def on_package(self, prev, package: IPDatagram):
        self.handler.post(fun=self.do_on_package, args=(prev, package))
        pass

    # 实际的接受包的方法,运行在自己的线程上
    def do_on_package(self, prev, package: IPDatagram):
        """
        网络节点处理网络数据包
        :param prev: 自己的上一个节点
        :param package: IP数据包
        :return: null
        """
        dest_ip = package.dest

        if dest_ip == self.ip:
            self.handle_package(package)

        # 不知道这个包发给谁，就直接丢弃这个包
        if dest_ip not in self.transpond_table.keys():
            return
        # 将这个包发送给下一个节点
        next_node = self.transpond_table[dest_ip]
        # ttl减1
        package.ttl = package.ttl - 1
        self.transmit_package(IPDatagram, next_node)
        pass

    def transmit_package(self, package, node):
        node.on_package(self, package)
        pass

    def handle_package(self, package):
        """
          处理消息，判断ttl，并决定是否将此消息返还给操作系统
          :param package:
          :return:
          """
        ttl = package.ttl
        # 如果消息的ttl小于0了,说明消息已经过期,这个时候回一个ICMP报文
        if ttl < 0:
            # todo 回发一个ICMP报文
            return
