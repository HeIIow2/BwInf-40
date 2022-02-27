import rechenrätsel_multiprocessing

import time

import matplotlib.pyplot as plt
import numpy as np

test_cases = list(range(0, 14))

def test():
    times = []

    for test_case in test_cases:
        start_time = time.time()
        test_result = rechenrätsel_multiprocessing.get_therm(test_case)
        print(test_result)
        end_time = time.time()

        times.append(str(end_time-start_time))
        print(f"test case {test_case} completed in {end_time-start_time}")

    with open("times.csv", "a") as times_file:
        times_file.write(", ".join(times) + "\n")


if __name__ == '__main__':
    test()
