# @coding: utf-8
# @Author: john pig
# @Date: 10/15/2019 9:58 AM
# @Tool: PyCharm
# @Description:

from src.components.attacker import malware
from src.components.end_host.phone import Phone
from src.components.end_host.server import Server
from src.components.network.core import router


def main():
    m_phone = Phone(name='iphone')
    router.add_router_to_net(router_count=6, has_firewall=True)
    malware.infect(m_phone)
    m_server = Server(name='linux_server')

    url = m_server.get_url()

    m_phone.post_message(url, msg='hello world')
    m_phone.post_message(url, msg='how are you')
    pass


if __name__ == '__main__':
    main()
