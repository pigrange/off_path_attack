# @coding: utf-8
# @Author: john pig
# @Date: 10/16/2019 8:29 AM
# @Tool: PyCharm
# @Description:


class SlidingWindow:
    """滑动窗口类"""

    # 默认滑动窗口的大小是64kb
    def __init__(self, window_size=1024):
        self.__url_sel_map = {}
        self.window_size = window_size
        pass

    # 防火墙会检查syn=1的包，并在字节的SlidingWindow中，为其创建
    # 为某一个连接创建一个window
    # @called : 当防火墙转发一个没有这个key的tcp包，并且此包的syn=1的时候
    def gen_window(self, key, seq):
        self.__url_sel_map[key] = seq
        pass

    # 检验tcp序列号的有效性
    def check_tcp_seq(self, recv_seq, key, new_connection):
        # print('FireWall : ', key)
        # print('seq is : ', recv_seq)

        # 如果是新的连接，并且防火墙并没有缓存的话,就为此连接创建窗口
        if new_connection & (key not in self.__url_sel_map.keys()):
            self.gen_window(key, recv_seq)
            return True

        # 如果这个消息在window内,就通过，并且更新当前的窗口
        expect_seq = self.__url_sel_map[key]
        if (recv_seq >= expect_seq) & (recv_seq < (expect_seq + self.window_size)):
            self.update_seq(recv_seq, key)
            return True
        # 返回false, 应该丢弃这个包
        return False

    def update_seq(self, new_seq, key):
        self.__url_sel_map[key] = new_seq
        pass
