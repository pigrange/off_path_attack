# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:48 PM
# @Tool ：PyCharm


class NetworkInfo:
    def __init__(self):
        info_table = self.__init_info_table()
        self.info_table = info_table
        pass

    def data(self):
        """
        :return:网络状态表
        """
        return self.info_table

    def update(self, key):
        """
        更新接受到的包的值
        :param key:
        :return:
        """
        self.info_table[key] += 1
        pass

    @staticmethod
    def __init_info_table():
        res = {"PacketsReceived": 0,
               "HeaderErrors": 0,
               "ReassemblyRequired": 0,
               "ReassemblySuccessful": 0,
               "PacketNoRoute": 0}
        return res
