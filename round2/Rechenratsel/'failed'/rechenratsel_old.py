"""
Ansatz:
x = x * (1)
x = x * (9 - 16 / 2)
x = x * 9 - x * 16 / (x / 2)
x = 2x * 18 - 0.5x * 8 / (2x / 4)
"""
import random
import math


def get_therm(_n: int, _result: int, addition_char=" + ", multiplication_char=" * ", division_char=" / ", maximum=9, debug=False):
    if _n == 0:
        return "No.", [[["No."]]]
    if _n == 1:
        return str(_result), [[[_result]]]

    def get_closest_number_with_many_primes(n: int):
        """
        Bekommt die nächstgelegene zahl zu n, die
        nur einstellige Primfaktoren hat.
        """

        def get_primes(n_):
            primes_ = []
            d = 2
            while d * d <= n_:
                while (n_ % d) == 0:
                    primes_.append(d)
                    n_ //= d
                d += 1
            if n_ > 1:
                primes_.append(n_)
            return primes_

        def are_small_numbers(primes_: list):
            if len(primes_) == 0:
                return False
            for prime_ in primes_:
                if prime_ > 9:
                    return False

            return True

        found_anything = False
        deviation = 0
        while not found_anything:
            primes = get_primes(n - deviation)
            found_anything = are_small_numbers(primes)
            if found_anything:
                return primes, -deviation

            primes = get_primes(n + deviation)
            found_anything = are_small_numbers(primes)
            if found_anything:
                return primes, deviation

            deviation += 1

    def therm_resulting_one(n: int, maximum=9, debug=False):
        if n == 1:
            return [[1]]

        # teilt den Therm in verschiedene Additionen/Substraktionen auf
        addition_indices = []

        n += 1

        for i in range(1, n - 1):
            # Wahrscheinlichkeit auf eine addition
            if random.randint(0, 3) != 0:
                addition_indices.append(i)

        if len(addition_indices) == 0:
            addition_indices.append(n - 2)

        if addition_indices[-1] != n - 2:
            addition_indices.append(n - 2)

        sub_therm_ranges = []

        # bekommt den Umfang der Unterrechnungen
        last_i = 0
        for i in addition_indices:
            sub_therm_ranges.append([last_i, i])
            last_i = i
        sub_therm_ranges.append([i, n - 1])

        # bekomme die Anzahl aller Zahlen in dem Therm
        sub_therm_sizes = []
        for range_ in sub_therm_ranges:
            sub_therm_sizes.append(range_[1] - range_[0])

        def get_addition_therm_resulting_to(n_: int, sub_therm_sizes_: list, resulting: int):
            # bekommt eine liste von positiven und negativen zahlen, die zusammengerechnet "resulting" ergeben
            if n_ == 1:
                return [resulting]

            nonlocal maximum
            temp_operands = []

            def get_avr(sub_therm_sizes__: list, value: int):
                operator_count = 0
                for sub_therm_size__ in sub_therm_sizes__:
                    if sub_therm_size__ == 1:
                        operator_count += 1
                    else:
                        value -= 1
                if operator_count == 0:
                    print(sub_therm_sizes_)
                return value / operator_count

            adds_up_to = 0
            for i in range(n_ - 1):
                if sub_therm_sizes_[i] != 1:
                    adds_up_to += 1
                    temp_operands.append(1)
                    continue

                avr = get_avr(sub_therm_sizes_[i:], resulting - adds_up_to)
                if avr > 0:
                    max_val = 9
                    min_val = int(avr - (9 - avr))
                else:
                    min_val = -9
                    max_val = int(avr - (-9 - avr))

                number = random.randint(min_val, max_val)
                adds_up_to += number
                temp_operands.append(number)

            temp_operands.append(resulting - adds_up_to)

            return temp_operands

        def get_division_therm_resulting_to(n_: int, resulting: int):
            # bekommt eine liste von zahlen, die dividiert "resulting" ergeben
            if n_ == 1:
                return [resulting]

            nonlocal maximum
            # es ist effizienter die Primfaktoren bin 9 in einer liste zu speichern als sie zu berechnen
            prime_factors = [
                [4, 2, 2],
                [6, 2, 3],
                [8, 2, 2, 2],
                [9, 3, 3]
            ]

            prime_factor = prime_factors[random.randrange(len(prime_factors))]

            def randomize_prime_factors(to_randomize: list):
                insert_later = to_randomize[0]
                to_randomize = to_randomize[1:]

                random.shuffle(to_randomize)
                to_randomize.insert(0, insert_later)

                return to_randomize

            if len(prime_factor) < n_:
                for i in range(n_ - len(prime_factor)):
                    prime_factor.append(1)
                return randomize_prime_factors(prime_factor)

            if len(prime_factor) == n_:
                return randomize_prime_factors(prime_factor)

            prime_factor_part = prime_factor[1:]

            merged_prime = [1] * (n_ - 1)
            for prime in prime_factor_part:
                multiply_ind = random.randrange(len(merged_prime))
                merged_prime[multiply_ind] = merged_prime[multiply_ind] * prime

            merged_prime.insert(0, prime_factor[0])

            return randomize_prime_factors(merged_prime)

        sub_therm_values = get_addition_therm_resulting_to(len(sub_therm_sizes), sub_therm_sizes, 1)

        equation = []
        for i, sub_therm_size in enumerate(sub_therm_sizes):
            # print("temp operants")
            equation.append(get_division_therm_resulting_to(sub_therm_size, sub_therm_values[i]))
            # print(equation[-1])

        if debug:
            def sub_equation_to_str(sub_equation: list):
                # dieser Code ist ekelhaft aber funktioniert. wenigstens ist er nicht permanent
                addition_str = []
                for addition in sub_equation:
                    addition_str_ = []
                    for elem in addition:
                        addition_str_.append(str(elem))
                    addition_str.append(" / ".join(addition_str_))

                equation_str = " + ".join(addition_str)

                return equation_str

            print(f"sub therm values: {sub_therm_values}")
            print(f"addition indices: {addition_indices}")
            print(f"sub therm ranges: {sub_therm_ranges}")
            print(f"sub therm sizes: {sub_therm_sizes}")
            print(f"equation: {equation}")
            print(f"stringified equation: {sub_equation_to_str(equation)}")
            print()

        return equation

    def therm_times_factors(simple_term_: list, factors: list, maximum=9, debug=False):
        # multipliziere den Therm ohne ihn zu vereinfachen
        boring_therm = []
        for therm_part in simple_term_:
            temp_element = []
            for factor in factors:
                temp_element.append([factor])
            temp_element.append(therm_part)
            boring_therm.append(temp_element)

        # vereinfache den Therm (multipliziere alle faktoren die multipliziert keine mehrstellige Zahl ergeben miteinander)
        return reduce_therm(boring_therm)

    def reduce_therm(multiplication_therm: list, maximum=9, debug=False):
        therm = []
        if debug:
            print("multiplication packages:")
        for multiplication_package in multiplication_therm:
            if debug:
                print(multiplication_package)
            found_something = True
            while found_something:
                found_something = False
                for i, fac_1 in enumerate(multiplication_package):
                    fac_1 = fac_1[0]
                    for j, fac_2 in enumerate(multiplication_package):
                        fac_2 = fac_2[0]
                        if i == j:
                            continue
                        if abs(fac_1) * abs(fac_2) <= maximum:
                            found_something = True
                            break
                    if found_something:
                        break

                if found_something:
                    if len(multiplication_package[j]) != 1:
                        multiplication_package[j][0] = multiplication_package[j][0] * multiplication_package[i][0]
                        multiplication_package.pop(i)
                    else:
                        multiplication_package[i][0] = multiplication_package[i][0] * multiplication_package[j][0]
                        multiplication_package.pop(j)

            if debug:
                print(multiplication_package)
                print()

            random.shuffle(multiplication_package)
            therm.append(multiplication_package)

        if debug:
            print(f"ausmultiplizierter therm: {therm}")

        return therm

    def get_operator_frequencies(therm: list):
        operator_frequencies = {}
        for multiplication_package in therm:
            for addition_package in multiplication_package:
                for division_package in addition_package:
                    division_package = abs(int(division_package))
                    if division_package in operator_frequencies:
                        operator_frequencies[division_package] += 1
                    else:
                        operator_frequencies[division_package] = 1

        return operator_frequencies

    def get_addition_therm_resulting_to_(n_: int, resulting: int, debug=False):
        # bekommt eine liste von positiven und negativen zahlen, die zusammengerechnet "resulting" ergeben
        if n_ == 1:
            return [[[resulting]]]

        nonlocal maximum
        temp_operands = []

        def get_avr(operator_count: int, value: int):
            return value / operator_count

        adds_up_to = 0
        for i in range(n_ - 1):
            avr = get_avr(n_ - i, resulting - adds_up_to)
            if avr > 9 or avr < -9:
                return None
            if avr > 0:
                max_val = 9
                min_val = int(avr - (9 - avr))
            else:
                min_val = -9
                max_val = int(avr - (-9 - avr))

            number = random.randint(min_val, max_val)
            adds_up_to += number
            temp_operands.append([[number]])

        temp_operands.append([[resulting - adds_up_to]])

        return temp_operands

    def therm_to_str(therm_: list):
        nonlocal multiplication_char
        nonlocal division_char
        nonlocal addition_char

        therm_ = list(therm_)

        multiplication_strings = []
        for multiplication_package in therm_:
            addition_strings = []
            for addition_package in multiplication_package:
                addition_package_ = []
                for elem in addition_package:
                    addition_package_.append(str(elem))
                addition_strings.append(division_char.join(addition_package_))

            multiplication_strings.append(multiplication_char.join(addition_strings))

        return addition_char.join(multiplication_strings)

    def get_operators(therm_: list):
        operators = 0
        for multiplication_package in therm_:
            for addition_package in multiplication_package:
                for division_package in addition_package:
                    operators += 1
        return operators

    # ändere das Ergebnis, bis es eine Zahl mit vielen Primfaktoren gibt, und füge diese änderung Später wieder hinzu
    initial_result = _result
    _primes, deviation = get_closest_number_with_many_primes(_result)
    _result = _result - deviation

    if debug:
        print(f"gewünschte länge: {_n}")
        print(f"endgültiges Ergebnis: {initial_result}")
        print(f"temporäres Ergebnis: {_result}; abweichung: {deviation}")
        print(f"primfaktoren {_primes}")
        print()

    missing_operators = -1
    i = 0
    while missing_operators <= 0:
        # bekomme den auszuklammernden Therm
        new_core_length = math.ceil(_n / (len(_primes))) - i
        if new_core_length <= 0:
            simple_therm = [[]]
            for _prime in _primes:
                simple_therm[0].append([_prime])
            therm_with_multiplication = reduce_therm(simple_therm, debug=debug)
            operators = get_operators(therm_with_multiplication)
            missing_operators = _n - operators

            if missing_operators != 0:
                if -maximum > -deviation / missing_operators or maximum < -deviation / missing_operators:
                    return f"für {initial_result} gibt es keinen Therm der Länge {_n}.", [[f"für {initial_result} gibt es keinen Therm der Länge {_n}."]]
            break
        else:
            simple_therm = therm_resulting_one(new_core_length, debug=debug)

            # multipliziere den term der 1 ergibt mit der gewünschten Zahl und Klammer aus.
            therm_with_multiplication = therm_times_factors(simple_therm, _primes, debug=debug)

        # zähle die anzahl an operatoren um zu sehen wie viele noch fehlen
        operators = get_operators(therm_with_multiplication)
        missing_operators = _n - operators
        if missing_operators != 0:
            if -maximum > -deviation / missing_operators or maximum < -deviation / missing_operators:
                missing_operators = 0
        # wenn es schon zu viele operatoren gibt (chance 2 147 in 100 000) rufe die Funktion nochmal auf
        i += 1

    if debug:
        operator_frequencies = get_operator_frequencies(therm_with_multiplication)
        print(f"operators: {operators}")
        print(f"missing operators: {missing_operators}")
        print(f"operator frequencies: {operator_frequencies}")
        therm_str = therm_to_str(therm_with_multiplication)
        print(f"therm: {therm_str}")
        print(f"result: {eval(therm_str)}")
        print()

    term_zero = get_addition_therm_resulting_to_(missing_operators, -deviation, debug=debug)
    if term_zero is None:
        return get_therm(_n, _result, debug)

    therm_with_multiplication.extend(term_zero)

    if debug:
        print(f"finished therm operator count: {get_operators(therm_with_multiplication)}")
        print(f"finished therm operators: {get_operator_frequencies(therm_with_multiplication)}")
        print(f"finished therm: {therm_with_multiplication}")
        stringified_therm = therm_to_str(therm_with_multiplication)
        print(f"finished therm stringified: {stringified_therm}")
        print(f"result: {eval(stringified_therm)}")

    return therm_to_str(therm_with_multiplication), therm_with_multiplication
