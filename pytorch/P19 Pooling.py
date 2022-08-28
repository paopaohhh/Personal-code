import torch
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn

dataset = torchvision.datasets.CIFAR10("../data", train=False, download=True
                                       , transform=torchvision.transforms.ToTensor())
dataloader = DataLoader(dataset, batch_size=64)
input = torch.tensor([[1,2,0,3,1],
                      [0,1,2,3,1],
                      [1,2,1,0,0],
                      [5,2,3,1,1],
                      [2,1,0,1,1]], dtype=torch.float32)
input = torch.reshape(input, (-1,1,5,5,))
print(input.shape)

class Mymodule(nn.Module):
    def __init__(self):
        super(Mymodule, self).__init__()
        #ceil_mode=True代表用ceil而不是floor，floor是向下取整，ceil是向上取整
        self.maxpool1 = nn.MaxPool2d(kernel_size=3, ceil_mode=True)

    def forward(self, input):
        output = self.maxpool1(input)
        return output

mymodule = Mymodule()

writer = SummaryWriter("logs_maxpool")
step = 0
for data in dataloader:
    img, target = data
    writer.add_images("input", img, step)
    output = mymodule(img)
    writer.add_images("output", output, step)
    step = step+1
writer.close()