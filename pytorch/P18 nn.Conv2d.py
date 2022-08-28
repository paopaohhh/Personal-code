import torch
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn

dataset = torchvision.datasets.CIFAR10("../data", train=True, transform=torchvision.transforms.ToTensor(),
                                       download=True)
dataloader = DataLoader(dataset, batch_size=64)

class Mymodule(nn.Module):
    def __init__(self):
        super(Mymodule, self).__init__()
        #这里是彩色图片，所以输入是RGB三通道
        self.conv1 = nn.Conv2d(3,6,3, stride=1, padding=0)

    def forward(self,x):
        x =self.conv1(x)
        return x

mymodule = Mymodule()
writer = SummaryWriter("../logs")

step=0
for data in dataloader:
    img, target = data
    output = mymodule(img)
    print(img.shape)
    print(output.shape)
    #input.size(64,3,32,32)
    writer.add_images("input", img, step)
    #output.size(64,6,30,30)
    output = torch.reshape(output, (-1, 3, 30, 30 ))
    writer.add_images("output", output, step)
    step = step+1
