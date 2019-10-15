# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:06 PM
# @Tool ：PyCharm
from src.components.end_host.system_service.user_interface import UserInterface


class Server:
    def __init__(self, name):
        self.__userInterface = UserInterface(name)
        pass

    def get_url(self):
        return self.__userInterface.get_url()

    def post_message(self, url, msg):
        self.__userInterface.post_message(url, msg)
