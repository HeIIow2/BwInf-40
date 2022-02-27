import threading
import rechenratsel
import random
import time

import matplotlib.pyplot as plt
import numpy as np


# test für die fertige aufgabe
def therm_len_test():
    total_tests = 3000
    failed = 0
    passed = 0

    values = [2] * total_tests
    STEPS = 1
    length = list(range(1, total_tests * STEPS + 1, STEPS))

    durations = []

    for i in range(total_tests):
        start_time = time.time()
        therm_str, therm = rechenratsel.get_therm(length[i], values[i])
        finish_time = time.time()

        operators = 0
        for multiplication_package in therm:
            for addition_package in multiplication_package:
                for division_package in addition_package:
                    if division_package > 9 or division_package < -9:
                        print(f"value is too big/small {division_package}")
                        print(therm_str)
                        failed += 1

                    operators += 1

        if operators != length[i]:
            print(f"length: {operators}, {length[i]}")
            print(therm_str)
            failed += 1

        difference = finish_time - start_time
        if difference == 0.0:
            difference = 0.000000001
        durations.append(difference)

        if eval(therm_str) == values[i]:
            passed += 1
        else:
            failed += 1
            print("value")
            print(therm_str)

    print(f"{failed} out of {total_tests} failed")

    y = np.array(durations)
    x = np.array(length)

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    plt.title("Rechenrätsel")
    plt.xlabel('number of operators')
    plt.ylabel('time')

    plt.plot(x, y, linewidth=0.5)
    plt.plot(x, p(x), "r--")
    plt.show()


def test_value():
    total_tests = 100000
    failed = 0
    passed = 0

    STEPS = 3
    values = list(range(1, total_tests * STEPS + 1, STEPS))
    length = [100] * total_tests

    durations = []

    for i in range(total_tests):
        start_time = time.time()
        therm_str, therm = rechenratsel.get_therm(length[i], values[i])
        finish_time = time.time()

        try:
            operators = 0
            for multiplication_package in therm:
                for addition_package in multiplication_package:
                    for division_package in addition_package:
                        if division_package > 9 or division_package < -9:
                            print(f"value is too big/small {division_package}")
                            print(therm_str)
                            failed += 1

                        operators += 1

            if operators != length[i]:
                print(f"length: {operators}, {length[i]}")
                print(therm_str)
                failed += 1
            gotten = int(eval(therm_str))
            if gotten == values[i]:
                passed += 1
            else:
                failed += 1
                print(f"value: {values[i]}; {gotten}")
                print(therm_str)

        except TypeError:
            print(therm_str)

        difference = finish_time - start_time
        if difference == 0.0:
            difference = 0.000000001
        durations.append(difference)

    print(f"{failed} out of {total_tests} failed")

    y = np.array(durations)
    x = np.array(values)

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    plt.title("Rechenrätsel")
    plt.xlabel('value of the result')
    plt.ylabel('time')

    plt.plot(x, y, linewidth=0.5)
    plt.plot(x, p(x), "r--")
    plt.show()


def test_uniqnes():
    LENGTH = 10
    while True:
        RESULT = random.randint(1, 100)
        therm_str, therm = rechenratsel.get_therm(LENGTH + 1, RESULT, addition_char=" o ", division_char=" o ",
                                                  multiplication_char=" o ")
        print(therm_str)

        def generate_list():
            nonlocal LENGTH
            nonlocal correct_results
            nonlocal operands

            OPERATORS = [
                " + ",
                " * ",
                " / "
            ]

            possibilities = [
                [0] * LENGTH
            ]

            for i in range(3 ** LENGTH - 1):
                last_list = list(possibilities[-1])

                for i, elem in enumerate(reversed(last_list)):
                    i = len(last_list) - i - 1
                    if elem > 1:
                        last_list[i] = 0
                    else:
                        last_list[i] += 1
                        break

                last_index = len(possibilities) - 1
                for i, elem in enumerate(possibilities[last_index]):
                    possibilities[last_index][i] = OPERATORS[possibilities[last_index][i]]

                possibilities.append(last_list)

                tryout_list = possibilities[last_index]

                therm_str_ = operands[0]
                for i, operator in enumerate(tryout_list):
                    if str(operator) == " / " and operands[i + 1] == "0":
                        break

                    therm_str_ += str(operator)
                    therm_str_ += operands[i + 1]

                if int(eval(therm_str_)) == RESULT:
                    correct_results += 1
                    print(therm_str_)
                    if correct_results > 1:
                        return False

            if correct_results == 1:
                return True
            print("The fuck?", correct_results)
            return False

        correct_results = 0
        operands = therm_str.split(" o ")
        passed = generate_list()

        if passed:
            break


def main_test():
    test_uniqnes()


if __name__ == '__main__':
    # den stack erhöhen, da mein Programm ein zu langen therm generiert
    threading.stack_size(200000000)
    thread = threading.Thread(target=main_test)
    thread.start()
