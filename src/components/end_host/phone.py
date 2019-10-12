# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:06 PM
# @Tool ：PyCharm


from src.components.end_host.system_service.user_interface import UserInterface
from src.components.attacker.malware import Parasitic


class Phone(Parasitic):
    def on_infect(self):
        return self.__user_interface.get_shell()

    def __init__(self):
        self.__user_interface = UserInterface()
        pass
