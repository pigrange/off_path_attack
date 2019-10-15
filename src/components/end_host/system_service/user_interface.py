# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 7:10 PM
# @Tool ：PyCharm

from src.components.end_host.system_service.framework.x_os import os_start


# device userInterface是面向设备使用者的一层抽象，当userInterface被实例化的时候，代表了这个系统已经启动
# userInterface 隐藏了高权限shell的细节，通过暴露给用户指定的方法来间接调用高权限shell的操作
# todo 用户的权限检查
# device 通过UserInterface 间接通过高权限的shell来控制os
class UserInterface:
    def __init__(self, name=None):
        shell = os_start()
        # user_interface 默认持有的是高优先级的Shell程序
        self.__high_privilege_shell = shell
        if name is not None:
            self.set_name(name)

    def get_shell(self):
        """
        自己持有的高权限shell不向外部暴露
        通过高优先级的shell返回一个普通优先级的shell
        :return: 普通优先级的shell
        """
        return self.__high_privilege_shell.new_shell()

    def get_ip_addr(self):
        return self.__high_privilege_shell.get_ip_addr()

    def get_port(self):
        return self.__high_privilege_shell.get_port()

    def post_message(self, url, msg):
        self.__high_privilege_shell.post_message(url, msg)

    def get_url(self):
        return self.get_ip_addr() + ':' + self.get_port()

    def set_name(self, name):
        self.__high_privilege_shell.name = name
