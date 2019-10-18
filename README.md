# off_path_attack

### Features

- [x] TCP有限状态机
- [x] 单链表构成的网络的基本结构
- [x] 运行在独立线程上，基于事件驱动的网络节点
- [x] 攻击者服务器和恶意软件
- [x] 防火墙和滑动窗口
- [ ] TCP序列号预测


### Structure
```                                                                        
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
|   |       |   |-- sliding_window.py                   
|   |       |   `-- tcp_fsm.py                          
|   |       `-- user_interface.py                       
|   `-- network                                         
|       |-- __init__.py                                              
|       |-- base                                        
|       |   |-- __init__.py                                  
|       |   `-- network_node.py                         
|       |-- core                                        
|       |   |-- __init__.py                                   
|       |   |-- firewall.py                             
|       |   |-- network_adapter.py                      
|       |   `-- router.py                               
|       |-- datagram                                    
|       |   |-- __init__.py                                   
|       |   |-- ip_datagram.py                          
|       |   `-- tcp_datagram.py                         
|       `-- network.py            
                      
|-- main.py                                             
|                               
`-- util                                                
    |-- __init__.py                                                       
    |-- handler.py                                      
    `-- looper.py   
```

