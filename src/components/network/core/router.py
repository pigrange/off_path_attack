# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 路由器,用于转发网络数据包
from src.components.network.base.network_node import NetworkNode

ROUTER_COUNT = 0


# 在网络中创建路由器
def add_router_to_net(router_count):
    for i in range(0, router_count):
        Router()


class Router(NetworkNode):
    """路由器类"""

    def transmit_package(self, package):
        print(self.name, ':', 'on_transmit_package')
        super().transmit_package(package)

    def on_package(self, prev, package):
        print(self.name, ':', 'on_package')
        super().on_package(prev, package)
        pass

    def __init__(self):
        global ROUTER_COUNT
        super().__init__()
        self.name = 'Router' + str(ROUTER_COUNT)
        ROUTER_COUNT += 1
        pass
