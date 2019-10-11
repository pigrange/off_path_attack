# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 路由器,用于转发网络数据包
from src.components.network.base.network_node import NetworkNode


class Router(NetworkNode):
    """路由器类"""

    def transmit_package(self):
        pass

    def on_package(self, prev):
        pass

    def __init__(self):
        super().__init__()
        pass
