import json
import numpy as np
import matplotlib.pyplot as plt

# read laufzeit.json and store lists in according variables

with open('laufzeit.json') as f:
    data = json.load(f)
    x_axis = data['x_axis']
    y_axis = data['y_axis']
    std = data['std']

factors = []
for n, y_value in zip(x_axis, y_axis):
    factors.append(y_value / (n * n))
factor = np.average(factors)

print("Average factor:", factor)

plt.plot(x_axis, y_axis, "-o", linewidth=1, label="data")

plt.errorbar(x_axis, y_axis, yerr=std, linestyle='None', markersize=0,
             label=f"Standart Deviation\navr: {round(np.average(std), 3)}")



def func(n):
    return n * n * factor

x_ = []
for i in range(0, x_axis[-1]):
    x_.append(i)
x_ = np.array(x_)
plt.plot(x_, func(x_), label="Fitted Curve")

plt.grid(visible=True, which='major', axis='both')

plt.title(f"Hex Max | t(n) = {round(factor, 8)} * n^2")
plt.xlabel("n (length of the hex number)")
plt.ylabel('time in seconds')
plt.legend(loc='upper left')
plt.savefig("Laufzeit.svg")
plt.savefig("Laufzeit.png")
plt.show()