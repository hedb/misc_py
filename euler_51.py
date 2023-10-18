
import cProfile
import math
import time

def return_primes(M,N):
    primes = [2]
    for i in range(2,N):
        so_far_prime = True
        for p in primes:
            if i % p  == 0:
                so_far_prime = False
                break
        if so_far_prime:
            primes.append(i)
    primes = [x for x in primes if x > M]
    return primes


def is_length_1(p,p1):
    ret= True

    p_str = str(p)
    p1_str = str(p1)
    p_digit = p1_digit = '-'
    replacement_positions = []

    for i in range(0,len(p_str)):
        if ( p_str[i] ==  p1_str[i] ) : continue
        if (p_digit == '-') :
            p_digit = p_str[i]
            p1_digit = p1_str[i]
            replacement_positions.append(i)
            continue
        if (p_digit == p_str[i] and p1_digit == p1_str[i]) :
            replacement_positions.append(i)
            continue
        ret = False; break;

    return ret,replacement_positions




def get_permutations(x,positions):
    permutations = []
    diff = 0
    for i in positions:
        diff += math.pow(10,len(str(x))-i-1)

    for i in range(int(str(x)[positions[0]]),9):
        x = x + diff
        permutations.append(x)
    return permutations


def main():
    n = 10
    while n<10000:
        n = n * 10
        primes = return_primes(n,n*10)
        l = len(primes)
        largest_family_so_far = []

        for i in range(0,l):
            p = primes[i]
            for j in range(i+1, l):
                p1 = primes[j]
                start_of_family,positions = is_length_1(p,p1)
                if start_of_family:
                    family = [p,p1]
                    perm = get_permutations(p1,positions)
                    for t in perm:
                        if t in primes:
                            family.append(t)
                    if (len(family) > len(largest_family_so_far)):
                        largest_family_so_far = family

        print(len(largest_family_so_far),"\t",largest_family_so_far)


cProfile.run('main()')