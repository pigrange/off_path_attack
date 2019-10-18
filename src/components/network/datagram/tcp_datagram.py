# @coding: utf-8
# @Author: john pig
# @Date: 10/12/2019 4:58 PM
# @Tool: PyCharm
# @Description: 

NORMAL = -1
HEADER_ERROR = 0
ADDRESS_ERROR = 1
UNKNOWN_PROTOCOL = 2
REASSEMBLY_SUCCESSFUL = 3


class TCPDatagram:
    def __init__(self, origin_port, dest_port, seq, ack=0, data=''):
        self.origin_port = origin_port
        self.dest_port = dest_port
        self.seq = seq
        self.ack = ack
        self.data = data
        self.flags = (0, 0, 0)
        self.tpe = NORMAL
        pass

    def set_flags(self, ack=0, rst=0, syn=0):
        flags = (ack, rst, syn)
        self.flags = flags

    # 可以通过此方法将其设置成特殊的IP数据包
    def set_package_type(self, tpe):
        if not isinstance(tpe, int):
            return
        if (tpe > 3) | (tpe < -1):
            return

        self.tpe = tpe
        pass
