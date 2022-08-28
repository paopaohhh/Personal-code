#找到网络模型、数据、损失函数，加上.to(device)就可以使用GPU来训练

import torch
import torchvision
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
import time #用来计时

#定义设备 双引号里可以写"cuda""cuda:0"
# device = torch.device("cpu")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

#创建网络模型
class Mymodule(nn.Module):
    def __init__(self):
        super(Mymodule, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3,32,5,1,2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,32,5,1,2),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 5, 1, 2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64*4*4, 64),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        x = self.model(x)
        return x

if __name__ == '__main__':
    mymodule = Mymodule()
    input = torch.rand(size = (64,3,32,32))
    output = mymodule(input)
    print(output.shape)

net = Mymodule()
        #对模型使用cuda
net = net.to(device)

#损失函数
loss = nn.CrossEntropyLoss()
        #对损失函数使用cuda
loss = loss.to(device)

#优化器
lr = 1e-2
optimer = torch.optim.SGD(net.parameters(), lr)

#记录训练和测试步骤
train_step = 0
test_step = 0

#使用Tensorboard
writer = SummaryWriter("../logs_完整神经网络")
#记录开始时间
start_time = time.time()

#训练
net.train() #进入训练模式，但是只对Dropout、BatchNorm层有作用
for epoch in range(10):
    print(f"----第{epoch+1:2d}轮训练开始----")
    l_sum=0
    for data in train_iter:
        # 对训练集使用cuda
        x,y=data
        x = x.to(device)
        y = y.to(device)
        output = net(x)
        l = loss(output, y)
        optimer.zero_grad()
        l.backward()
        optimer.step()
        train_step+=1

        if train_step%100 == 0:
            #l.item()会把tensor转换成常用的整数或浮点数
            print(f"第{train_step:6d}次训练，loss：{l.item()}")
            #记录结束时间
            end_time = time.time()
            #打印出从开始到现在所花费的时间
            print(end_time-start_time)
            writer.add_scalar("Train_loss", l.item(), global_step=train_step)

    #测试开始
    l_sum=0.0
    #求总的精准度
    total_accuracy = 0.0
    with torch.no_grad():
        for data in test_iter:
            x,y=data
            #对测试集使用cuda
            x = x.to(device)
            y = y.to(device)
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