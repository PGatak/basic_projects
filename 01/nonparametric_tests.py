from scipy import stats
from preparation import data_1, data_2

print("\n\t\t\t\tdata_1.PRZED_1, data_1.PO_1")
print(sum(data_1.PRZED_1) / len(data_1.PRZED_1))
print(sum(data_1.PO_1) / len(data_1.PO_1))
test = stats.ttest_rel(data_1.PRZED_1, data_1.PO_1)
print(test)
test = stats.wilcoxon(data_1.PRZED_1, data_1.PO_1)
print(test)

print("\n\t\t\t\tdata_2.PRZED_2, data_2.PO_2")
print(sum(data_2.PRZED_2) / len(data_2.PRZED_2))
print(sum(data_2.PO_2) / len(data_2.PO_2))
test = stats.ttest_rel(data_2.PRZED_2, data_2.PO_2)
print(test)
test = stats.wilcoxon(data_2.PRZED_2, data_2.PO_2)
print(test)

print("\n\t\t\t\tdata_1.PRZED_1, data_2.PRZED_2")
print(sum(data_1.PRZED_1) / len(data_1.PRZED_1))
print(sum(data_2.PRZED_2) / len(data_2.PRZED_2))
test = stats.ttest_ind(data_1.PRZED_1, data_2.PRZED_2)
print(test)
test = stats.mannwhitneyu(data_1.PRZED_1, data_2.PRZED_2)
print(test)

print("\n\t\t\t\tdata_1.PO_1, data_2.PO_2")
print(sum(data_1.PO_1) / len(data_1.PO_1))
print(sum(data_2.PO_2) / len(data_2.PO_2))
test = stats.ttest_ind(data_1.PO_1, data_2.PO_2)
print(test)
test = stats.mannwhitneyu(data_1.PO_1, data_2.PO_2)
print(test)
