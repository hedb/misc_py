
import math
import random



def get_converge_index_empiracally(max_power):
    converge_point = 2**max_power-1
    yi = 0
    for i in range(1,100):
        xi = random.randint(0,converge_point)
        yi = yi|xi
        # print("{0:14b}".format(yi))
        if yi==converge_point:
            return i
    raise Exception("Didn't converge after X steps")

def binomial_cooeficient(x,y):
    ret = math.factorial(x) / math.factorial(y) / math.factorial(x-y)
    return ret

s = {1:2}
def get_converge_index(max_power):
    if max_power in s: return s[max_power]
    # assuming we have all prev values in s
    denominator = 2**max_power
    s_curr_coefficient = 1 - 1/denominator
    right_side = 2 * 1 / denominator
    for i in range(1,max_power):
        c = binomial_cooeficient(max_power,i)
        right_side += (c / denominator) * ( 1 + s[i] )
    ret = right_side / s_curr_coefficient
    return ret


# if True:
#     p = 2
for p in range(1,33):

    empiracally = True
    if empiracally:
        trials = 10000
        sum = 0.0
        for i in range(1,trials):
            tmp =  get_converge_index_empiracally(p)
            # print ('------ ' + str(tmp))
            sum += tmp
        res_p = sum/trials
    else:
        res_p = get_converge_index(p)
        s[p] = res_p
    print(p,'\t',res_p)

