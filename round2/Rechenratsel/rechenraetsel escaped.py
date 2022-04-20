from multiprocessing import Pool, freeze_support
import random


def generate_operands(n, minimum=0, maximum=9):
    """
    generiert eine Liste von Operanden der Laenge n

    :param n: die Anzahl an Operatoren
    :param minimum: der kleinst moegliche Operand
    :param maximum: der groesstmoegliche Operand
    :return: liste von Operanden der Laenge n
    """
    # liste aller Operanden
    operands = []
    # queue fuer die Operanden, da 'echter' Zufall langweilig ist
    unused_operands = []

    # auffuellen der queue
    def refresh_unused_operands():
        nonlocal unused_operands
        unused_operands = list(range(minimum, maximum + 1))
        random.shuffle(unused_operands)
        for i, unused_operator in enumerate(unused_operands):
            if random.randint(0, 1) == 0:
                index_difference = random.randint(1, 2)
                if i - index_difference >= 0:
                    if i - index_difference > unused_operator:
                        unused_operands[i] = unused_operands[i - index_difference]
                        unused_operands[i - index_difference] = unused_operator

    refresh_unused_operands()

    # generiere liste von Operanden mit der queue
    new_operand = None
    for i in range(n + 1):
        if len(operands) != 0:
            last_operand = operands[-1]
            # wenn der letzte Operand durch einen der noch in der queue ist teilbar ist, nehme diesen
            for i, unused_operand in enumerate(unused_operands):
                if unused_operand != 0 and unused_operand != 1:
                    if last_operand % unused_operand == 0:
                        new_operand = unused_operand
                        unused_operands.pop(i)
                        break

        if new_operand is None:
            new_operand = unused_operands[0]
            unused_operands.pop(0)

        if len(unused_operands) == 0:
            refresh_unused_operands()

        operands.append(new_operand)
        new_operand = None

    return operands


def maybe_get_therm(n, operands, minimum=0, maximum=9):
    """
        generiert eine Liste von Operanden
        sucht alle eindeutigen Therme
        gibt alle eindeutigen Therme zurueck

        :param n: die Anzahl an Operatoren
        :param operands: optional zu n einfach die Operanden
        :param minimum: der kleinst moegliche Operand
        :param maximum: der groesstmoegliche Operand
        :return: liste potenzieller Loesungen
    """

    OPERATORS = [" + ", " - ", " * ", " / "]

    # generiere ein liste von operanden oder nimmt die uebergebene
    if operands is None:
        operands = generate_operands(n=n, minimum=minimum, maximum=maximum)

    result_frequencies = compute_combinations(part=0, n=n, operands=operands, threads=1)

    unique_therms = []
    for key in result_frequencies:
        if result_frequencies[key]["freq"] == 1:
            unique_therms.append({
                'therm': result_frequencies[key]['therm'],
                'result': result_frequencies[key]['result']
            })

    return unique_therms


def compute_combinations(part, n, operands, threads=4):
    OPERATORS = [
        " + ",
        " - ",
        " * ",
        " / "
    ]

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
    last_list[0] = part
    last_list[-1] = -1

    for i in range(int((4 ** n) / threads)):
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

    return result_frequencies


def maybe_get_therm_multiprocessing(n, operands, minimum=0, maximum=9):
    """
    generiert eine Liste von Operanden
    started threads, die jeweils ein Teil aller Loesungen eindeutigen Therme
    schaut wenn alle threads fertig sind ob die Loesungen wirklich eindeutig sind,
    gibt alle eindeutigen Therme zurueck

    :param n: die Anzahl an Operatoren
    :param operands: optional zu n einfach die Operanden
    :param minimum: der kleinst moegliche Operand
    :param maximum: der groesstmoegliche Operand
    :return: liste potenzieller Loesungen
    """

    # generiere ein liste von operanden oder nimmt die uebergebene
    if operands is None:
        operands = generate_operands(n=n, minimum=minimum, maximum=maximum)

    with Pool() as pool:
        result = pool.starmap(compute_combinations,
                              [(0, n, operands), (1, n, operands), (2, n, operands), (3, n, operands)])
        print("multiprocessing done")

        unique_therms = []

        for i in range(len(result)):
            for key in result[i]:
                is_unique = True
                for j in range(len(result)):
                    if j == i:
                        continue
                    if key in result[j]:
                        is_unique = False
                        result[j].pop(key)
                if is_unique:
                    unique_therms.append({
                        'therm': result[i][key]['therm'],
                        'result': key
                    })

        return unique_therms


