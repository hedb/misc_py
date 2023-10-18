import math


def my_print(*args):
    print(*args)

def verify_speacial_sum(arr):
    my_print(arr)
    d = len(arr)
    for split_index in range(1,int(math.pow(2,d-1))):
        split = ('{0:0' + str(d) + 'b}').format(split_index)
        len_a = len_b = sum_a = sum_b = 0
        for i in range(d):
            to_a = split[i] == '1'
            sum_a += 0 if not to_a else arr[i]
            sum_b += 0 if to_a else arr[i]
            len_a += to_a
            len_b += not to_a

        my_print("Checking: ",len_a,len_b,split,sum_a,sum_b)

        if sum_a == sum_b or (len_a > len_b and sum_a < sum_b) or (len_a < len_b and sum_a > sum_b):
            my_print("Failed. ",split,sum_a,sum_b)
            return False
    return True


# def calc_optimum(n,till_where_to_search):
#     ret = None
#     for i in range(n,till_where_to_search+1):
#         print(i)


if __name__ == '__main__':

    # calc_optimum(3,10)

    print(  verify_speacial_sum([6, 9, 11, 12, 13]) )
    print(  verify_speacial_sum([6, 9, 10, 11, 12]) )