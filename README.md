# off_path_attack

### Features

- [x] TCP有限状态机
- [x] 网络的基本结构
- [ ] 网络节点的事件驱动
- [ ] Attacker


### Structure
```
|-- __init__.py
|-- components
|   |-- __init__.py
|   |-- attacker
|   |   |-- __init__.py
|   |   |-- attack_server.py
|   |   `-- malware.py
|   |-- end_host
|   |   |-- __init__.py
|   |   |-- phone.py
|   |   |-- server.py
|   |   `-- system_service
|   |       |-- __init__.py
|   |       |-- framework
|   |       |   |-- __init__.py
|   |       |   |-- shell.py
|   |       |   `-- x_os.py
|   |       |-- network
|   |       |   |-- __init__.py
|   |       |   |-- network_info.py
|   |       |   |-- network_listener.py
|   |       |   `-- tcp_fsm.py
|   |       `-- user_interface.py
|   `-- network
|       |-- __init__.py
|       |-- base
|       |   |-- __init__.py
|       |   `-- network_node.py
|       |-- core
|       |   |-- __init__.py
|       |   |-- filewall.py
|       |   |-- network_adapter.py
|       |   `-- router.py
|       |-- datagram
|       |   |-- __init__.py
|       |   |-- ip_datagram.py
|       |   `-- tcp_datagram.py
|       `-- network.py
|-- main.py
```