import torch
import numpy as np
import d2l

def synthetic_data(w, b, num_examples):
    X=torch.normal(0, 1, (num_examples, len(w)))
    y=torch.matmul(X,w) + b
    y+=torch.normal(0, 0.01, y.shape)
    return X, y.reshape(-1,1)

true_w= torch.tensor([2,-3.4])
true_b = 4.2
features, labels = synthetic_data(true_w, true_b, 1000)

def data_iter(batch_size, features, labels):
    num_examples = len(features)
    indices = list(range(num_examples))
    np.random.shuffle(indices)

    for i in range(0, num_examples, batch_size):
        batch_indices = indices[i:min(num_examples,i+batch_size)]
        yield features[batch_indices], labels[batch_indices]

batch_size = 10
for X,y in data_iter(batch_size, features, labels):
    print('X=',X, '/ny=', y)
    break

w=torch.normal(0,1,(2,1),requires_grad=True)
b=torch.zeros(1, requires_grad=True)

def linreg(X, w, b):
    return torch.matmul(X,w)+b

def squared_loss(y_hat, y, batch_size):
    '''线性回归模型'''
    return (y_hat-y.reshape(y.shape))**2/2/batch_size

def sgd(params, lr):  #@save
    """小批量随机梯度下降。"""
    with torch.no_grad(): #不参与梯度计算
        for param in params:
            param -= lr * param.grad
            param.grad.zero_()

lr = 0.03
num_epochs = 3  #整个数据迭代3遍
net = linreg
loss = squared_loss

for epoch in range(num_epochs):
    for X,y in data_iter(batch_size, features, labels):
        l=loss(net(X,w,b), y,batch_size)
        l.sum().backward()
        sgd([w,b], lr)
    with torch.no_grad():
        train_l = loss(net(features, w, b), labels, batch_size)
        print(f'epoch {epoch + 1}, loss {float(train_l.mean()):f}')