def get_therm(n: int, operands: list=None, minimum=0, maximum=9):
    """
    https://bwinf.de/fileadmin/bundeswettbewerb/40/aufgaben402.pdf
    Diese Funktion loest die Aufgabe Rechenraetsel

    :param n: die Anzahl an Operatoren
    :param operands: optional zu n einfach die Operanden
    :param minimum: der kleinst moegliche Operand
    :param maximum: der groesstmoegliche Operand
    :return: tuple (Loesung, Aufgabe)
    """

    # edge cases
    if n < 0:
        return "No.", "still No."
    if n == 0:
        random_number = random.randint(minimum + 1, maximum)
        return f"{random_number} = {random_number}", f"{random_number} = {random_number}"

    mixing_afterwards = True
    if operands is not None:
        mixing_afterwards = False

    """
    fuellt die Liste mit moeglichen Ergebnissen auf.
    nutzt ab n < 8 Parallelisierung, da vorher thread pulling 
    laenger als die eigentliche Aufgabe braucht.
    """
    results = []
    while not len(results):
        if n < 8:
            results = maybe_get_therm(n, operands, minimum=minimum, maximum=maximum)
        else:
            results = maybe_get_therm_multiprocessing(n, operands, minimum=minimum, maximum=maximum)
        operands = None

    """
    da negative operatoren (-, /) vergleichsweise selten sind suche die Loesung
    mit der hoechsten Anzahl von diesen heraus
    """

    def negative_operators(result_: dict):
        therm_str = result_['therm']
        if not therm_str.count('/'):
            return 0
        return therm_str.count('-') + therm_str.count('/')

    best_result = results[random.randrange(len(results))]
    best_diversity = 0
    for result in results:
        diversity = negative_operators(result)
        if diversity > best_diversity:
            best_diversity = diversity
            best_result = result

    if best_diversity == 0 and n > 3:
        # wenn es mehr als 3 Operatoren gibt muss mindestens ein negativer Operator
        # enthalten sein
        return get_therm(n, minimum=minimum, maximum=maximum)

    print(f"best operator diversity: {best_diversity}")

    result = best_result['result']
    therm = best_result['therm']

    # mische den Therm noch einmal
    def mix_therm():
        therm_list = therm.split(" + ")
        random.shuffle(therm_list)
        return " + ".join(therm_list)

    # entferne die operatoren
    def censor_therm(therm_: str):
        return therm_.replace(" + ", u" ◦ ").replace(" - ", u" ◦ ").replace(" * ", u" ◦ ").replace(" / ", u" ◦ ")

    if mixing_afterwards:
        finished_therm = mix_therm()
    else:
        finished_therm = therm

    return f"{finished_therm} = {int(result)}", f"{censor_therm(finished_therm)} = {int(result)}"


if __name__ == "__main__":
    freeze_support()
    while True:
        input_ = input("\ntype 'n: <n>' to specify n else just type the desired operands seperated by space: ")
        if input_ == "exit":
            break

        if "n:" in input_:
            n = int(input_.split(":")[1])
            operands = None
        else:
            try:
                operands = [int(x) for x in input_.split(" ")]
                n = len(operands) - 1
            except ValueError:
                print("invalid input")
                continue

        print("computing...")
        print(get_therm(n, operands=operands))
