import time
import math
import itertools
from functools import reduce

primes = [2]

primes_rep_cache = {}

# primes = [None] * pow(10,7)
# primes[0]=2


SIZE = pow(2,10)
# SIZE = pow(10,6)
MAX_PRIME = math.ceil(math.log2(SIZE))
sieve = [None] * (SIZE+2)

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





def represent_as_primes(n1):
    n = n1
    ret = {}
    total = 0

    index = -1
    for p in primes:
        index += 1
        if p == None or p > n : break
        while n%p == 0:
            total +=1
            if p in ret:
                ret[p] = ret[p] + 1
            else:
                ret[p] = 1
            n = n/p

        if n in primes_rep_cache:
            prev_ret = primes_rep_cache[n]
            total += sum(prev_ret.values())
            for p in prev_ret.keys():
                if p in ret:
                    ret[p] += prev_ret[p]
                else:
                    ret[p] = prev_ret[p]
            n = 1
            break

    if n > 1:
        primes.append(n)
        # primes[index] = (n)
        total = 1
        ret[n] = 1

    if total < 7:
        primes_rep_cache[n1] = ret

    return total,ret



def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def is_co_divide(l):
    ret = False
    for i,v in enumerate(l):
        for j,v1 in enumerate(l):
            if (j <= i):
                continue
            else:
                if (v>v1 and v%v1 == 0) or (v<=v1 and v1%v == 0):
                    ret = True
                    break

        if ret:
            break
    return ret


assert not is_co_divide([1])
assert is_co_divide([1,1])
assert is_co_divide([2,4])
assert not is_co_divide([2,5])


def find_longest_antichain(i):
    S = list(factors(i))
    ret = [S[0]]
    l = len(S)
    for i in range(2,l+1):
        comb = list(itertools.combinations(S, i))
        # print("{} over {} : {} combinations" . format(l,i,len(comb)))
        for c in comb:
            if not is_co_divide(c):
                ret = c
                break

    # print (ret)
    return ret

def find_anti_chains(i,n):
    S = list(factors(i))
    ret = [S[0]]
    l = len(S)
    comb = list(itertools.combinations(S, n))
    for c in comb:
        if not is_co_divide(c):
            print(c)
            ret = c

    return ret


def count_options(position_limit,total):

    if len(position_limit) == 0 or total <= 0:
        if total == 0:
            return 1
        else:
            return 0
    ret = 0
    for i in range(position_limit[0],-1,-1):
        ret += count_options(position_limit[1:],total-i)
    return ret






def find_longest_antichain2(i):
    count,unique_primes = represent_as_primes_sieve(i)
    primes_as_key = list(unique_primes.values())

    # primes_as_key.sort(reverse=True)
    primes_as_key_str = '_'.join(str(c) for c in primes_as_key)




    if primes_as_key_str in key_res_match:
        ret = key_res_match[primes_as_key_str]
    else:
        total = sum(primes_as_key)
        total = math.floor(total/2)
        ret = count_options(primes_as_key,total)

        key_res_match[primes_as_key_str] = ret

    # print('key {} : {}{}'.format(primes_as_key_str,ret, ' retrieved from cache' if is_from_cache else ' caclulated first time'))
    return ret









# assert len(find_longest_antichain([1, 2, 3, 5, 6, 10, 15, 30])) == 3
# assert len(find_longest_antichain(list(factors(210)))) == 6
# print(represent_as_primes(1000))
# f = list(factors(1890))
# print(len(f))
# assert find_longest_antichain(list(factors(1890))) == 10

key_res_match ={}
ts = time.time()


def run_verification_for_primeKey_to_antiChain():
    global ts


    for i in range(2, 37):

        count, unique_primes = represent_as_primes(i)
        primes_as_key = list(unique_primes.values())
        primes_as_key.sort()
        primes_as_key = '_'.join(str(c) for c in primes_as_key)

        # if primes_as_key in key_res_match:
        #     continue

        print('--- going to calc', primes_as_key, )

        longest_length1 = find_longest_antichain2(i)
        print('--- Second ', " : ", time.time() - ts, 'sec')
        ts = time.time()

        res1 = find_longest_antichain(i)
        # res1 = find_anti_chains(i,10)
        print('--- First ', " : ", time.time() - ts, 'sec')
        ts = time.time()
        longest_length = len(res1)

        if (longest_length != longest_length1):
            raise Exception(i,longest_length,longest_length1)

        print(i,longest_length,longest_length1)

        key_res_match[primes_as_key] = longest_length

        print(primes_as_key, '\t', longest_length, '\t', unique_primes, '\t', len(unique_primes), '\t', res1)




def run_calc_sum_longest_chain():
    global ts

    s = 0
    print_threshold = 2

    for i in range(2, SIZE +1):
    # for i in range(2, 30 + 1):

        t = find_longest_antichain2(i)
        s += t
        # print(i,t,s)

        if i%print_threshold == 0:
            print_threshold *= 2
            print("{}\t{}\t{}".format(i,s,time.time() - ts))
            ts = time.time()

        # x = represent_as_primes(i)
        # if i%print_threshold == 0:
        #     print_threshold *= 2
        #     print("Calc till {}, in {} seconds".format(i,time.time() - ts))
        #     ts = time.time()
        #


    print( s+1 )




def run_calc_sum_represent_as_primes():
    global ts

    distribution_by_prime_representation = {}
    distribution_by_unique_prime_representation = {}

    s = 0
    print_threshold = 2

    for i in range(2, SIZE +1):
    # for i in range(2, 30 + 1):

        if (i == 4096): exit()

        count,unique_primes = represent_as_primes_sieve(i)
        # count,unique_primes = represent_as_primes(i)
        s += count
        # print(i,t,s)

        if count in distribution_by_prime_representation:
            distribution_by_prime_representation[count] += 1
        else:
            distribution_by_prime_representation[count] = 1

        if len(unique_primes) in distribution_by_unique_prime_representation:
            distribution_by_unique_prime_representation[len(unique_primes)] += 1
        else:
            distribution_by_unique_prime_representation[len(unique_primes)] = 1


        if True:
        # if i%print_threshold == 0:
            print_threshold *= 2
            # print("{}\t{}\t{}".format(i,s,time.time() - ts))
            print("{}\t{}\t{}".format(i,s,unique_primes))
            ts = time.time()

    print('---------------------------------')
    for key in distribution_by_prime_representation.keys():
        print("{}\t{}".format(key,distribution_by_prime_representation[key]))

    print('---------------------------------')

    for key in distribution_by_unique_prime_representation.keys():
        print("{}\t{}".format(key, distribution_by_unique_prime_representation[key]))

    print('---------------------------------')

        # x = represent_as_primes(i)
        # if i%print_threshold == 0:
        #     print_threshold *= 2
        #     print("Calc till {}, in {} seconds".format(i,time.time() - ts))
        #     ts = time.time()
        #


    print( s+1 )



run_verification_for_primeKey_to_antiChain()

# run_calc_sum_represent_as_primes()

# run_calc_sum_longest_chain()