import time


def SieveOfEratosthenes(n):
    primes = [set() for i in range(n + 1)]

    p = 2
    while (p <= n):

        # If prime[p] is not changed, then it is a prime
        if (len(primes[p]) == 0):
            primes[p].add(p)

            # Update all multiples of p
            for i in range(p * 2, n + 1, p):
                primes[i].add(p)
        p += 1
    primes[0] = set()
    primes[1] = set()

    return primes

distinct_factorization = SieveOfEratosthenes(20)
assert distinct_factorization[10] == {2,5}
assert distinct_factorization[8] == {2}
assert distinct_factorization[15] == {3,5}

def method0() :
    M=10

    while M < 1000*1000+1:
    # if True:
        start_time = time.time()

        distinct_factorization = SieveOfEratosthenes(M+1)
        mid_time = time.time()

        number_elements = []
        number_of_distinct = 0

        for n in range(1,M+1):
            for d in range(n+1, M + 1):
                if len(distinct_factorization[n] & distinct_factorization[d]) == 0:
                # if True:
                    number_of_distinct += 1

        end_time = time.time()

        print(M,'\t:\t',number_of_distinct,"\t mid_time:\t",mid_time-start_time,"\t end_time:\t",end_time-start_time)
        M *=2


def method1(M) :
    distinct_factorization = SieveOfEratosthenes(M+1)

    number_of_distinct = 0

    for n in range(1,M+1):
        for d in range(n+1, M + 1):
            if len(distinct_factorization[n] & distinct_factorization[d]) == 0:
                if n/d > 1/3 and n/d < 1/2:
                    number_of_distinct += 1

    return number_of_distinct



def  method2(M) :

    n = 1
    distinct_factorization = SieveOfEratosthenes(M+1)
    disjoints_count = 0
    disjoints = [True] * (M + 1)

    while n<M:

        for i in range(0,M+1):
                disjoints[i] = True

        for p in distinct_factorization[n]:
            t = n+p
            while t <= M:
                disjoints[t] = False
                t+=p

        for t in range(n+1,M+1):
            if disjoints[t]:
                # print('{} / {}'.format(n,t))
                disjoints_count += 1

        n += 1

    return disjoints_count

# print(method1(80))
# print(method2(80))


M=12000

# ׳while M < 1000*1000+1:
if True:
    start_time = time.time()
    number_of_distinct = method1(M)
    # number_of_distinct = method2(M)
    end_time = time.time()
    print(M,'\t:\t',number_of_distinct,"\t end_time:\t",end_time-start_time)
    M *=2

