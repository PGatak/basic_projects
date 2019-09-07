from preparation import data_1, data_2
from normal_distribution_test_models import *


print(basic_test(data_1.PRZED_1))
print(skew_test(data_1.PRZED_1))
print(kurtosis_test(data_1.PRZED_1))
print(shapiro_test(data_1.PRZED_1))
print(kstest_test(data_1.PRZED_1), "\n")

print(basic_test(data_1.PO_1))
print(skew_test(data_1.PO_1))
print(kurtosis_test(data_1.PO_1))
print(shapiro_test(data_1.PO_1))
print(kstest_test(data_1.PO_1), "\n")

print(basic_test(data_2.PRZED_2))
print(skew_test(data_2.PRZED_2))
print(kurtosis_test(data_2.PRZED_2))
print(shapiro_test(data_2.PRZED_2))
print(kstest_test(data_2.PRZED_2), "\n")


print(basic_test(data_2.PO_2))
print(skew_test(data_2.PO_2))
print(kurtosis_test(data_2.PO_2))
print(shapiro_test(data_2.PO_2))
print(kstest_test(data_2.PO_2))


plot_test(data_1.PRZED_1, 1)
plot_test(data_1.PO_1, 2)
plot_test(data_2.PRZED_2, 3)
plot_test(data_2.PO_2, 4)
plt.show()
