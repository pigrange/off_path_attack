# off_path_attack

### Features

- [x] TCP有限状态机
- [x] 网络的基本结构
- [x] 网络节点的事件驱动
- [ ] Attacker


### Structure
```
|-- __init__.py
|-- components
|   |-- attacker
|   |   |-- attack_server.py
|   |   `-- malware.py
|   |-- end_host
|   |   |-- phone.py
|   |   |-- server.py
|   |   `-- system_service
|   |       |-- framework
|   |       |   |-- shell.py
|   |       |   `-- x_os.py
|   |       |-- network
|   |       |   |-- network_info.py
|   |       |   |-- network_listener.py
|   |       |   `-- tcp_fsm.py
|   |       `-- user_interface.py
|   `-- network
|       |-- base
|       |   `-- network_node.py
|       |-- core
|       |   |-- filewall.py
|       |   |-- network_adapter.py
|       |   `-- router.py
|       |-- datagram
|       |   |-- ip_datagram.py
|       |   `-- tcp_datagram.py
|       `-- network.py
|
|-- main.py
|
`-- util          
    |-- handler.py
    `-- looper.py 
```

