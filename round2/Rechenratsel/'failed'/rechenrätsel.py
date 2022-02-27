import random

def generate_therm(n: int, minimum=0, maximum=9):
    if n==0:
        return "No."
    if n==1:
        random_number = random.randint(minimum, maximum)
        return f"{random.randint(minimum, maximum)} = {random.randint(minimum, maximum)}"

    def stringifie_therm(operands_: list, operators_: list):
        therm_string = str(operands_[0])
        for i, operator_ in enumerate(operators_):
            print(operator_)
            therm_string += OPERATORS[operator_]
            therm_string += str(operands_[i])
        try:
            result_ = int(eval(therm_string))
        except ZeroDivisionError:
            result_ = None

        return f"{therm_string} = {result_}"

    OPERATORS = [" + ", " - ", " * ", " / "]
    operators = []

    subtotal = 0
    total_divisions = 0

    operands = [int(random.randint(minimum+1, maximum))]

    options = []
    results = [[[operands[-1], None]]]

    print(operands)
    i = 0
    while i < n:
        if len(options) <= len(operators):
            latest_number = operands[-1]
            possible_operators = [0, 1, 2]

            to_append = {}
            for possible_operator in possible_operators:
                if possible_operator == 3:
                    to_append_append = [latest_number]
                    if latest_number*2 < maximum:
                        to_append_append.append(latest_number*2)
                    to_append[possible_operator] = to_append_append

                else:
                    to_append[possible_operator] = list(range(minimum, maximum+1))

            options.append(to_append)

        possible_options = options[-1]
        new_operator = list(possible_options)[random.randrange(len(list(possible_options)))]
        new_operand_ind = random.randrange(len(possible_options[new_operator]))
        new_operand = possible_options[new_operator][new_operand_ind]

        print(results)

        options[-1][new_operator].pop(new_operand_ind)
        if len(options[-1][new_operator]) == 0:
            options[-1].pop(new_operator)

        operands.append(new_operand)
        operators.append(new_operator)
        # print(operators)

        def get_real_therm(operands_, operators_):
            therm_string = str(operands_[0])
            for i, operator_ in enumerate(operators_):
                therm_string += OPERATORS[operator_]
                therm_string += str(operands_[i])

            try:
                result_ = int(eval(therm_string))
            except ZeroDivisionError:
                result_ = None

            return result_

        def check_for_other_solutions(current_length: int, result: int, operators):
            nonlocal operands

            correct_results = 0

            possibilities = [
                [0] * current_length
            ]

            for i in range(4 ** current_length - 1):
                last_list = list(possibilities[-1])

                for i, elem in enumerate(reversed(last_list)):
                    i = len(last_list) - i - 1
                    if elem > 2:
                        last_list[i] = 0
                    else:
                        last_list[i] += 1
                        break

                possible_result = get_real_therm(operands, last_list)
                if possible_result == result:
                    correct_results += 1
                    if correct_results > 1:
                        return correct_results

                possibilities.append(last_list)

            if correct_results==0:
                pass

            return correct_results

        solutions = check_for_other_solutions(i+1, get_real_therm(operands, operators), operators)

        if solutions != 1:
            operands.pop(-1)
            operators.pop(-1)

            if len(options[-1]) == 0:
                operands.pop(-1)
                operators.pop(-1)
                options.pop(-1)
                print(i)
                print(f"operators: {operators}")
                print(f"operands: {operands}")
                print()
                i += -1
            continue
        print(i)
        print(f"operators: {operators}")
        print(f"operands: {operands}")
        print()
        i += 1

    print(stringifie_therm(operands, operators))


generate_therm(5)