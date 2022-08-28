import torchvision
from PIL import Image
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter

'''
train_set = torchvision.datasets.CIFAR10(root = "./dataset", train=True, download=True)
test_set = torchvision.datasets.CIFAR10(root = "./dataset", train=False, download=True)
#会输出一个图片类型和一个数字，数字是代表package也就是分类的编号
print(test_set[0])
#因此可以直接获取图片的类型和其分类
img, target = test_set[0]

print(img)
print(target)
print(test_set.classes[target])
img.show()
'''

dataset_transform = transforms.Compose([transforms.ToTensor(), ])
train_set = torchvision.datasets.CIFAR10(root = "./dataset", transform=dataset_transform
                                         , train=True, download=True)
test_set = torchvision.datasets.CIFAR10(root = "./dataset", transform=dataset_transform
                                        , train=False, download=True)

writer = SummaryWriter("p14")
for i in range(10):
    image, target = test_set[i]
    writer.add_image("test_set", image, i)
writer.close()