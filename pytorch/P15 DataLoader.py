import torchvision
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader
from PIL import Image

#用DataLoader取出数据集
test_data = torchvision.datasets.CIFAR10("./dataset", train=False, transform=torchvision.transforms.ToTensor(),
                                         download=False)
test_loader = DataLoader(dataset=test_data, batch_size=64, shuffle=False, num_workers=0, drop_last=False)

#输出CIFAR10中第一张图片的信息
img, target = test_data[0]
print(img.shape)
print(target)

#表示DataLoader取出的数据集中的每一个样本
writer = SummaryWriter("DataLoader")

for epoch in range(2):
    step = 0
    for data in test_loader:
        img, target = data
        # print(img.shape)
        # print(target)
        writer.add_images(f"Epoch:{epoch}", img_tensor=img, global_step=step)
        step= step+1
writer.close()