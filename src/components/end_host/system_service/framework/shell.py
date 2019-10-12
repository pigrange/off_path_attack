# @coding: utf-8
# @Author: john pig
# @Date: 10/12/2019 6:53 PM
# @Tool: PyCharm
# @Description: 


class Shell:
    def __init__(self, os):
        self.__os = os
        pass

    # 通过shell查询网络数据
    def query_net_state(self):
        """
        查询网络状态
        :return: 字典类型的网络状态
        """
        info = self.__os.network_info
        return info.data()

    # 通过shell注册网络监听者
    def register_network_listener(self, listener):
        """
        注册网络监听接口
        :param listener: 网络监听接口
        :return: null
        """
        self.__os.add_network_listener(listener)

    # 通过shell获取ip地址
    def get_ip_addr(self):
        return self.__os.get_ip_addr()

    # 通过shell发送网络消息
    def post_message(self, url, msg):
        """
        发送消息，通过os的API间接调用网卡发送消息
        注意：整个时候的消息还未被封装为IP报文
        :param url: 目标ip地址和端口号
        :param msg: 消息
        :return: null
        """
        self.__os.send_message(msg, url, self)
        pass

    # os处理消息后将消息丢给指定端口的shell, 在这里回调
    @staticmethod
    def handle_message(msg):
        """
        Shell处理消息，并将消息返回给应用层
        这里直接print消息就行了
        :param msg: 应该提供给应用层的消息
        :return: 返回给应用层的数据
        """
        print(msg)
        # todo

    # 外部的程序或用户等，本质是通过shell和系统进行交互的
    # 所以shell是可以克隆的
    def new_shell(self):
        """
        通过shell可以创建新的shell程序
        :return: 一个新的shell对象,持有私有的os引用
        """
        return Shell(self.__os)


# 高权限的shell
class HighPrivilegeShell(Shell):
    def __init__(self, os):
        super().__init__(os)
        self.__os = os
