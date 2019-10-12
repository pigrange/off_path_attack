# @coding: utf-8
# @Author: john pig
# @Date: 10/12/2019 4:58 PM
# @Tool: PyCharm
# @Description: 


class TCPDatagram:
    def __init__(self, origin_port, dest_port, seq, ack=0, data=''):
        self.origin_port = origin_port
        self.dest_port = dest_port
        self.seq = seq
        self.ack = ack
        self.data = data
        self.flags = (0, 0, 0)
        pass

    def set_flags(self, ack=0, rst=0, syn=0):
        flags = (ack, rst, syn)
        self.flags = flags
