import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

with open("times.csv", "r") as time_file:
    time_lines = time_file.read().split("\n")

    ys = []

    for n, time_line in enumerate(time_lines):
        if n == 0 or time_line == "":
            continue

        times = time_line.split(", ")
        for i in range(len(times)):
            if i == 0:
                continue

            i = i-1

            times[i] = float(times[i])
            if times[i] == 0.0:
                times[i] = 0.0000000001

            if i >= len(ys):
                ys.append([])
            ys[i].append(times[i])

    y = []
    std = []
    for i in ys:
        y.append(np.average(i))
        std.append(np.std(i))

    x = np.arange(1, len(times))

    x_ = []
    for i in range(len(x)* 100):
        x_.append(i/100)
    x_ = np.array(x_)


    def func(x, a, b, c):
        c = 0
        return a * np.exp(b * x) + c
        
    popt, pcov = curve_fit(func, x, y)
    
    total_time = 0
    for i in range(1, 16):
        new_time = func(i, *popt)
        print(f"{i} elements take {new_time} seconds.")
        total_time += new_time
        
    print(total_time)
    
    deviations = []
    for i, time in enumerate(y):
        deviations.append(func(x[i], *popt) - time)
        
    print(deviations)
    deviations = np.array(deviations)
    avr = np.average(abs(deviations))

    SCALE_FACTOR = 1
    standart_deviation = deviations / avr * SCALE_FACTOR

    plt.plot(x, y, "o", linewidth=1, label="data")
    plt.plot(x_, func(x_, *popt), label="Fitted Curve")
    plt.errorbar(x, y, yerr=std, linestyle='None', markersize=0, label=f"Standart Deviation\navr: {round(np.average(std) ,3)}")

    plt.xticks(range(0, max(x)+1))
    
    plt.annotate("start\nparallel", # this is the text
                 (8,func(8, *popt)), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center')
                 
    #plt.yscale("symlog")

    plt.title(f"Rechenrätsel")
    plt.xlabel('operators in therm')
    plt.ylabel('time in s')
    plt.legend(loc='upper left')
    plt.show()
