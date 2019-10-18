# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 路由器,用于转发网络数据包
import time

from src.components.network.base.network_node import NetworkNode

ROUTER_COUNT = 0


class Router(NetworkNode):
    """路由器类"""

    def transmit_package(self, package):
        # print(self.name, ':', 'on_transmit_package')
        super().transmit_package(package)

    def on_package(self, prev, package):
        # print(self.name, ':', 'on_package')
        super().on_package(prev, package)
        pass

    def __init__(self):
        global ROUTER_COUNT
        super().__init__()
        self.name = 'Router' + str(ROUTER_COUNT)
        ROUTER_COUNT += 1
        pass

    # 路由器IP数据包进行检查
    def process_package(self, package):
        """
        路由器检查ip数据包的ttl,是否能被有效转发
        :param package:
        :return: 节点是否处理了这个消息
        """
        super().process_package(package)
        # for test
        # 节点处理时延,5毫秒
        # time.sleep(0.005)
        time.sleep(0.1)

        dest_ip = package.dest

        ttl = package.ttl
        # 如果消息的ttl小于0了,说明消息已经过期,这个时候回一个ICMP报文
        if ttl < 0:
            print('router : ', 'ttl小于0 , 停止转发')
            # todo 发一个ICMP报文
            return True

        # 不知道这个包发给谁，就直接丢弃这个包
        if dest_ip not in self.transpond_table.keys():
            return True
        return False


# 在网络中创建路由器
def add_router_to_net(router_count, has_firewall=False):
    for i in range(0, router_count):
        Router()

        # excuse me ? 为什么要在这里import才可以
        from src.components.network.core.firewall import FireWall
        if has_firewall & (i == int(router_count / 2)):
            FireWall()
