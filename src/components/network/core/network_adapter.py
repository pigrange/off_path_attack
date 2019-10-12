# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 网络适配器,用于握手和通信
from src.components.network.base.network_node import NetworkNode
from abc import ABCMeta, abstractmethod

from src.components.network.datagram.ip_datagram import IPDatagram


class NetworkAdapter(NetworkNode):
    """网络适配器类"""

    def send_package(self, tcp_pack, dest_ip):
        """
        将TCP数据包封装成IP数据包,并发送到网络
        :param tcp_pack: TCP数据包
        :param dest_ip:  目标ip地址
        :return:
        """
        origin_ip = self.ip
        package = IPDatagram(tcp_pack, origin_ip, dest_ip)
        self.transmit_package(package)
        pass

    def transmit_package(self, package):
        pass

    def on_package(self, prev, package):
        pass

    def process_package(self, package):
        """
        预处理网络数据包，判断是否是自己的，判断TTL是否有效...
        通知注册的网络监听，收到了消息
        :param package:
        :return:
        """
        # todo 处理消息的逻辑
        self.CallBack.on_package(package)
        # todo 丢弃消息的逻辑
        pass

    def is_destination(self, addr):
        pass

    def __init__(self, callback):
        super().__init__()
        self.CallBack = callback
        self.ip = None

    class CallBack:
        __metaclass__ = ABCMeta

        @abstractmethod
        def on_package(self, package):
            pass
