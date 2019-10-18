# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:48 PM
# @Tool ：PyCharm


class NetworkInfo:
    def __init__(self):
        info_table = self.__init_info_table()
        self.info_table = info_table
        self.__type_key_map = {
            -1: 'PacketsReceived',
            0: 'HeaderErrors',
            1: 'AddressErrors',
            2: 'UnknownProtocol',
            3: 'ReassemblySuccessful'
        }
        pass

    def data(self):
        """
        :return:网络状态表
        """
        return self.info_table

    def update(self, tp):
        """
        更新接受到的包数量
        :param tp: 包的类型
        :return:
        """
        key = self.__type_to_key(tp)
        self.info_table[key] += 1
        pass

    def __type_to_key(self, t):
        return self.__type_key_map[t]
        pass

    @staticmethod
    def __init_info_table():
        res = {"PacketsReceived": 0,
               "HeaderErrors": 0,
               "AddressErrors": 0,
               "UnknownProtocol": 0,
               "ReassemblySuccessful": 0}
        return res
