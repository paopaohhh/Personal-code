import torch
import torchvision
from torch import nn
from model import *
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

############################第一步，获取并加载数据########################
#准备数据集
train_data = torchvision.datasets.CIFAR10("../dataset", train=True, transform=torchvision.transforms.ToTensor())
test_data = torchvision.datasets.CIFAR10("../dataset", train=False, transform=torchvision.transforms.ToTensor())

#数据长度
train_data_size = len(train_data)
test_data_szie = len(test_data)
print(f"训练集长度为{train_data_size}")
print(f"测试集长度为{test_data_szie}")

#加载数据集
batch_size =64
train_iter = DataLoader(train_data, batch_size=batch_size)
test_iter = DataLoader(test_data, batch_size=batch_size)

############################第二步，建立网络，设置损失函数、优化器，设置超参数########################
#创建网络模型
net = Mymodule()

#损失函数
loss = nn.CrossEntropyLoss()

#优化器
lr = 1e-2
optimer = torch.optim.SGD(net.parameters(), lr)

#记录训练和测试步骤
train_step = 0
test_step = 0

#使用Tensorboard
writer = SummaryWriter("../logs_完整神经网络")


############################第三步，训练、验证、测试########################
#训练
net.train() #进入训练模式，但是只对Dropout、BatchNorm层有作用
for epoch in range(10):
    print(f"----第{epoch+1:2d}轮训练开始----")
    l_sum=0
    for x, y in train_iter:
        output = net(x)
        l = loss(output, y)
        optimer.zero_grad()
        l.backward()
        optimer.step()
        train_step+=1

        if train_step%100 == 0:
            #l.item()会把tensor转换成常用的整数或浮点数
            print(f"第{train_step:6d}次训练，loss：{l.item()}")
            writer.add_scalar("Train_loss", l.item(), global_step=train_step)

    #测试开始
    l_sum=0.0
    #求总的精准度
    total_accuracy = 0.0
    with torch.no_grad():
        for x,y in test_iter:
            output = net(x)
            l = loss(output, y)
            l_sum+=l
            #求每次测试的精准度
            # .argmax(1)代表着对每一行的数据比大小，返回相应的列数，参数为0就是按列比大小，返回对应的行数
            # ==y会返回一个布尔类型的向量，.sum()操作就是把True当作1，False当作0，然后向量元素求和，最后得出分类正确的个数
            accuracy = (output.argmax(1) == y).sum()
            #把每一次正确的个数加到总正确个数上
            total_accuracy += accuracy
    print(f"第{epoch+1}轮测试，误差为：{l_sum/batch_size}")
    print(f"第{epoch+1}轮测试，准确率为{total_accuracy/test_data_szie}")
    writer.add_scalar("Test_loss", l_sum/batch_size, test_step)
    writer.add_scalar("Test_accuracy", total_accuracy/test_data_szie, test_step)
    test_step += 1

    #保存每一轮的模型和参数
    torch.save(net, f"net_{epoch+1}.pth")
    print(f"net{epoch+1}已经保存")

writer.close()