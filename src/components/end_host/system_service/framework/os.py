# @coding: utf-8
# @Author：john pig
# @Date ：10/11/2019 5:41 PM
# @Tool ：PyCharm
import random

from src.components.end_host.system_service.framework.shell import Shell, HighPrivilegeShell
from src.components.end_host.system_service.network.network_info import NetworkInfo
from src.components.end_host.system_service.network.network_listener import NetWorkListener
from src.components.end_host.system_service.network.tcp_fsm import TCPFSM
from src.components.network.core.network_adapter import NetworkAdapter
from src.components.network.datagram.tcp_datagram import TCPDatagram


class __OS(NetworkAdapter.CallBack):
    def __init__(self):
        self.network_info = NetworkInfo()
        self.listener_info = self.__ListenerInfo()

        # 网络适配器只和发送消息和接受消息有关
        # TCP的握手逻辑由操作系统负责
        self.network_adapter = NetworkAdapter(callback=self)
        self.app_port_map = {}
        self.connection_map = {}
        self.cached_message = {}
        pass

    # 网卡回调此方法
    def on_package(self, package):
        """
        网卡接受到消息之后，回调OS的on_package方法
        :param package 收到的消息
        :return: null
        """
        # 首先更新网络消息
        # 如果是无效的消息就直接return了
        if not self.update_network_info(package):
            return

        if self.listener_info is not None:
            self.listener_info.on_package()

        # todo 接受的SYN=1的消息打开连接的判断逻辑
        # todo 检验消息的seq是否有效,
        # todo 在哪里存放当前的seq? 有限状态机?
        # 注意：这里假设所有的网络顺序到达，故seq始终未当前的seq+1
        # 非+1的消息全部丢弃

        # todo 调用handle_message
        pass

    # os将消息丢到指定端口号的应用
    def handle_message(self, msg, port):
        """
        向上层返回消息
        :param msg: ip层拆包得到的消息
        :param port: 指定的端口号
        :return: null
        """
        p_map = self.app_port_map
        app: Shell = p_map[port]
        app.handle_message(msg)
        pass

    # 解析url
    def parse_url(self, url):
        """
        解析url
        :param url:传入的url
        :return: ip地址,目标端口
        """
        # todo 拆分url为和端口
        return None, None
        pass

    # os调用网卡发送消息
    def send_message(self, msg, url, app):
        """
        将敏文消息封装为ip报文,并为指定的app分配端口号
        :param url: 目标ip地址和端口号
        :param msg: 上层传递过来的消息
        :param app: 上层的应用
        :return: null
        """
        if not self.check_connection(url):
            # 缓存当前的消息
            self.cached_message[url] = (msg, app)
            # 建立连接
            self.establish_connection(url)
            return

        # 解析url
        (dest_ip, dest_port) = self.parse_url(url)
        # 打包生成TCP包
        tcp_pack = self.gen_tcp_pack(dest_port, app, msg)
        # 将TCP报文丢给网络适配器发送
        self.network_adapter.send_package(tcp_pack, dest_ip)
        pass

    # 生成tcp报文
    def gen_tcp_pack(self, dest_port, app, msg):
        """
        把消息打包成tcp报文
        :param dest_port: 目标端口
        :param app: 发送此报文的应用程序
        :param msg: tcp的消息内容
        :return: tcp报文对象
        """
        origin_port = self.map_app_to_port(app)

        seq = random.randint((0, 4294967295))

        return TCPDatagram(origin_port, dest_port, data=msg, seq=seq)
        pass

    # 添加网络包的监听器
    def add_network_listener(self, listener):
        self.listener_info.listeners.append(listener)
        pass

    # 将app映射到端口,即为上层应用分配端口
    def map_app_to_port(self, app: Shell):
        """
        将shell程序映射程端口号
        :param app:
        :return: 端口号
        """
        port = hash(app) % 65536
        # 缓存端口
        self.app_port_map[port] = app
        return port
        pass

    # 检查是否检验了连接
    def check_connection(self, url):
        if url in self.connection_map.keys():
            return True
        else:
            return False

    # 建立连接
    def establish_connection(self, url):
        # 初始化此TCP状态机
        fsm = TCPFSM()
        self.connection_map[url] = fsm
        # todo 进行tcp的三次握手
        pass

    # 更新网络信息
    def update_network_info(self, package):
        """
        检测消息的类型，选择性更新network_info
        并根据消息的类型选择性丢弃消息
        :param package:
        :return:
        """
        # todo 更新 network_info
        return

    # 获取本机的ip地址
    def get_ip_addr(self):
        return self.network_adapter.ip

    # 操作系统注册的网络监听信息
    class __ListenerInfo:
        listeners = []

        def __init__(self):
            pass

        def on_package(self):
            for listener in self.listeners:
                if listener is NetWorkListener:
                    listener.on_package_received()

        def on_establish_connection(self, origin, target):
            for listener in self.listeners:
                if listener is NetWorkListener:
                    listener.on_establish_connection(origin, target)


def os_start():
    running_os = __OS()
    shell = HighPrivilegeShell(running_os)
    return shell
