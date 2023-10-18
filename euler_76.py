import math
import numpy as np
import re



# tmp = re.search(r"[^,]*,$", "1,112,")
# print(tmp.group())
# tmp = re.search(r"[^,]*,$", "1,")
# print(tmp.group())
# exit(1)

target = 20
backlog = {}


def full_join(a1,a2):
    ret = []
    for x in a1:
        for y in a2:
            if (y[0] >= x[len(x)-1]):
                ret.append( x+y )
    return ret


def full_join_string(a1,a2):
    ret = []
    for x in a1:
        for y in a2:
            last_number = re.search(r"[^,]*,$", x).group()
            if (last_number<=y ):
                # TBD SHOULD BE NUMBER COMPARISON
                ret.append(x+y)
    return ret

def list_remove_duplicates_string(arr):
    ret = list(set(arr))
    return ret


def list_remove_duplicates(arr):
    d = {}
    for a in arr:
        d[str(a)] = a
    ret = d.values()
    return ret


def full_join_numpy(arr1,arr2):
    return None


def calc_options_numpy(n):
    dtype1 = [('combinations', np.array)]
    dtype2 = [('factor', np.int)]
    arr2 = np.array( n ,dtype2)
    arr1 = np.array(arr2 ,dtype1)
    # for i in range(1,math.floor(n/2)+1):
    #     tmp = full_join_numpy(backlog[i],backlog[n-i])

    return None

def calc_options(n):
    ret = [[n]]
    for i in range(1,math.floor(n/2)+1):
        tmp = full_join(backlog[i],backlog[n-i])
        ret += tmp
    ret = list_remove_duplicates(ret)
    return ret

def calc_options_string(n):
    ret = [str(n)+","]
    for i in range(1, math.floor(n / 2) + 1):
        tmp = full_join_string(backlog[i], backlog[n - i])
        ret += tmp
    ret = list_remove_duplicates_string(ret)
    return ret


def main_simple():
    for i in range(1,target):
        backlog[i] = calc_options(i)
        # print (i," : ",len(backlog[i])-1)
        print (i," : ",len(backlog[i])-1, " : ",  backlog[i] )


def main_string():
    for i in range(1,target):
        backlog[i] = calc_options_string(i)
        # print (i," : ",len(backlog[i])-1)
        print (i," : ",len(backlog[i])-1, " : ",  backlog[i] )


def main_numpy():
    for i in range(1, target):
        backlog[i] = calc_options_numpy(i)
        print (i," : ",backlog[i].size, " : ",  backlog[i] )



cache = {}

def main_recursion(target,max_sum,indent):
    global cache
    total_options = 0

    key = "{}_{}".format(target,max_sum)

    if (key in cache):
        return cache[key]
    if target == 0 and max_sum == 0:
        total_options = 0
    elif (target <= 1):
        total_options = 1
    else:
        # print (indent + "starting g({},{})".format(target,max_sum))
        for leading_first_group in range(max_sum, 0,-1):
            sum_covered_by_first_group = leading_first_group
            index = 1
            while sum_covered_by_first_group <= target:
                total_options += main_recursion(target-sum_covered_by_first_group,leading_first_group-1, indent + "  ")
                sum_covered_by_first_group += leading_first_group
                index += 1

    # print (indent + "g({},{}) returns {} ".format(target,max_sum,total_options))
    cache[key] = total_options
    return total_options

def solution_chernish(coins, total):
    # tabulation way
    arr = [1] + [0] * total
    for coin in coins:
        for i in range(coin, total + 1):
            arr[i] += arr[i - coin]
    return 0 if total == 0 else arr[total]

# main_numpy()
# main_simple()
# main_string()

# print(main_recursion(19,18,""))
# print(main_recursion(100,99,""))

print(solution_chernish(list(range(1, 100)), 100))
