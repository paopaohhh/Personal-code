import numpy as np
data = np.arange(36).reshape(9,4)
k=4
k_sample_count = data.shape[0]//k

for fold in range(k):
    validation_begin = k_sample_count*fold
    validation_end = k_sample_count*(fold +1)
    
    validation_data = data[validation_begin:validation_end]
    
    """np.vstack, 沿着垂直方向堆叠数组"""
    train_data = np.vstack([data[:validation_begin],
                            data[validation_end:]])

    print()
    print(f'####第{fold}折####')
    print('验证集：\n',validation_data)
    print('训练集：\n',train_data)