# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 网络适配器,用于握手和通信
from abc import ABCMeta, abstractmethod

from src.components.network.base.network_node import NetworkNode
from src.components.network.datagram.ip_datagram import IPDatagram


class NetworkAdapter(NetworkNode):
    """网络适配器类"""

    def send_package(self, ip_pack):
        self.handler.post(fun=self.do_send_package, args=ip_pack)

    def do_send_package(self, ip_pack):
        """
        将TCP数据包封装成IP数据包,并发送到网络,运行在网络适配器自己的线程上
        :param ip_pack: IP数据包
        :return:
        """
        self.transmit_package(ip_pack)
        pass

    def handle_package(self, package):
        # 把消息丢给操作系统
        self.callBack.on_package(package)

    def __init__(self, callback):
        super().__init__()
        self.callBack = callback

    class CallBack:
        __metaclass__ = ABCMeta

        @abstractmethod
        def on_package(self, package):
            pass

    def process_package(self, package):
        super().process_package(package)
        dest_ip = package.dest
        if dest_ip == self.ip:
            self.handle_package(package)
            return True

        return False
