# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 网络适配器,用于握手和通信
from src.components.network.base.network_node import NetworkNode


class NetworkAdapter(NetworkNode):
    """网络适配器类"""

    def transmit_package(self):
        pass

    def on_package(self, prev):
        pass

    def __init__(self):
        super().__init__()
