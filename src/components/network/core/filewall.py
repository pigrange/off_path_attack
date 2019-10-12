# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:07 PM
# @Tool ：PyCharm
# @Description: 防火墙，用于拦截窗口外的数据
from src.components.network.base.network_node import NetworkNode


class FileWall(NetworkNode):
    """防火墙类"""

    def on_package(self, prev, package):
        pass

    def transmit_package(self,package):
        """
        防火墙同样可以发送ICMP报文
        :return:
        """
        pass

    def __init__(self):
        pass


class SlidingWindow:
    """滑动窗口类"""

    def __init__(self):
        pass
