import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

with open("times.csv", "r") as time_file:
    times = time_file.read().split(", ")
    for i in range(len(times)):
        times[i] = float(times[i])
        if times[i] == 0.0:
            times[i] = 0.0000001

    y = np.array(times[1:])
    x = np.arange(1, len(times))

    x_ = []
    for i in range(len(x)* 100):
        x_.append(i/100)
    x_ = np.array(x_)


    def func(x, a, b, c):
        # c = 0
        return a * np.exp(b * x) + c
    popt, pcov = curve_fit(func, x, y)

    plt.plot(x, y, "o", linewidth=1, label="data")
    plt.plot(x_, func(x_, *popt), label="Fitted Curve")

    plt.title("Rechenrätsel")
    plt.xlabel('operators in therm')
    plt.ylabel('time in s')
    plt.legend(loc='upper left')
    plt.show()
