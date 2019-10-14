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
from src.components.network.datagram.ip_datagram import IPDatagram
from src.components.network.datagram.tcp_datagram import TCPDatagram



class __OS(NetworkAdapter.CallBack):
    def __init__(self):
        self.network_info = NetworkInfo()
        self.listener_info = self.__ListenerInfo()

        # 网络适配器只和发送消息和接受消息有关
        # TCP的握手逻辑由操作系统负责
        self.network_adapter = NetworkAdapter(callback=self)
        # 存放端口号和对应应用程序之间的映射关系
        self.__port_app__map = {}
        # 存放url和连接状态机的映射关系
        self.__url_tcpfsm_map = {}
        # 存放url和消息的映射关系，用于缓存Message
        self.__url_message_map = {}
        # 存放连接状态和此seq之间的映射关系
        self.__url_seq_map = {}
        pass

    # 网卡回调此方法
    def on_package(self, package: IPDatagram):
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

        # 获取发送方的ip地址
        dest_ip = package.origin
        # 获取发送放的tcp报文
        tcp_pack: TCPDatagram = package.tcp_package

        # 获取端口号
        dest_port = tcp_pack.origin_port
        origin_port = tcp_pack.dest_port

        # 获取监听此端口的app
        if origin_port not in self.__port_app__map.keys():
            # 没有端口监听，直接返回
            return
        app = self.__port_app__map[origin_port]

        # 获取实际的url
        url = dest_ip + ':' + dest_port

        # 如果没有建立连接，那么就建立连接
        if not self.check_connection(url):
            # 会生成fsm
            self.establish_connection(url)

        fsm: TCPFSM = self.get_tcp_fsm(url)
        state = fsm.state()

        # 服务端调用,接受到了客户端消息的状态
        if state is 'closed':
            # flag格式(ack,rst,syn)
            flags = tcp_pack.flags
            # 这种包直接丢弃
            if flags[2] is not 1:
                return
            print('服务器收到第一次握手,准备第二次握手')
            second_shake = self.gen_tcp_pack(url, app)

            # 缓存客户端口的seq,由于gen_tcp_pack的时候才会建立seq
            # 所以在它之后创建
            # +1是因为客户端发送了第一个握手包
            remote_seq = tcp_pack.seq + 1
            self.update_remote_seq(remote_seq, url)

            # 发送syn=1,ack 进行第二次握手
            second_shake.set_flags(ack=tcp_pack.seq + 1, syn=1)
            # 更新为syn_rcved状态
            fsm.receive()
            print('服务器发送第二次握手消息')
            print('服务器端seq', self.__url_seq_map[url][0])
            print('服务端维护的客户端seq', self.__url_seq_map[url][1])
            self.network_adapter.send_package(second_shake, dest_ip)
            return

        # 客户端调用，发送了第一次握手后，收到回复的状态z
        # 这个方法内部进行第三次TCP握手
        elif state is 'syn_send':
            # 检查服务器回复的是否是syn+ack,如果是的话，就进行第三次握手
            flags = tcp_pack.flags
            # 非syn = 1直接return
            if flags[2] is 0:
                return
            ack = flags[0]
            # ack应该为自己的seq+1
            expect_ack = self.__url_seq_map[url][0]
            if not ack == expect_ack:
                return

            print('客户端收到了服务端的第二次握手')
            # 缓存服务端的seq, +1是因为服务端的第二次握手占用了一个长度
            remote_seq = tcp_pack.seq + 1
            self.update_remote_seq(remote_seq, url)

            # 进行第三次握手
            third_handshake = self.gen_tcp_pack(url, app)
            third_handshake.set_flags(ack=tcp_pack.seq + 1)
            # 更新为establish状态
            fsm.establish()
            print('客户端发送第三次握手，并建立连接')
            self.network_adapter.send_package(third_handshake, dest_ip)

            # 通知监听器,TCP握手已经完成
            origin = (self.get_ip_addr(), origin_port)
            dest = (dest_ip, dest_port)
            self.listener_info.on_establish_connection(origin, dest)

            # 将缓存的消息发送给服务器
            cached_msg = self.__url_message_map[url]
            self.__url_message_map.pop(url)
            print('客户端发送缓存的消息')
            self.send_message(cached_msg, url, app)

            return

        # 服务端调用，进行了第二次握手，等待客户端的第三个握手的状态
        elif state is 'syn_rcved':
            # flag格式(ack,rst,syn)
            flags = tcp_pack.flags

            # 接收到rst，重置
            if flags[1] == 1:
                fsm.reset()
                self.__url_seq_map.pop(url)
                return

            # 这个时候syn应该为0
            if flags[2] == 1:
                return

            # 接受到第三次握手，建立连接
            # ack应该为自己的seq+1,seq应该为当前的seq+1
            ack = flags[0]
            expect_ack = self.__url_seq_map[url][0]
            expect_seq = self.__url_seq_map[url][1]
            if (ack == expect_ack) & (expect_seq == tcp_pack.seq):
                print('服务端收到第三个握手消息，建立连接')
                remote_seq = tcp_pack.seq + 1
                self.update_remote_seq(remote_seq, url)
                fsm.establish()
            return

        # 客户段和服务端均调用
        elif state is 'establish':
            print('收到对方消息')
            seq = tcp_pack.seq
            # 接受到的消息应该是连接中的seq
            expect_seq = self.__url_seq_map[url][1]
            if not seq == expect_seq:
                return

            # 将消息丢给上层应用
            msg = tcp_pack.data
            # 更新远程seq
            new_remote_seq = expect_seq + len(msg) + 1
            # new_remote_seq = expect_seq + 1
            self.update_remote_seq(new_remote_seq, url)
            # 将消息丢给上层应用
            app_port = tcp_pack.dest_port
            self.handle_message(msg, app_port)

    def update_remote_seq(self, remote_seq, url):
        (origin_seq, _) = self.__url_seq_map[url]
        self.__url_seq_map[url] = (origin_seq, remote_seq)

    # shell调用os发送消息
    def send_message(self, msg, url, app):
        """
        将敏文消息封装为ip报文,并为指定的app分配端口号
        :param url: 目标ip地址和端口号
        :param msg: 上层传递过来的消息
        :param app: 上层的应用
        :return: null
        """
        if not self.check_connection(url):
            # 建立连接
            self.establish_connection(url)

        # 解析url
        dest_ip = self.parse_url(url)[0]

        fsm: TCPFSM = self.get_tcp_fsm(url)
        state = fsm.state()

        if state is 'closed':
            # 将本来要发送的消息缓存
            cached_message = self.__url_message_map
            cached_message[url] = msg
            first_handshake = self.gen_tcp_pack(url, app)
            # syn=1,即第一次握手的包
            first_handshake.set_flags(syn=1)
            # 转换状态为send
            fsm.send()
            print('客户端发送第一次握手')
            print('客户端的seq', self.__url_seq_map[url][0])
            self.network_adapter.send_package(first_handshake, dest_ip)
            return
        elif state is 'syn_send':
            # 第三次握手应该在on_package来完成，所以这里就直接返回
            return
        elif state is 'syn_rcved':
            # 这种状态在发送包的时候不存在，直接return
            return
        elif state is 'establish':
            # 打包生成TCP包
            tcp_pack = self.gen_tcp_pack(url, app, msg)
            # 将TCP报文丢给网络适配器发送
            self.network_adapter.send_package(tcp_pack, dest_ip)
            return

    # os将消息丢到指定端口号的应用
    def handle_message(self, msg, port):
        """
        向上层返回消息
        :param msg: ip层拆包得到的消息
        :param port: 指定的端口号
        :return: null
        """
        p_map = self.__port_app__map
        app: Shell = p_map[port]
        app.handle_message(msg)
        pass

    # 解析url
    @staticmethod
    def parse_url(url):
        """
        解析url
        :param url:传入的url
        :return: ip地址,目标端口
        """
        url = str(url)
        index = url.index(':')
        return url[0:index], url[index + 1:len(url)]
        pass

    # 生成tcp报文s
    def gen_tcp_pack(self, url, app, msg=''):
        """
        把消息打包成tcp报文
        :param url: 目标url-> iP_addr:port形式
        :param app: 发送此报文的应用程序
        :param msg: tcp的消息内容
        :return: tcp报文对象
        """
        # 获取端口号
        origin_port = self.map_app_to_port(app)
        dest_port = self.parse_url(url)[1]

        # 获取或者生成seq
        seq_map = self.__url_seq_map
        if url in seq_map.keys():
            (seq, remote_seq) = seq_map[url]
        else:
            (seq, remote_seq) = random.randint(0, 4294967295), 0

        new_seq = seq + len(msg) + 1
        seq_map[url] = (new_seq, remote_seq)

        return TCPDatagram(origin_port, dest_port, data=msg, seq=seq)

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
        port = str(hash(app) % 65536)
        # 如果缓存了port的话,就直接返回端口
        if port not in self.__port_app__map.keys():
            # 缓存端口
            self.__port_app__map[port] = app
        return port

    # 检查是否检验了连接
    def check_connection(self, url):
        if url in self.__url_tcpfsm_map.keys():
            return True
        else:
            return False

    # 建立连接
    def establish_connection(self, url):
        # 初始化此TCP状态机
        fsm = TCPFSM()
        self.__url_tcpfsm_map[url] = fsm
        pass

    # 通过url获取状态机
    def get_tcp_fsm(self, url):
        return self.__url_tcpfsm_map[url]

    # 更新网络信息
    def update_network_info(self, package):
        """
        检测消息的类型，选择性更新network_info
        并根据消息的类型选择性丢弃消息
        :param package:
        :return:
        """
        # todo 更新 network_info
        return True

    # 获取本机的ip地址
    def get_ip_addr(self):
        return self.network_adapter.ip

    # 当shell被创建的时候会向os注册,让os分配它一个端口
    def register_app(self, app):
        self.map_app_to_port(app)

    # 操作系统注册的网络监听信息
    class __ListenerInfo:
        listeners = []

        def __init__(self):
            pass

        def on_package(self):
            for listener in self.listeners:
                if listener is NetWorkListener:
                    listener.on_package_received()

        def on_establish_connection(self, origin, dest):
            for listener in self.listeners:
                if listener is NetWorkListener:
                    listener.on_establish_connection(origin, dest)


def os_start():
    running_os = __OS()
    shell = HighPrivilegeShell(running_os)
    return shell
