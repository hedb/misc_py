import time
import math
import itertools




def SieveOfEratosthenes(n):
    primes = [True for i in range(n + 1)]
    ret = []

    p = 2
    while (p <= n):

        # If prime[p] is not changed, then it is a prime
        if (primes[p] == True):
            ret.append(p)

            # Update all multiples of p
            for i in range(p * 2, n + 1, p):
                primes[i] = False
        p += 1
    primes[0] = False
    primes[1] = False

    return ret






def calc_N(N):
    arr = [1]*N
    prev_value = 1
    last_one_changes = []
    # print(arr)
    for i in range(2,N):
        j = i-1
        while j < N:
            arr[j] = (arr[j]+1)%6
            if arr[j] == 0: arr[j] = 6
            j+=i
        # print(arr)
        if prev_value!=arr[N-1]:
            prev_value = arr[N - 1]
            last_one_changes.append(i)

    ret = []
    for i in range(0,len(arr)):
        if arr[i] == 1: ret.append(i+1)
    return arr.count(1),ret,last_one_changes

    return primes



def generating_all_permutations_rec(size,possible_powers):
    ret = []

    if size == 3:
        break_point = True

    if size == 1: return possible_powers
    else :
        suffixes = generating_all_permutations_rec(size-1,possible_powers)
        for s in suffixes:
            max_p_in_suffix = min(s)
            for prefix in possible_powers:
                if prefix[-1]<=max_p_in_suffix:
                    ret.append( prefix + s)
    return ret


def generating_all_permutations(permutation_size,possible_powers1):
    ret = []
    possible_powers = []
    for p in possible_powers1:
        possible_powers.append( [p] )
    for i in range(1,permutation_size+1):
        ret+= generating_all_permutations_rec(i,possible_powers)


    ret1 = set()
    ret2 = []
    for r in ret:
        if str(r) not in ret1:
            ret1.add(str(r))
            ret2.append(r)

    return ret2


primes_perm_cache = {}
def get_permutations(arr,size):
    if size in primes_perm_cache:
        return primes_perm_cache[size]
    ret = list(itertools.permutations(arr,size))
    primes_perm_cache[size] = ret
    return ret



def calc_N_1(N):
    top_power = math.floor(math.log(N,2))
    top_prime = math.floor( max( math.pow(N/16,1/4), math.pow(N,1/6) ))

    primes = SieveOfEratosthenes(top_prime)

    sum_so_far = 1; permutation_size = 0
    for i in range(0,len(primes)):
        sum_so_far = sum_so_far*math.pow(primes[i],4)
        if sum_so_far>N:
            permutation_size = i
            break

    possible_powers = [4,6]
    i = 1
    while True:
        if 4+i*6 > top_power: break
        else: possible_powers.append(4+i*6)
        if 6 + i * 6 <= top_power:  possible_powers.append(6+i*6)
        i+=1

    candidate_perms = generating_all_permutations(permutation_size,possible_powers)
    power_perms = []
    for perm in candidate_perms:
        swaps = 1
        for power in perm:
            swaps *= (power+1)
        if (swaps-1)%6 == 0:
            power_perms.append(perm)


    dice_positions = set()
    #merging primes & permutations
    for power_perm in power_perms:
        primes_perms = get_permutations(primes,len(power_perm))
        for primes_perm in primes_perms:
            sum = 1
            for i in range(0,len(power_perm)):
                sum = sum * math.pow(primes_perm[i],power_perm[i])
                if sum > N:
                    break;
            if sum <= N:
                dice_positions.add( int(sum) )


    return len(dice_positions)#,sorted(dice_positions)



for i in range(2,37):
    N = 10**i

# if True:
#     i=1
#     N=10**4

    start = time.time()
    print(i,N,calc_N_1(N), '{} seconds'.format(time.time()-start))

#
# for i1 in range(1,7):
#         if ((i1 + 1) - 1) % 6 == 0:
#             print(i1)
#
# for i1 in range(1,7):
#     for i2 in range(i1, 7):
#         if ((i1 + 1) * (i2 + 1) - 1) % 6 == 0:
#             print(i1, i2)
#
# for i1 in range(1, 7):
#     for i2 in range(i1, 7):
#         for i3 in range(i2, 7):
#             if ((i1 + 1) * (i2 + 1) * (i3 + 1) - 1) % 6 == 0:
#                 print(i1, i2, i3)
#
#
# for i1 in range(1, 7):
#     for i2 in range(i1, 7):
#         for i3 in range(i2, 7):
#             for i4 in range(i3, 7):
#                 if ((i1 + 1) * (i2 + 1) * (i3 + 1)* (i4 + 1) - 1) % 6 == 0:
#                     print(i1, i2, i3,i4)
