# @coding: utf-8
# @Author: john pig
# @Date: 10/12/2019 6:54 PM
# @Tool: PyCharm
# @Description: 
# TCP 有限状态机


# 基于传输层的，os维持一个new_work_connect table
# 记录那些URL被连接
# 当os被调用send_message的时候,会去检测目标url是否建立了连接
# 如果没有建立连接就尝试握手
from transitions import Machine

from src.test.test_fsm import Matter


class TCPFSM:
    def __init__(self):
        model = Matter()
        states = ['closed', 'syn_send', 'establish', 'syn_rcved']
        transitions = [
            {'trigger': 'send', 'source': 'closed', 'dest': 'syn_send'},
            {'trigger': 'establish', 'source': 'syn_send', 'dest': 'establish'},
            {'trigger': 'receive', 'source': 'closed', 'dest': 'syn_rcved'},
            {'trigger': 'establish', 'source': 'syn_rcved', 'dest': 'establish'},
            {'trigger': 'reset', 'source': 'syn_rcved', 'dest': 'closed'}
        ]
        Machine(model=model, states=states, transitions=transitions, initial='closed')
        self.__model = model
        pass

    def send(self):
        self.__model.send()

    def establish(self):
        self.__model.establish()

    def receive(self):
        self.__model.receive()

    def reset(self):
        self.__model.reset()

    def state(self):
        return self.__model.state
