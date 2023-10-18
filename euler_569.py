

import time
from sortedcontainers import SortedSet
import itertools as it


N =  2500000


def erat3( ):
    D = { 9: 3, 25: 5 }
    yield 2
    yield 3
    yield 5
    MASK= 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0,
    MODULOS= frozenset( (1, 7, 11, 13, 17, 19, 23, 29) )

    for q in it.compress(
            it.islice(it.count(7), 0, None, 2),
            it.cycle(MASK)):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D or (x%30) not in MODULOS:
                x += 2*p
            D[x] = p




start = time. time()

def calc_primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * (n//2)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]

# primes = calc_primes(N**2)

prime_gen = erat3()
next(prime_gen)

# print("calculated {} primes, took {} sec".format(N**2,time.time()-start))


peaks = [(2,2)]

for i in range(1,N+1):

    p1 = next(prime_gen)
    p2 = next(prime_gen)
    peaks.append( ( peaks[i-1][0] + p1 + p2 , peaks[i-1][1] + p2 - p1  ) )
    # peaks.append( ( peaks[i-1][0] + primes[i*2-1] + primes[i*2] , peaks[i-1][1] + primes[i*2] - primes[i*2-1]  ) )
    # print(peaks[-1])



def is_in_line_of_site(viewer,last_blocker,candidate):

    viewer_to_blocker = (viewer[1]-last_blocker[1]) / (viewer[0]-last_blocker[0])
    viewer_to_candidate = (viewer[1] - candidate[1]) / (viewer[0] - candidate[0])

    return viewer_to_blocker > viewer_to_candidate


lines_of_sight = [[],[0]]

for i in range(2,N): # starting from the third one


    viewed_peaks = [i-1]
    candidates_to_check = SortedSet(lines_of_sight[i-1])

    while len(candidates_to_check) > 0:
        candidate = candidates_to_check.pop()
        if (is_in_line_of_site(peaks[i], peaks[viewed_peaks[-1]], peaks[candidate] )):
            viewed_peaks.append(candidate)
            candidates_to_check = candidates_to_check.union(lines_of_sight[candidate])


    # for j in range(i-2,0,-1):
    #     if (is_in_line_of_site(peaks[i], peaks[viewed_peaks[-1]], peaks[j] )):
    #         viewed_peaks.append(j)


    lines_of_sight.append(viewed_peaks)



sum = 0
for i in range(0,N):
    # print (lines_of_sight[i])
    sum += len(lines_of_sight[i])

print("{} : {}, took {} sec".format(N,sum,time.time()-start))
