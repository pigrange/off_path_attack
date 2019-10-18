# @coding: utf-8
# @Author: john pig
# @Date: 10/11/2019 8:25 PM
# @Tool: PyCharm
# @Description: 网络数据包

NORMAL = -1
HEADER_ERROR = 0
ADDRESS_ERROR = 1
UNKNOWN_PROTOCOL = 2
REASSEMBLY_SUCCESSFUL = 3


class IPDatagram:
    def __init__(self, tcp_package, origin, dest, ttl=255):
        self.origin = origin
        self.tcp_package = tcp_package
        self.dest = dest
        self.ttl = ttl
        self.sent = False
        pass

    def size(self):
        return 40 + len(self.tcp_package.data)

