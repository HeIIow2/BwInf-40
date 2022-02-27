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


"""
def split_primes(n: int, number_elem: int):
    if n == 0 or n == 1:
        return [n] * number_elem

    def primes(n):
        primfac = []
        d = 2
        while d*d <= n:
            while (n % d) == 0:
                primfac.append(d)
                n //= d
            d += 1
        if n > 1:
           primfac.append(n)
        return primfac

    primes_ = primes(n)
    if len(primes_) <= number_elem:
        print(f"there are less than {number_elem} primes. Using {len(primes_)} primes")
        return primes_

    split_list = [1] * number_elem

    print(primes_)

    for prime in primes_:
        multiply_ind = random.randrange(len(split_list))
        split_list[multiply_ind] = split_list[multiply_ind] * prime

    return split_list
"""