
import cProfile
import math
import time

counter = {}

for i in range(1,10):
    for j in range(1, 10):
        s = i+j
        key = ('<10' if (s<10) else 's>=10') + ',' +  ('even' if s%2 == 0 else 'odd')
        if key in counter:
            counter[key] += 1
        else:
            counter[key] = 1
        print(i,j,key)

print (counter)
exit()

def get_digits_arr(n):
    digits = []
    while (n != 0):
        d = n - (math.floor(n / 10) * 10)
        n = (n - d) / 10
        digits = [d] + digits
    return digits

def reverse(n):
    allowed_to_be_reversed = True
    digits = get_digits_arr(n)
    if (digits[-1] == 0): allowed_to_be_reversed = False
    ret = 0
    pos = 0
    for d in digits:
        ret += d * math.pow(10,pos)
        pos += 1

    return ret,allowed_to_be_reversed


def is_all_odd(n):
    ret = True
    digits = get_digits_arr(n)
    for d in digits:
        if (d%2 == 0):
            ret = False
    return ret



def main():
    number_of_reversible = 0
    t0 = time.time()
    for i in range(1,n):
        reverse_i, is_allowed = reverse(i)
        if (is_allowed and reverse_i>i):
            s = i + reverse_i
            if is_all_odd(s):
                number_of_reversible += 1
                # print (i,reverse_i,s)
    t1 = time.time()
    print(n," : ", number_of_reversible*2,t1-t0)


n = 10
while n<(1000*1000*1000 + 1):
    n = n * 10
    # cProfile.run('main()')
    main()

# n = 1000*1000*10
# main()