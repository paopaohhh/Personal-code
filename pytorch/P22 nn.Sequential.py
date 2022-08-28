import torch
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn

# dataset = torchvision.datasets.CIFAR10("../data", train=False, transform=torchvision.transforms.ToTensor()
#                                        , download=False)
# dataloader = DataLoader(dataset, batch_size=64, num_workers=2, drop_last=True)

class Mymodule(nn.Module):
    def __init__(self):
        super(Mymodule, self).__init__()
        self.model1 = nn.Sequential(
            nn.Conv2d(3, 32, 5, padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 32, 5, padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 5, padding=2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(1024, 64),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        x = self.model1(x)
        return x

input = torch.rand(size = (64,3,32,32))
print(input)

mymodule = Mymodule()

output = mymodule(input)
print(output)

writer = SummaryWriter("logs")
writer.add_graph(mymodule, input)
writer.close()