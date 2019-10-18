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
from src.util import looper
from threading import currentThread


class __OS(NetworkAdapter.CallBack):
    def __init__(self):
        self.network_info = NetworkInfo()
        self.listener_info = self.__ListenerInfo()
        self.handler = looper.loop()

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

    # 网络适配器回调此方法
    def on_package(self, package):
        """
        运行在网络适配器的线程中,将实际接受消息的方法丢在系统的消息队列里
        :param package: IP数据包
        :return: null
        """
        self.handler.post(fun=self.do_on_package, args=package)
        pass

    # 实际处理package的方法,运行在os线程
    def do_on_package(self, package: IPDatagram):
        """
        实际的on_package方法,处理收到的IP报文
        :param package 收到的IP报文
        :return: null
        """

        # 获取发送方的ip地址
        dest_ip = package.origin
        # 获取发送放的tcp报文
        tcp_pack: TCPDatagram = package.tcp_package

        # 获取端口号
        dest_port = tcp_pack.origin_port
        origin_port = tcp_pack.dest_port

        # 获取监听此端口的app
        if origin_port not in self.__port_app__map.keys():
            # 没有端口监听，说明对方端口号填错了
            return
        app = self.__port_app__map[origin_port]

        # 获取实际的url
        dest_url = dest_ip + ':' + dest_port
        key = dest_url + origin_port

        # 如果没有建立连接，那么就建立连接
        if not self.check_connection(dest_url, origin_port):
            # 会生成fsm
            self.establish_connection(dest_url, origin_port)

        fsm: TCPFSM = self.get_tcp_fsm(key)
        state = fsm.state()

        # 检查tcp序列号的有效性
        if not self.check_tcp_seq(tcp_pack.seq, key, state):
            # emmmm 为了达到效果，就不检查rst包的seq了
            if not tcp_pack.flags[1] == 1:
                return

        # 更新本地的网络计数器的信息
        if not self.update_network_info(tcp_pack):
            return

        # 通知网络监听者,这里是malware
        if self.listener_info is not None:
            self.listener_info.on_package()

        # 服务端调用,接受到了客户端的第一次握手的消息
        if state is 'closed':
            # 检查第一次握手包是否是syn形式
            # flag格式(ack,rst,syn)
            flags = tcp_pack.flags
            if flags[2] is not 1:
                return

            print(currentThread(), ':  server: 收到第一次握手消息')

            # 创建第二次握手的包
            second_shake = self.gen_tcp_pack(dest_url, origin_port)
            remote_seq = tcp_pack.seq
            self.update_remote_seq(remote_seq, dest_url, origin_port)
            second_shake.set_flags(ack=tcp_pack.seq + 1, syn=1)

            # 更新为syn_rcved状态
            fsm.receive()
            print(currentThread(), ':  server : 已发送第二次握手消息')
            self.send_tcp_package(second_shake, dest_ip)
            return

        # 客户端调用，发送了第一次握手后，收到回复的状态
        # 这个方法内部进行第三次TCP握手
        elif state is 'syn_send':

            # 检查服务器回复的消息是否是syn+ack的形式,并检查正确性
            flags = tcp_pack.flags
            if flags[2] is 0:
                return  # 非syn = 1直接return
            ack = flags[0]
            expect_ack = self.__url_seq_map[key][0] + 1
            if not ack == expect_ack:  # ack应该为自己的seq+1
                return

            print(currentThread(), ':  client:已收到第二次握手消息')

            # 缓存服务端的seq, +1是因为服务端的第二次握手占用了一个长度
            remote_seq = tcp_pack.seq
            self.update_remote_seq(remote_seq, dest_url, origin_port)

            # 进行第三次握手
            third_handshake = self.gen_tcp_pack(dest_url, origin_port)
            ack = tcp_pack.seq + 1
            # print('client : ', '发送的ack', ack)
            third_handshake.set_flags(ack)

            # 更新为establish状态
            fsm.establish()

            # 发送第三次握手消息
            print(currentThread(), ':  client:已发送第三次握手消息,建立连接')
            self.send_tcp_package(third_handshake, dest_ip)

            # 通知监听器,TCP握手已经完成
            origin = (self.get_ip_addr(), origin_port)
            dest = (dest_ip, dest_port)
            self.listener_info.on_establish_connection(origin, dest)

            # 将缓存的消息发送给服务器
            cached_msgs = self.__url_message_map[key]
            self.__url_message_map.pop(key)
            print(currentThread(), ':  client: 正在发送已缓存的消息')
            for msg in cached_msgs:
                self.do_send_message(msg, dest_url, app)
            return

        # 服务端调用，进行了第二次握手，等待客户端的第三个握手的状态
        elif state is 'syn_rcved':
            # flag格式(ack,rst,syn)
            flags = tcp_pack.flags

            # 接收到rst，重置
            if flags[1] == 1:
                print(currentThread(), ':  server', '收到rst,关闭连接')
                fsm.reset()
                self.__url_seq_map.pop(key)
                return

            # 这个时候syn应该为0
            if flags[2] == 1:
                return

            # 接受到第三次握手，判断ack
            ack = flags[0]
            expect_ack = self.__url_seq_map[key][0] + 1
            # print('server', 'ack is ', ack)
            # print('server', 'expect ack is ', expect_ack)
            if ack == expect_ack:
                print(currentThread(), ':  server:收到第三次握手消息，建立连接')
                remote_seq = tcp_pack.seq
                self.update_remote_seq(remote_seq, dest_url, origin_port)
                fsm.establish()
            return

        # 建立连接后接收到消息调用
        elif state is 'establish':
            print('------收到对方消息-----')

            remote_seq = tcp_pack.seq

            # 更新remote的seq
            msg = tcp_pack.data
            new_remote_seq = remote_seq + len(msg)
            self.update_remote_seq(new_remote_seq, dest_url, origin_port)

            # 将消息丢给上层应用
            app_port = tcp_pack.dest_port
            self.dispatch_message(msg, app_port, dest_url)
            return

    # 更新tcp连接中的对方的seq
    def update_remote_seq(self, remote_seq, url, origin_port):
        """
        :param remote_seq: 连接对方的seq
        :param url: 连接对方的url
        :param origin_port: 自己的端口号
        :return:
        """
        key = url + origin_port
        (origin_seq, _) = self.__url_seq_map[key]
        self.__url_seq_map[key] = (origin_seq, remote_seq)
        return

    # 检验tcp序列号的有效性
    def check_tcp_seq(self, remote_seq, key, state):
        # 如果是关闭状态和syn_send状态，默认返回True
        if (state is 'closed') | (state is 'syn_send'):
            return True
        expect_seq = self.__url_seq_map[key][1]
        return remote_seq >= expect_seq

    # 实际通过os发送消息
    def do_send_message(self, msg, dest_url, app):
        """
        将消息封装为ip报文,并为指定的app分配端口号
        :param dest_url: 目标ip地址和端口号
        :param msg: 上层传递过来的消息
        :param app: 上层的应用
        :return: null
        """
        # 获取当前app对应的端口号
        origin_port = self.map_app_to_port(app)

        if not self.check_connection(dest_url, origin_port):
            # 建立连接
            self.establish_connection(dest_url, origin_port)

        # 解析url
        dest_ip = self.parse_url(dest_url)[0]

        key = dest_url + origin_port

        fsm: TCPFSM = self.get_tcp_fsm(key)
        state = fsm.state()

        # closed即为还未建立连接，这个时候进行第一次握手
        if state is 'closed':
            # 将本来要发送的消息缓存
            cached_message = self.__url_message_map
            cached_message[key] = [msg]

            # 生成第一次握手的tcp包
            first_handshake = self.gen_tcp_pack(dest_url, origin_port)
            first_handshake.set_flags(syn=1)

            # 转换状态为send
            fsm.send()
            self.send_tcp_package(first_handshake, dest_ip)
            print(currentThread(), ':  client: 已发送第一次握手消息')
            return

        # 如果正在握手，但是又有新的消息到来,就将新的消息缓存
        elif state is 'syn_send':
            cached_message = self.__url_message_map
            cached_message[key].append(msg)
            return

        # 这种状态在发送包的时候不存在，直接return
        elif state is 'syn_rcved':
            return

        # 如果已经建立连接了，那么就直接发送消息
        elif state is 'establish':
            # 打包生成TCP包
            tcp_pack = self.gen_tcp_pack(dest_url, origin_port, msg)
            # 将TCP报文丢给网络适配器发送
            self.send_tcp_package(tcp_pack, dest_ip)
            return

    # shell调用os发送消息
    def send_message(self, msg, dest_url, app):
        self.handler.post(fun=self.do_send_message, args=(msg, dest_url, app))
        pass

    # 将TCP报文丢给网络适配器发送
    def send_tcp_package(self, tcp_pack, dest_ip):
        ip_addr = self.get_ip_addr()
        ip_pack = IPDatagram(tcp_pack, ip_addr, dest_ip)
        self.network_adapter.send_package(ip_pack=ip_pack)
        return

    # 让网络适配器直接发送IP报文
    def send_ip_package(self, ip_pack):
        self.network_adapter.send_package(ip_pack=ip_pack)

    # os将消息丢到指定端口号的应用
    def dispatch_message(self, msg, port, msg_source):
        """
        向上层返回消息
        :param msg_source: 消息的源头
        :param msg: ip层拆包得到的消息
        :param port: 指定的端口号
        :return: null
        """
        p_map = self.__port_app__map
        app: Shell = p_map[port]
        app.handle_message(msg, msg_source)
        return

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

    # 生成tcp报文
    def gen_tcp_pack(self, url, origin_port, msg=''):
        """
        把消息打包成tcp报文
        :param url: 目标url-> iP_addr:port形式
        :param origin_port: 发送此报文的端口号
        :param msg: tcp的消息内容
        :return: tcp报文对象
        """
        # 获取key
        key = url + origin_port
        # 获取目标端口号
        dest_port = self.parse_url(url)[1]
        # 获取或者生成seq
        seq_map = self.__url_seq_map
        if key in seq_map.keys():
            (seq, remote_seq) = seq_map[key]
        else:
            (seq, remote_seq) = random.randint(0, 4294967295), 0

        # 根据当前消息的长度更新seq
        new_seq = seq + len(msg)
        seq_map[key] = (new_seq, remote_seq)

        return TCPDatagram(origin_port, dest_port, data=msg, seq=seq)

    # 添加网络包的监听器
    def add_network_listener(self, listener):
        self.listener_info.listeners.append(listener)
        return

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
    def check_connection(self, url, origin_port):
        """
        检查本地是否有该当前端口号和目标ip对应的tcp状态机
        :param url: 目标ip
        :param origin_port: 当前端口号
        :return:
        """
        key = url + origin_port
        if key in self.__url_tcpfsm_map.keys():
            return True
        else:
            return False

    # 建立连接
    def establish_connection(self, url, origin_port):
        # 初始化此TCP状态机
        key = url + origin_port
        self.__url_tcpfsm_map[key] = TCPFSM()
        return

    # 通过url获取状态机
    def get_tcp_fsm(self, key):
        return self.__url_tcpfsm_map[key]

    # 更新网络信息
    def update_network_info(self, package: TCPDatagram):
        """
        检测消息的类型，选择性更新network_info
        并根据消息的类型选择性丢弃消息
        :param package: TCP数据包
        :return: 该消息是否有效
        """
        tpe = package.tpe
        res = tpe == -1
        self.network_info.update(tpe)
        return res

    # 获取本机的ip地址
    def get_ip_addr(self):
        return self.network_adapter.ip

    # 当shell被创建的时候会向os注册,让os分配它一个端口
    def register_app(self, app):
        self.map_app_to_port(app)
        return

    # 操作系统注册的网络监听信息
    class __ListenerInfo:

        def __init__(self):
            self.listeners = []
            pass

        # 接收到消息的时候，广播所有的listener
        def on_package(self):
            for listener in self.listeners:
                if isinstance(listener, NetWorkListener):
                    listener.on_package_received()
            return

        # 建立了连接的时候，广播所有的listener
        def on_establish_connection(self, origin, dest):
            for listener in self.listeners:
                if isinstance(listener, NetWorkListener):
                    listener.on_establish_connection(origin, dest)
            return


def os_start():
    running_os = __OS()
    shell = HighPrivilegeShell(running_os)
    return shell
