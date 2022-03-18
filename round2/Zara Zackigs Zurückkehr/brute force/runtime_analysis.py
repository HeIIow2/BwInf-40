def get_combinations(n, k):
    combinations = 0
    for i in range(n-k+1):
        combinations += n-k+1-i

    return combinations

def get_combinations_(n, k):
    return ((k**2-2*k*n*n-3*k+n**2+3*n+2)/2) + k**2-2*k*n-2*k+n**2+2*n+1

print(get_combinations(20, 4))

for j in range(1, 5):
    runtimes = []
    runtimes_diffrences = []
    start_x = 6
    for x in range(start_x,500,10):
        runtimes.append(get_combinations(x, 3))
        if x==start_x:
            continue
        runtimes_diffrences.append(runtimes[-1] - runtimes[-2])

    print(runtimes_diffrences)
