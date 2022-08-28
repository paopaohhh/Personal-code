import torch
import torchvision
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

vgg = torchvision.models.vgg16(pretrained=False)

#保存方式1 模型结构+模型参数
torch.save(vgg, "vgg16_mothed1.pth")
#加载方式1
model1 = torch.load("vgg16_mothed1.pth")
print("model1:",model1)

#保存方式2 模型参数(官方推荐)
torch.save(vgg.state_dict(), "vgg16_method2.pth")
#加载方式2
model2 = torchvision.models.vgg16(pretrained=False)
model2.load_state_dict(torch.load("vgg16_method2.pth"))
print("model2:",model2)