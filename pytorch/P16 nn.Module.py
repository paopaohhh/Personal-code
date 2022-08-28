from torch import nn
import torch
import torch.nn.functional as F

class Paopao(nn.Module):
    def __init__(self):
        super(Paopao, self).__init__()
        self.conv1 = nn.Conv2d(1,20,5)

    def forward(self, input):
        output = F.relu(self.conv1(input))
        return output

paopao = Paopao()
x = torch.arange(25).resize(5,5)
output = paopao(x)
output