# https://projecteuler.net/problem=187
import math
import time

def efficient_get_primes(n):
    primes = []
    is_prime = [True] * (n + 1)
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(2 * i, n + 1, i):
                is_prime[j] = False
    return primes


def get_primes(n):
    primes = [2]
    for i in range(3,n+1):
        is_prime = True
        for p in primes:
            if i % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes


N = int(math.pow(10,8))

# t = time.time()
# p = get_primes( N )
# print("get_primes took", time.time() - t, "seconds")
t = time.time()
p = efficient_get_primes( N )
print("efficient_get_primes took", time.time() - t, "seconds")

# print(p)
# exit(1)


lower_ind = 0
upper_ind = len(p)-1
sum = 0

while lower_ind <= upper_ind:
    if p[lower_ind] * p[upper_ind] <= N:
        print("{}({}), {}({})".format(p[lower_ind] ,lower_ind, p[upper_ind],upper_ind))
        sum += upper_ind - lower_ind + 1
        lower_ind += 1
    else:
        upper_ind -= 1

print(sum)


