import numpy as np
import pandas as pd
import torch
from torch.utils import data
from d2l import torch as d2l

true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = d2l.synthetic_data(true_w, true_b, 1000)   #生成随机数据集

def load_array(data_array, batch_size , is_trian=True):
    dataset = data.TensorDataset(*data_array)
    #   *代表序列解包 https://blog.csdn.net/yilovexing/article/details/80576788
    return data.DataLoader(dataset, batch_size, shuffle=is_trian)

batch_size = 10
data_iter = load_array((features, labels), batch_size)
next(iter(data_iter))

# `nn` 是神经网络的缩写
from torch import nn
net= nn.Sequential(nn.Linear(2,1))  #输入的维度是2，输出的维度是1

net[0].weight.data.normal_(0,0.01)
#.weight访问w，.data访问全部数据，.normal_转换为高斯分布
net[0].bias.data.fill_(0)
#.bias访问b，.fill_(0)全部填充为0

loss = nn.MSELoss()  #平方L2范数，默认情况下，它返回所有样本损失的平均值。
trainer = torch.optim.SGD(net.parameters(), lr=0.03)
#梯度下降的函数，至少要写两个参数，net.parameters()代表net里全部的数据，lr是学习率

num_epochs = 3
for epoch in range(num_epochs):
    for X,y in data_iter:
        l=loss(net(X), y)
        trainer.zero_grad()
        l.backward()  #这里pytorch已经做了求和
        trainer.step()
    l=loss(net(features), labels)
    print(f'epoch {epoch + 1}, loss {l:f}')

w = net[0].weight.data
print('w的估计误差：', true_w - w.reshape(true_w.shape))
b = net[0].bias.data
print('b的估计误差：', true_b - b)