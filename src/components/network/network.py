# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:40 PM
# @Tool: PyCharm
# @Description: 整个网络的抽象模型
import random


class Network:
    """路由器链,由路由器节点构成的链表"""

    def __init__(self):
        self.network_node_chain = None
        pass

    def join(self, new_node):
        # ip直接设置成0到4294967295的随机数
        distributed_ip = str(random.randint(0, 4294967295))
        new_node.ip = distributed_ip

        # 如果网络中还没有任何节点的话,就将当前node设置为节点
        if self.network_node_chain is None:
            self.network_node_chain = new_node

        # 如果由节点的话,就将当前的节点加入到网络链表的尾部
        else:

            new_ip = distributed_ip
            head = self.network_node_chain
            inner_net_ip = []

            prev = None
            # 为每一个现有的网络节点广播新的节点的加入
            while head is not None:
                head.transpond_table[new_ip] = head.next
                inner_net_ip.append(head.ip)
                prev = head
                head = head.next
            # 将新的节点插入到当前网络链表的末尾
            prev.next = new_node
            prev.transpond_table[new_ip] = new_node

            # 为当前的节点创建网络的转发表
            for ip in inner_net_ip:
                new_node.transpond_table[ip] = prev


# 初始化整个网络
RUNNING_NETWORK = Network()


def join(network_node):
    """
    网络节点加入到网络中,并返回该节点的ip地址
    :param network_node:
    :return: ip地址
    """
    RUNNING_NETWORK.join(network_node)


# 输出整个网络结构
def net_status():
    net = RUNNING_NETWORK
    head = net.network_node_chain
    while head is not None:
        print(head)
        head = head.next
    pass
