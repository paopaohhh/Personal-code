#找到网络模型、数据、损失函数，加上.cuda()就可以使用GPU来训练

# PyTorch深度学习快速入门教程（绝对通俗易懂！）【小土堆】
# https://www.bilibili.com/video/BV1hE411t7RN?spm_id_from=333.999.header_right.fav_list.click

# 例子代码只是给定超参数训练和测试过程，没有验证和调参，调参需要手动进行，超参数包括学习率lr和批量大小batch_size
# 如果需要使用GPU，需要在神经网络、损失函数和数据集后加.cuda()，.cuda()把数据放在GPU的显存上

# 1. 读取数据
# 2. 做成迭代器
# 3. 定义神经网络、损失函数、优化器、各种超参数（batch_size迭代器每次取出样本的数量, learning_rate学习率）
# 4. 训练测试
# 5. 保存模型和参数


import torch # pytorch
import torchvision # torchvision.transforms 转换数据类型.ToTensor()转换为tensor, .Normlize()批量归一化, .Resize()改变大小
from torch import nn # linear, conv2d, maxpool, dropout, BatchNorm
from torch.utils.data import DataLoader # 迭代器，用来每次取确定数量的数据
from torch.utils.tensorboard import SummaryWriter # 数据可视化
import time #用来计时


############################第一步，获取并加载数据########################
#准备数据集
train_data = torchvision.datasets.CIFAR10("../dataset", train=True, transform=torchvision.transforms.ToTensor(), download=False) # .ToTensor()维度变化CHW -> WHC
test_data = torchvision.datasets.CIFAR10("../dataset", train=False, transform=torchvision.transforms.ToTensor(), download=False)
# 数据集是现成的，
# x, y = train_data
# 数据长度
train_data_size = len(train_data)
test_data_szie = len(test_data)
print(f"训练集长度为{train_data_size}")
print(f"测试集长度为{test_data_szie}")

#加载数据集
batch_size = 64
train_iter = DataLoader(train_data, batch_size=batch_size) # 做一个数据的迭代器
test_iter = DataLoader(test_data, batch_size=batch_size)

#创建网络模型
# class Mymodule(nn.Module):
#     def __init__(self):
#         super(Mymodule, self).__init__()
#         self.model = nn.Sequential(
#             nn.Conv2d(3,32,5,1,2),
#             nn.MaxPool2d(2),
#             nn.Conv2d(32,32,5,1,2),
#             nn.MaxPool2d(2),
#             nn.Conv2d(32, 64, 5, 1, 2),
#             nn.MaxPool2d(2),
#             nn.Flatten(),
#             nn.Linear(64*4*4, 64),
#             nn.Linear(64, 10)
#         )
#
#     def forward(self, x):
#         x = self.model(x)
#         return x

net = nn.Sequential(  # 神经网络
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
# if torch.cuda.is_available():
    # net = net.cuda()

# if __name__ == '__main__':
#     mymodule = Mymodule()
#     input = torch.rand(size = (64,3,32,32))
#     output = mymodule(input)
#     print(output.shape)


############################第二步，建立网络，设置损失函数、优化器，设置超参数########################
# net = Mymodule()
        #对模型使用cuda
# if torch.cuda.is_available():
    # net = net.cuda()

#损失函数
loss = nn.CrossEntropyLoss()
        #对损失函数舒勇cuda
# if torch.cuda.is_available():
    # loss = loss.cuda()

#优化器
lr = 1e-2
optimer = torch.optim.SGD(net.parameters(), lr)

#记录训练和测试步骤
train_step = 0
test_step = 0

#使用Tensorboard
writer = SummaryWriter("../logs_完整神经网络") # 定义训练结果保存的文件夹
# 运行完程序，在terminal显示图表的命令： tensorboard --logdir logs_完整神经网络
#记录开始时间
start_time = time.time()


############################第三步，训练、验证、测试########################
#训练
net.train() #进入训练模式，但是只对Dropout、BatchNorm层有作用
for epoch in range(10):
    print(f"----第{epoch+1:2d}轮训练开始----")
    l_sum=0
    for data in train_iter: # 从迭代器取数据，train_iter从全部训练集中每次取batch_size个数据，直到全部取完
        # 对训练集使用cuda
        x,y=data
        # if torch.cuda.is_available():
            # x = x.cuda()
            # y = y.cuda()
        output = net(x) # 预测
        l = loss(output, y) # 计算损失，y是实际分类，output是预测
        optimer.zero_grad() # 梯度清零
        l.backward() # 反向传播
        optimer.step() # 更新一次神经网络内部参数
        train_step+=1 # 训练步骤+1

        if train_step%100 == 0: # 每100次训练，报告一次loss，记录并画图
            #l.item()会把tensor转换成常用的整数或浮点数
            print(f"第{train_step:6d}次训练，loss：{l.item()}")
            #记录结束时间
            end_time = time.time()
            #打印出从开始到现在所花费的时间
            print(end_time-start_time)
            writer.add_scalar("Train_loss", l.item(), global_step=train_step) # 画图

    #测试开始
    # l_sum=0.0
    #求总的精准度
    total_num_correct = 0.0
    with torch.no_grad(): # 不参与梯度下降
        for data in test_iter:
            x, y = data
            #对测试集使用cuda
            # if torch.cuda.is_available():
                # x = x.cuda()
                # y = y.cuda()
            output = net(x)
            l = loss(output, y) # y的元素都是0和1，
            # l_sum+=l
            #求每次测试的精准度
            # .argmax(1)代表着对每一行的数据比大小，返回相应的列数，参数为0就是按列比大小，返回对应的行数
            # ==y会返回一个布尔类型的向量，.sum()操作就是把True当作1，False当作0，然后向量元素求和，最后得出分类正确的个数
            num_correct = (output.argmax(1) == y).sum()
            # 假设是五分类问题，单个样本输出维度是5，每个维度代表分类的可能性
            # output = (.1,.2,.3,.4,.5), output.argmax(1) = (0,0,0,0,1)  y = (0,1,0,0,0)  (output.argmax(1) == y).sum() = 0
            # output = (.1,.2,.3,.4,.5), output.argmax(1) = (0,0,0,0,1)  y = (0,0,0,0,1)  (output.argmax(1) == y).sum() = 1
            # 把每一次正确的个数加到总正确个数上
            total_num_correct += num_correct # 这个样本预测正确accuracy为1，预测错误accuracy为0
    # print(f"第{epoch+1}轮测试，误差为：{l_sum/batch_size}")
    print(f"第{epoch+1}轮测试，准确率为{total_num_correct/test_data_szie}")
    # writer.add_scalar("Test_loss", l_sum/batch_size, test_step)
    writer.add_scalar("Test_accuracy", total_num_correct/test_data_szie, test_step) # 画图
    test_step += 1

    #保存每一轮的模型和参数
    torch.save(net, f"net_{epoch+1}.pth")
    print(f"net{epoch+1}已经保存")

writer.close() # 把Summarywriter工具关闭