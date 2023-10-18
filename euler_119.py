import math


def get_digits_arr_with_float(n):
    digits = []
    while (n != 0):
        d = n - (math.floor(n / 10) * 10)
        n = (n - d) / 10
        digits = [d] + digits
    return digits

def get_digits_arr_with_string_format(n):
    digits = []
    s = format(n)
    for c in s:
        digits = [int(c)] + digits
    return digits



for n in range(2,200):
# for n in range(91,92):
    pwr = 1
    sum_of_digits = 0
    while pwr < 100:
        pwr=pwr+1
        p = pow(n,pwr)
        arr = get_digits_arr_with_string_format(p)
        sum_of_digits = 0
        for a in arr: sum_of_digits+= a;
        if (sum_of_digits == n):
            print(n,'\t',pwr,'\t',p)

