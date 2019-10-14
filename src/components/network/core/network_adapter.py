# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 网络适配器,用于握手和通信
from abc import ABCMeta, abstractmethod

from src.components.network import network
from src.components.network.base.network_node import NetworkNode
from src.components.network.datagram.ip_datagram import IPDatagram


class NetworkAdapter(NetworkNode):
    """网络适配器类"""

    def send_package(self, tcp_pack, dest_ip):
        self.handler.post(fun=self.do_send_package, args=(tcp_pack, dest_ip))

    def do_send_package(self, tcp_pack, dest_ip):
        """
        将TCP数据包封装成IP数据包,并发送到网络
        :param tcp_pack: TCP数据包
        :param dest_ip:  目标ip地址
        :return:
        """
        origin_ip = self.ip
        package = IPDatagram(tcp_pack, origin_ip, dest_ip)
        next_node = self.transpond_table[dest_ip]
        self.transmit_package(package, next_node)
        pass

    def handle_package(self, package):
        # 判断消息的ttl
        super().handle_package(package)

        # 把消息丢给操作系统
        self.callBack.on_package(package)

    def __init__(self, callback):
        super().__init__()
        self.callBack = callback
        network.join(self)

    class CallBack:
        __metaclass__ = ABCMeta

        @abstractmethod
        def on_package(self, package):
            pass
