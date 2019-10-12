# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 8:12 PM
# @Tool ：PyCharm

from abc import ABCMeta, abstractmethod


class NetworkNode:
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_package(self, prev, package):
        pass

    def transmit_package(self, package):
        pass
