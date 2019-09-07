import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import sklearn.linear_model as slm

data = pd.read_csv('data/heart.csv')
data = data.dropna()
print(data)

rows = random.sample(2)
print(rows)



# data_100 = data.loc[rows]
# data_300 = data.drop(rows)

# data_lst = data_mtx.tolist()
# print(data_lst)
# print(random.sample(data_lst, 100))

#
# data1 = data.drop("target000", axis=1)
# data2 = data.target000
#
# data1_mtx = np.matrix(data1)
# data1_list = data1_mtx.tolist()
# data2_mtx = np.matrix(data2)
# data2_list = data2_mtx.tolist()
# print(data2_list)
#


