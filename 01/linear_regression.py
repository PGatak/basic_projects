import numpy as np
import matplotlib.pyplot as plt
import sklearn.linear_model as slm
from preparation import data_1, data_2

print("I przed, I po")
x_axis = np.array([data_1.PRZED_1]).reshape(-1, 1)
y_axis = np.array(data_1.PO_1.tolist())


regresja = slm.LinearRegression()

regresja.fit(x_axis, y_axis)

regresja = slm.LinearRegression()

regresja.fit(x_axis, y_axis)
print('Wyraz wolny jest równy: %s' % np.round(regresja.intercept_, 3))
print('Współczynnik kierunkowy wynosi: %s' % np.round(regresja.coef_, 3))
print('Współczynnik dopasowania wynosi: %s' % np.round(regresja.score(x_axis, y_axis),3))

P = np.array([0.692*x - 10.121 for x in np.linspace(1, 150, 100)])

plt.figure(1)
plt.scatter(x_axis, y_axis, c='r', s=1.5)
plt.plot(np.linspace(1, 150, 100), P)
plt.xlabel('I przed')
plt.ylabel('I po')
plt.title('Współczynnik dopasowania wynosi: 0.441')


print("II przed, II po")
x_axis = np.array([data_2.PRZED_2]).reshape(-1, 1)
y_axis = np.array(data_2.PO_2.tolist())


regresja = slm.LinearRegression()

regresja.fit(x_axis, y_axis)

regresja = slm.LinearRegression()

regresja.fit(x_axis, y_axis)
print('Wyraz wolny jest równy: %s' % np.round(regresja.intercept_, 3))
print('Współczynnik kierunkowy wynosi: %s' % np.round(regresja.coef_, 3))
print('Współczynnik dopasowania wynosi: %s' % np.round(regresja.score(x_axis, y_axis),3))

P = np.array([0.679*x + 5.419 for x in np.linspace(1, 150, 100)])

plt.figure(2)
plt.scatter(x_axis, y_axis, c='r', s=1.5)
plt.plot(np.linspace(1, 150, 100), P)
plt.xlabel('II przed')
plt.ylabel('II po')
plt.title('Współczynnik dopasowania wynosi: 0.586')
plt.show()
