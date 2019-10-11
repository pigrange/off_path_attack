# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 7:10 PM
# @Tool ：PyCharm
from src.components.end_host.system.os import os_start


class UserInterface:
    def __init__(self):
        (h_shell, l_shell) = os_start()
        self.__high_privilege_shell = h_shell
        self.__low_privilege_shell = l_shell

    def get_shell(self):
        return self.__low_privilege_shell
