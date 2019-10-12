# @coding: utf-8
# @Author: john pig
# @Date: 10/12/2019 1:00 PM
# @Tool: PyCharm
# @Description: 

from abc import ABCMeta, abstractmethod


class NetWorkListener:
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_package_received(self):
        pass

    @abstractmethod
    def on_establish_connection(self, origin, target):
        pass
