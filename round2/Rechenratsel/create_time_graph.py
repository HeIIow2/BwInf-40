import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

START_AT = 8
CALCULATE_FROM = 0
CALCULATE_TO = 15

with open("times.csv", "r") as time_file:
    tests = time_file.read().split("\n")

    values = []

    for n, time_line in enumerate(tests):
        if n == 0 or time_line == "":
            continue

        times = time_line.split(", ")
        times = times[START_AT:]
        for i in range(len(times)):
            times[i] = float(times[i])
            # if times[i] == 0.0:
            #     times[i] = 0.0000000001

            if i >= len(values):
                values.append([])
            values[i].append(times[i])

y_parallel = []
std = []
for i in values:
    y_parallel.append(np.average(i))
    std.append(np.std(i))

x_parallel = np.arange(START_AT, len(times) + START_AT)
y_parallel = np.array(y_parallel)


factors = []
for i in range(len(y_parallel)):
    if i == 0:
        continue
    factors.append(4 ** x_parallel[i] / y_parallel[i])
FACTOR = 1 / np.average(factors)
print(f"{round(FACTOR, 8)} * 4^n")

x_ = []
for i in range((len(x_parallel) - 1) * 100):
    x_.append(START_AT + i / 100)
x_ = np.array(x_)

def func(x):
    return FACTOR * 4 ** x


total_time = 0
for i in range(CALCULATE_FROM, CALCULATE_TO+1):
    new_time = func(i)
    total_time += new_time
print(f"it takes {round(int(total_time) / 60, 2)} minutes to generate therms from {CALCULATE_FROM} to {CALCULATE_TO}")


plt.plot(x_parallel, y_parallel, "o", linewidth=1, label="data")
plt.plot(x_, func(x_), label="Fitted Curve")
plt.errorbar(x_parallel, y_parallel, yerr=std, linestyle='None', markersize=0,
             label=f"Standart Deviation\navr: {round(np.average(std), 3)}")

plt.xticks(range(START_AT, max(x_parallel) + 1))
plt.grid(visible=True, which='major', axis='both')

plt.annotate("start\nparallel",  # this is the text
             (8, func(8)),  # these are the coordinates to position the label
             textcoords="offset points",  # how to position the text
             xytext=(0, 10),  # distance from text to points (x,y)
             ha='center')

plt.title(f"Rechenrätsel")
plt.xlabel('operators in therm')
plt.ylabel('time in s')
plt.legend(loc='upper left')
plt.savefig("Laufzeit.svg")
plt.savefig("Laufzeit.png")
plt.show()
