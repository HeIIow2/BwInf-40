import random


def maybe_get_therm(n, minimum=0, maximum=9):
    OPERATORS = [" + ", " - ", " * ", " / "]

    operands = []

    unused_operators = []

    def refresh_unused_operators():
        nonlocal unused_operators
        unused_operators = list(range(minimum, maximum + 1))
        # unused_operators.extend(list(range(4, maximum+1)))
        random.shuffle(unused_operators)
        for i, unused_operator in enumerate(unused_operators):
            if random.randint(0, 1) == 0:
                index_difference = random.randint(1, 2)
                if i - index_difference >= 0:
                    if i - index_difference > unused_operator:
                        unused_operators[i] = unused_operators[i - index_difference]
                        unused_operators[i - index_difference] = unused_operator

    refresh_unused_operators()

    new_operand = None
    for i in range(n + 1):
        if len(operands) != 0:
            last_operand = operands[-1]
            for i, unused_operand in enumerate(unused_operators):
                if unused_operand != 0 and unused_operand != 1:
                    if last_operand % unused_operand == 0:
                        new_operand = unused_operand
                        unused_operators.pop(i)
                        break

        if new_operand is None:
            new_operand = unused_operators[0]
            unused_operators.pop(0)

        if len(unused_operators) == 0:
            refresh_unused_operators()

        operands.append(new_operand)
        new_operand = None

    # bekommt eine Liste aller Kombinationen aller Operatoren
    def get_real_therm(operands_, operators_):
        therm_string = str(operands_[0])

        multiplication_sub = 1
        for i, operator_ in enumerate(operators_):
            if operator_ == 2:
                multiplication_sub = multiplication_sub * operands_[i]
            elif operator_ == 3:
                if operands_[i + 1] == 0 or multiplication_sub * operands_[i] / operands_[i + 1] % 1 != 0:
                    return ""
            elif operator_ == 0 or operator_ == 1:
                multiplication_sub = 1
            therm_string += OPERATORS[operator_]
            therm_string += str(operands_[i + 1])
        return therm_string

    result_frequencies = {

    }

    last_list = [0] * n
    last_list[-1] = -1
    for i in range((4 ** n)):
        for i, elem in enumerate(reversed(last_list)):
            i = len(last_list) - i - 1
            if elem > 2:
                last_list[i] = 0
            else:
                last_list[i] += 1
                break

        therm = get_real_therm(operands, last_list)
        if therm != "":
            result = eval(therm)
            if result <= 0:
                continue
            if result % 1 != 0:
                continue

            if result in result_frequencies:
                result_frequencies[result]['freq'] += 1
            else:
                result_frequencies[result] = {'freq': 1, 'therm': therm, 'result': int(result)}

    final_results = []

    for result_frequency in result_frequencies:
        if result_frequencies[result_frequency]['freq'] == 1:
            final_results.append({
                'therm': result_frequencies[result_frequency]['therm'],
                'result': result_frequency
            })

    return final_results


def get_therm(n: int, minimum=0, maximum=9):
    results = []
    while not len(results):
        results = maybe_get_therm(n, minimum=minimum, maximum=maximum)

    def negative_operators(result_: dict):
        therm_str = result_['therm']
        if not therm_str.count('/'):
            return 0
        return therm_str.count('-') + therm_str.count('/')

    best_result = {}
    best_diversity = 0
    for result in results:
        diversity = negative_operators(result)
        if diversity > best_diversity:
            best_diversity = diversity
            best_result = result

    if best_diversity == 0 and n>3:
        return get_therm(n, minimum=minimum, maximum=maximum)

    print(f"best operator diversity: {best_diversity}")

    result = best_result['result']
    therm = best_result['therm']

    def mix_therm(therm_: str):
        therm_list = therm.split(" + ")
        random.shuffle(therm_list)
        return " + ".join(therm_list)

    finished_therm = mix_therm(therm)

    return f"{finished_therm} = {int(result)}"


if __name__ == '__main__':
    print(get_therm(8))
