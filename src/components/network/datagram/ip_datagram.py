# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 网络数据包


class IPDatagram:
    def __init__(self, tcp_package, origin, dest, ttl=10):
        self.origin = origin
        self.tcp_package = tcp_package
        self.dest = dest
        self.ttl = ttl
        pass
