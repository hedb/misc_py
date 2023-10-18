

def SieveOfEratosthenes(n):
    primes = [True for i in range(n + 1)]

    p = 2
    while (p * p <= n):

        # If prime[p] is not changed, then it is a prime
        if (primes[p] == True):

            # Update all multiples of p
            for i in range(p * 2, n + 1, p):
                primes[i] = False
        p += 1
    primes[0] = False
    primes[1] = False

    return primes

if __name__ == '__main__':
    n = 1000*1000
    primes = SieveOfEratosthenes(n)

    best_so_far = {"length":0}
    # Print all prime numbers
    for p1 in range(n + 1):
        if primes[p1]:
            length = 1
            p_seq = [p1]
            for p2 in range(p1+1,n+1):
                if primes[p2]:
                    p_seq.append(p2)
                if sum(p_seq) >= n:
                    break
                if primes[sum(p_seq)] and len(p_seq) > best_so_far['length']:
                    best_so_far = {'length':len(p_seq), 'p':p1, 'sum':sum(p_seq), 'list':list(p_seq) }

    print(best_so_far)



