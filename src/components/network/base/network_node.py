# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 8:12 PM
# @Tool ：PyCharm
import time

from src.components.network import network
from src.components.network.datagram.ip_datagram import IPDatagram
from src.util import looper

NETWORK_BANDWIDTH = 1000_000


class NetworkNode:

    def __init__(self):
        self.next = None
        self.prev = None
        self.ip = None
        self.transpond_table = {}
        self.handler = looper.loop()
        network.join(self)
        pass

    # 其他网络节点调用
    def on_package(self, prev, package: IPDatagram):
        self.handler.post(fun=self.do_on_package, args=(prev, package))
        pass

    # 实际的接受包的方法,运行在自己的线程上
    def do_on_package(self, prev, package: IPDatagram):
        """
        网络节点处理网络数据包
        :param prev: 自己的上一个节点
        :param package: IP数据包
        :return: null
        """
        # for test
        # 节点处理时延,5毫秒
        time.sleep(0.005)

        dest_ip = package.dest

        if dest_ip == self.ip:
            self.handle_package(package)

        # 不知道这个包发给谁，就直接丢弃这个包
        if dest_ip not in self.transpond_table.keys():
            return

        # 转发ip数据包
        self.transmit_package(package)
        pass

    # 转发ip数据包
    def transmit_package(self, package):
        """
        获取ip数据包中的ip地址,根据自己的ip映射表获取下一个节点，并将其转发给下一个节点
        :param package:ip数据包
        :return:
        """
        # 将这个包发送给下一个节点
        dest_ip = package.dest
        next_node = self.transpond_table[dest_ip]
        # ttl减1
        package.ttl = package.ttl - 1

        # 模拟传输时延
        if not package.sent:
            byte_count = package.size()
            send_time = byte_count / NETWORK_BANDWIDTH
            time.sleep(send_time)
            print('发送: ', byte_count, 'byte的数据,', '耗时: ', '{:.6f}'.format(send_time), 's')
            package.sent = True

        next_node.on_package(self, package)
        pass

    def handle_package(self, package):
        """
          处理消息，判断ttl，并决定是否将此消息返还给操作系统
          :param package:
          :return:
          """
        ttl = package.ttl
        # 如果消息的ttl小于0了,说明消息已经过期,这个时候回一个ICMP报文
        if ttl < 0:
            # todo 回发一个ICMP报文
            return
