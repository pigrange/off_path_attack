# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:07 PM
# @Tool ：PyCharm
# @Description: 防火墙，用于拦截窗口外的数据
from src.components.end_host.system_service.network.sliding_window import SlidingWindow
from src.components.network.core.router import Router
from src.components.network.datagram.tcp_datagram import TCPDatagram


class FireWall(Router):
    """防火墙类"""

    def on_package(self, prev, package):
        super().on_package(prev, package)
        pass

    def transmit_package(self, package):
        """
        防火墙同样可以发送ICMP报文
        :return:
        """
        super().transmit_package(package)
        pass

    def __init__(self):
        super().__init__()
        self.__window = SlidingWindow()
        pass

    # 如果防火墙决定丢弃(拦截),这里返回True
    def process_package(self, package):
        # 判断ttl是否小于0
        handled = super().process_package(package)
        if handled:
            return handled

        # 对TCP序列号进行过滤
        tcp_pack: TCPDatagram = package.tcp_package

        syn = tcp_pack.flags[2] == 1

        ip = package.origin
        port_1 = tcp_pack.origin_port
        port_2 = tcp_pack.dest_port

        key = ip + '_' + port_1 + '_' + port_2

        pss = self.__window.check_tcp_seq(tcp_pack.seq, key, syn)
        drop = not pss
        if drop:
            print('防火墙: drop seq ',tcp_pack.seq)
        return drop
