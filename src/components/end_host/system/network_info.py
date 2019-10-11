# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:48 PM
# @Tool ：PyCharm
from abc import ABCMeta, abstractmethod


class NetWorkListener:
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_package_received(self):
        pass


class NetworkInfo:
    def __init__(self):
        pass

    # 将networkInfo的属性转化为字典
    def data(self):
        """
        将网络状态生成字典并返回
        :return:
        """
        res = {}
        return res


