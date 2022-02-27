import rechenrätsel_multiprocessing

import time

test_cases = list(range(14))

def test():
    times = []

    for test_case in test_cases:
        start_time = time.time()
        result, exercise = rechenrätsel_multiprocessing.get_therm(test_case)
        end_time = time.time()

        therm, res = result.split(" = ")
        if int(eval(therm)) != int(res):
            print(f"failed {result} {exercise}")

        with open("examples.txt", "a", encoding="utf-8") as examples_file:
            examples_file.write(f"{test_case}: {exercise} | {result}; {end_time-start_time}\n")

        times.append(str(end_time-start_time))
        print(f"test case {test_case} completed in {end_time-start_time}")

    with open("times.csv", "a") as times_file:
        times_file.write(", ".join(times) + "\n")


if __name__ == '__main__':
    for k in range(3):
        test()
