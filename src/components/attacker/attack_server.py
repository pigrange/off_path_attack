# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:05 PM
# @Tool ：PyCharm
from threading import currentThread

from src.components.end_host.system_service.framework import x_os
from src.components.network.datagram.ip_datagram import IPDatagram
from src.components.network.datagram.tcp_datagram import TCPDatagram


class AttackerServer:
    def __init__(self, malware):
        self.malware = malware
        self.shell = x_os.os_start()
        pass

    def notify_second_handshake_sent(self, origin, dest):
        origin_url = origin[0] + ':' + origin[1]
        dest_url = dest[0] + ':' + dest[1]
        # print('AttackerServer', 'received malware message')
        # print('From: ', origin_url)
        # print('To', dest_url)

        # 伪造一个客户端的rst消息
        rst = TCPDatagram(origin[1], dest[1], 0)
        rst.set_flags(rst=1)
        package = IPDatagram(rst, origin[0], dest[0])
        print(currentThread(), 'AttackServer: 向原始服务器发送rst消息')
        self.shell.send_ip_package(package)
        # todo 进行tcp序列号预测
        pass
