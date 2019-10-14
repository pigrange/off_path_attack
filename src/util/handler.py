# @coding: utf-8
# @Author: john pig
# @Date: 10/14/2019 4:22 PM
# @Tool: PyCharm
# @Description:
from queue import Queue
from threading import Condition


class Handler:
    def __init__(self, condition, queue):
        self.__target = queue
        self.__condition = condition
        pass

    def post(self, fun, args=None):
        if self.__target is None:
            return
        q: Queue = self.__target
        condition: Condition = self.__condition

        condition.acquire()
        q.put((fun, args))
        condition.notify()
        condition.release()
        pass
