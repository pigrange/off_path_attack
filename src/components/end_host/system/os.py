# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:41 PM
# @Tool ：PyCharm

from src.components.end_host.system.network_info import NetworkInfo, NetWorkListener


class __OS:
    def __init__(self):
        self.network_info = NetworkInfo()
        self.listener_info = self.__ListenerInfo()
        pass

    def add_network_listener(self, listener):
        self.listener_info.listeners.append(listener)

    # 操作系统注册的网络监听信息
    class __ListenerInfo:
        listeners = []

        def __init__(self):
            pass

        def notify(self):
            for listener in self.listeners:
                if listener is NetWorkListener:
                    listener.on_package_received()


class Shell:
    def __init__(self, os):
        self.__os = os
        pass

    # shell查询网络数据
    def query_net_state(self):
        """
        查询网络状态
        :return: 字典类型的网络状态
        """
        info = self.__os.network_info
        return info.data()

    def register_network_listener(self, listener):
        """
        注册网络监听接口
        :param listener: 网络监听接口
        :return: null
        """
        self.__os.add_network_listener(listener)


class HighPrivilegeShell(Shell):
    def __init__(self, os):
        super().__init__(os)
        self.__os = os


def os_start():
    running_os = __OS()
    l_shell = Shell(running_os)
    h_shell = HighPrivilegeShell(running_os)
    return h_shell, l_shell
