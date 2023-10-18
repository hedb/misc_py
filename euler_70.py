import time
import math
import itertools
from functools import reduce

primes = [2]
primes_rep_cache = {}
ts = time.time()

# primes = [None] * pow(10,7)
# primes[0]=2


SIZE = pow(10,7)
sieve = [None] * (SIZE+2)
MAX_PRIME = math.ceil(math.log2(SIZE))

def represent_as_primes_sieve(n):
    if sieve[n] == None:
        # prime
        for power in range(1,MAX_PRIME): # max # of primes in 10^8
            n_power = pow(n,power)
            for i in range(n_power,SIZE+1,n_power):
                if sieve[i] is None:
                    sieve[i] = {n: power}
                else :
                    sieve[i][n] = power


    return sum(sieve[n].values()),sieve[n]

def calc_phi(i,unique_primes):
    

def run_calc_sum_represent_as_primes():
    global ts
    s = 0
    print_threshold = 2

    for i in range(2, SIZE +1):
        # if (i == 4096): exit()

        count,unique_primes = represent_as_primes_sieve(i)
        s += calc_phi(i,unique_primes)
        # print(i,t,s)


        # if True:
        # if print_threshold - i < 3:
        if i%print_threshold == 0:
            if i%print_threshold == 0: print_threshold *= 2
            print("{}\t{}\t{}\t{}".format(i,s,unique_primes,time.time() - ts))
            ts = time.time()

run_calc_sum_represent_as_primes()