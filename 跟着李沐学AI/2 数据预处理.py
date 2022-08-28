import os
import pandas as pd
os.makedirs(os.path.join('..','data'), exist_ok=True)
data_file = os.path.join('..','data', 'house_tiny.csv')
with open(data_file, 'w') as f:
    f.write('NumRooms, Alley, price\n')
    f.write('Na, Pave, 127500\n')
    f.write('2, NA,106000\n')
    f.write('4,NA,1781000\n')
    f.write('NA,NA,140000\n')

data = pd.read_csv(data_file)
print(data)