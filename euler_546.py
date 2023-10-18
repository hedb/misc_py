import math
import time


for p in range(0,14):
    sum = 0
    start_time = time.time()
    for i in range(0,int(math.pow(10,p))):
        sum + 13
        sum = sum%7
    print ('finished 10^{} in {} sec'.format(p,time.time()-start_time))

exit()


def rec_print(s):
    print(s)
    pass

DIVISOR = 7
cache = {}
start_time = 0

def f(is_first,k,pre_n,indent):
    global cache
    global start_time

    call_tree = 1

    if (is_first):
        start_time = time.time()

    n = pre_n
    if (not is_first) and (pre_n != 0):
        n = math.floor(pre_n/k)

    key = "{}_{}".format(k,n)
    if (key in cache):
        return (cache[key],call_tree)

    indent_space = str(indent) + '\t'
    indent_tab = '\t' * indent


    if (n==0):
        rec_print (indent_space + "f({},floor({}/{}))".format(k,pre_n,k) + indent_tab + "1")
        # print(indent + "1")
        return 1,call_tree
    else:
        if not is_first:
            rec_print (indent_space + "f({},floor({}/{}))".format(k,pre_n,k))
            pass

        indent += 1
        sum = 0

        start_ind = 0
        key_minus_1 = "{}_{}".format(k, n - 1)
        if (key_minus_1 in cache):
            sum = cache[key_minus_1]
            start_ind = n

        for i in range (start_ind,n+1):
            sub_tree_calls = 0
            sub_tree_sum = 0

            (sub_tree_sum, sub_tree_calls) = f(False,k,i,indent)
            call_tree +=sub_tree_calls
            sum += sub_tree_sum
            sum = sum % DIVISOR

        if is_first:
            print("f({},{}) returns {} after {} recursion in {} sec".format(k, n,sum,call_tree,time.time()-start_time))

        cache[key] = sum
        return (sum, call_tree)


# assert f(True,5,10,0)[0] == 18%DIVISOR
# assert f(True,7,100,0)[0] == 1003%DIVISOR
assert f(True,2,1000,0)[0] == 264830889564%DIVISOR

# for i in range(1,14):
#     f(True, 2, int(math.pow(10,i)), 0)

# sum = 0
# for k in range(2,10+1):
#     sum += f(k,math.pow(10,14))
#     cache = {}
#     sum = sum % DIVISOR
# print (sum)