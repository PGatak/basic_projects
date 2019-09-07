import pandas as pd

data_all = pd.read_excel('data/Dane.xlsx', names=["NR", "PRZED_1", "PO_1", "PRZED_2", "PO_2"])
data_all.index = data_all.NR
data_all = data_all.drop("NR", axis=1)

data_1 = data_all.iloc[:, :2]
data_1 = data_1.dropna()
data_2 = data_all.iloc[:, 2:]
data_1 = data_1.dropna()
