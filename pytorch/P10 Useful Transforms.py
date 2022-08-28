from PIL import Image
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter

img = Image.open("D:/中财云盘/用户文档/韩丰羽/深度学习/代码/PyTorch深度学习快速入门教程（绝对通俗易懂！）【小土堆】/hymenoptera_data/train/ants/0013035.jpg")
type(img)


class Person:
    def __call__(self, name):
        print("__call__" + "Hello" + name)

    def hello(self, name):
        print("hello" + name)


person = Person()
person("zhangsan")
# __call__方法会被直接调用，其他方法需要用 .方法名 的形式调用
person.hello("lisi")


class Person:
    def __call__(self, name):
        print("__call__" + "Hello" + name)

    def hello(self, name):
        print("hello" + name)


person = Person()
person("zhangsan")
# __call__方法会被直接调用，其他方法需要用 .方法名 的形式调用
person.hello("lisi")

#Totensor变为tensor类型，将输入的数据shape W，H，C ——> C，H，W
trans_totensor = transforms.ToTensor()
img_tensor = trans_totensor(img)
type(img_tensor)

writer = SummaryWriter("logs")
writer.add_image("Totensor", img_tensor)

#Normalize归一化
print(img_tensor[0][0][0])
#Normalize中给出均值和方差，图片为三通道，数据分布在[-1,1]
trans_norm = transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])
img_norm = trans_norm(img_tensor)
print(img_norm[0][0][0])
writer.add_image("Normalize", img_norm)

#Resize
print(img.size)
trans_size = transforms.Resize((512,512))
#img PIL -> resize -> img_resize PIL
img_resize = trans_size(img)
#img_resieze PIL -> Totensor -> img tensor
img_resize = trans_totensor(img_resize)
print(img_resize)
writer.add_image("Resize",img_resize)

#Compose Resize 2
trans_size_2 = transforms.Resize(512)
#transforms.Compose的参数需要是一个列表，数据类型是transform的类
#PIL -> Resize -> tensor
trans_compose = transforms.Compose([trans_size_2, trans_totensor])
img_resize_2 = trans_compose(img)
writer.add_image("Compose", img_resize_2)

#RandomCrop随机裁剪
trans_randomcrop = transforms.RandomCrop(512)
trans_compose_2 = transforms.Compose([trans_randomcrop, trans_totensor])
for i in range(10):
    img_crop = trans_compose_2(img)
    writer.add_image("RandomCrop", img_crop, i)

writer.close()