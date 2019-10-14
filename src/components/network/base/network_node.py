# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 8:12 PM
# @Tool ：PyCharm

from abc import abstractmethod

from src.components.network.datagram.ip_datagram import IPDatagram


class NetworkNode:

    def __init__(self):
        self.next = None
        self.prev = None
        self.ip = None
        self.transpond_table = {}
        pass

    def on_package(self, prev, package: IPDatagram):
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

    @abstractmethod
    def handle_package(self, package):
        pass
