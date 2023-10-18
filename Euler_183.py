import math


primes = [2]

for i in range(3,10001):
    is_prime = True
    for p in primes:
        if (i%p==0):
            is_prime = False
            break
    if is_prime:
        primes.append(i)


def break_into_primes(N):
    ret = []
    for p in primes:
        if (p > N):
            break
        while (N%p==0):
            ret.append(p)
            N=N/p
    return ret


def calc_P_max_1(N):
    best_so_far = 0
    ret = 0
    for i in range(2, N):
        tmp = math.pow(N / i, i)
        if (tmp > best_so_far) :
            best_so_far = tmp
            ret = i
    return ret

def calc_P_max_2(N,prev_p_max):
    if prev_p_max < 0 :
        best_so_far = 0
        ret = 0
        for i in range(2, N):
            tmp = math.pow(N / i, i)
            if (tmp > best_so_far) :
                best_so_far = tmp
                ret = i
    else :
        ret = prev_p_max
        d1 = abs(N/prev_p_max - math.e)
        d2 = abs(N/(prev_p_max +1) - math.e)
        # print(N,d1,d2)
        if (d2<d1):
            ret = prev_p_max+1
    return ret

def calc_P_max_3(N,prev_p_max):
    if prev_p_max < 0 :
        best_so_far = 0
        ret = 0
        for i in range(2, N):
            tmp = math.pow(N / i, i)
            if (tmp > best_so_far) :
                best_so_far = tmp
                ret = i
    else :
        ret = prev_p_max

        s_prev_dvided_by_s_prev_plus_1 = (prev_p_max +1) / N * (math.pow((prev_p_max +1)/prev_p_max,prev_p_max))
        if ( s_prev_dvided_by_s_prev_plus_1 < 1):
            ret = prev_p_max+1
    return ret

def is_terminal_decimal_ratio(x,y):
    x_break = break_into_primes(x)
    y_break = break_into_primes(y)
    # x_break - y_break
    for i in x_break:
        if i in y_break:
            y_break.remove(i)
    ret = True
    for p in y_break:
        if (p!=2 and p!=5):
            ret = False
            break
    return ret


def verify_closest_to_e(n,r):
    d1 = abs(n/(r-1) - math.e)
    d2 = abs(n/(r) - math.e)
    d3 = abs(n/(r+1) - math.e)
    ret = d2<d1 and d2<d3
    return ret

# for i in range(5,50):
#     print("{}/{} = {}".format(i,calc_P_max(i),i/calc_P_max(i)))


# print(is_terminal_decimal_ratio(100,600))
sum = 0
p_max = -1
for i in range(5,10001):
    # print ("{}/{}, {}".format(i,calc_P_max(i),i/calc_P_max(i)), is_terminal_decimal_ratio(i,calc_P_max(i)))
    # print(verify_closest_to_e(i,calc_P_max(i)))

    # p_max_orig = calc_P_max_1(i)
    p_max = calc_P_max_3(i,p_max)
    # if (p_max != p_max_orig):
    #     print(i,p_max_orig,p_max)

    if is_terminal_decimal_ratio(i,p_max):
        sum -= i
    else :
        sum += i

print (sum)

#
# test = 19
# print(test, 53/test, math.e-53/test ,math.pow(53/test,test))
# test = 20
# print(test, 53/test, math.e-53/test ,math.pow(53/test,test))
# test = 53 / math.e
# print(test, 53/test, math.e-53/test ,math.pow(53/test,test))