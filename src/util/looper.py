# @coding: utf-8
# @Author: john pig
# @Date: 10/14/2019 4:15 PM
# @Tool: PyCharm
# @Description: 

from threading import Thread, Condition, Lock
from queue import Queue

from src.util.handler import Handler


def loop():
    """
    创建一个启动线程
    并返回一个handler
    :return: handler,用于向线程中传递消息
    """
    q = Queue()
    condition = Condition(lock=Lock())
    handler = Handler(condition=condition, queue=q)

    Thread(target=on_start, args=(q, condition)).start()
    return handler


# 运行在worker线程里面的方法
def on_start(queue: Queue, condition: Condition):
    while True:
        condition.acquire()
        if queue.empty():
            condition.wait()

        msg = queue.get()
        condition.release()
        (func, args) = (msg[0], msg[1])
        if args is not None:
            if type(args) is not tuple:
                func(args)
            else:
                func(*args)
        else:
            func()
    pass
