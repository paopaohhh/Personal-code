from socket import *

# 创建tcp套接字

sockfd = socket()#此处如果是import socket方式，就和上述

# 发起连接
server_addr = ('10.11.222.113', 12000) # 服务端的网络地址
sockfd.connect(server_addr)

# 收发消息
message = input('输入你的信息：')
sockfd.send(message.encode())
data = sockfd.recv(1024)
print('From Server:', data.decode())

# 关闭
sockfd.close()