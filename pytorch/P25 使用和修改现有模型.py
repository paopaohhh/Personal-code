import torch
import torchvision
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

# dataset = torchvision.datasets.ImageNet("../data_Imagenet", split='train', download=True,
#                                         transform=torchvision.transforms.ToTensor())
# dataloader = DataLoader(dataset, batch_size=64)

vgg16_false = torchvision.models.vgg16(pretrained=False)
vgg16_true = torchvision.models.vgg16(pretrained=True)

# print(vgg16_true)

train_data = torchvision.datasets.CIFAR10("../dataset", train=True, transform=torchvision.transforms.ToTensor(),
                                          download=True)
train_iter = DataLoader(train_data, batch_size=64)

vgg16_true.add_module("add_linear", nn.Linear(1000, 10))
print(vgg16_false)
#改变classifier中的层
vgg16_false.classifier[6] = nn.Linear(4096, 10)
print(vgg16_false)