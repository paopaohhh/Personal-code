'''
TCP 套接字服务端重点代码
'''

import socket

# 创建流式套接字
sockfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定本机地址
sockfd.bind(('10.11.222.113',12000))

# 设置监听
sockfd.listen(5)

# 等待客户端连接
print('Waiting for connect...')
connfd, addr = sockfd.accept()

# 收发消息
data = connfd.recv(1024)
print('接收到的消息: ', data.decode())

n = connfd.send('Received your message'.encode())# 注意发送字节串，也可以encode
print('发送了%d个字节数据' % n)

# 关闭套接字
connfd.close()
sockfd.close()
