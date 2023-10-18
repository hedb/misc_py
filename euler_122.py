import math
import time


# def get_all_permutations(values,permutation_size,prefix = []):
#     ret = []
#
#     if len(prefix) == permutation_size:
#         return [prefix]
#
#     for v in values:
#         tmp = get_all_permutations(values,permutation_size,prefix + [v])
#         # ret.append(tmp)
#         ret += tmp
#
#     return ret
#
#
# def main_attempt_1():
#     # We shall define m(k) to be the minimum number of multiplications to compute n^k; for example m(15) = 5.
#     MAX_M_IN_200_RANGE = 2
#     ITERATIONS = 2
#
#     m_values = {1:(0,[]),   2:(1,[1,1]) }
#
#     for i in range(ITERATIONS):
#         for perm_size in range(1,MAX_M_IN_200_RANGE+1):
#             permutations = get_all_permutations(m_values.keys(),perm_size)
#
#             t = 1
#
#             for perm in permutations:
#                 sum = 0
#                 cost = 0
#                 for v in perm:
#                     sum += v
#                     cost += m_values[v][0]
#                 if sum not in m_values or m_values[sum][0] > cost:
#                     m_values[sum] = (cost,perm)
#
#             print("Iteration:",i,", size",perm_size)
#             for p in permutations:
#                 print("\t",p)
#
#     for m in m_values.items():
#         print(m)

# def generate_perm_on_set(available_values,generated_values,length):
#     ret = []
#
#     if length == 0:
#         return None
#
#     for v in available_values:
#         curr = [v]
#         postfix_options = generate_perm_on_set(available_values,generated_values,length-1)
#         if postfix_options == None:
#             ret.append(curr)
#         else:
#             for p in postfix_options:
#                 new_option = curr + p
#                 candidate_value = sum(new_option)
#                 if candidate_value not in available_values:
#                     generated_values.add(candidate_value)
#                 ret.append(new_option)
#
#     return ret
#
# def main_attempt_2():
#     existing_values = {1}
#     newly_available_values = set()
#     res = []
#
#     for i in range(8):
#         res += generate_perm_on_set(existing_values,newly_available_values,2)
#         existing_values = existing_values.union(newly_available_values)
#         newly_available_values = set()
#
#
#
#     print(len(existing_values),existing_values)
#     print(res)


# 9 87.2920880317688
#  {8: 2987743, 7: 88251, 6: 3573, 5: 209, 4: 19, 3: 3, 2: 1, 1: 1}



depth_counters = {}

def make_one_multiplication_move(available_values,depth):
    global m_values
    if not isinstance(available_values,list) :
        raise Exception("should be list")

    if depth == MAX_DEPTH:
        return

    start = time.time()

    for v1 in available_values:
        for v2 in available_values:
            new_v = v1+v2
            if new_v not in available_values:
                make_one_multiplication_move(available_values + [new_v],depth+1)
            if new_v not in m_values or m_values[new_v][0] > depth:
                m_values[new_v] = (depth,[v1,v2])


    key = sorted(available_values)
    key_str = str(key)
    print(key_str)

    # print
    if MAX_DEPTH - depth > 3:
        print(depth, time.time() - start )
    if depth not in depth_counters: depth_counters[depth] = 0
    depth_counters[depth] += 1

    pass

if __name__ == '__main__':

    #     # We shall define m(k) to be the minimum number of multiplications to compute n^k; for example m(15) = 5.

    N = 100
    MAX_DEPTH = 9
    m_values = { 1:(0,[]) }

    make_one_multiplication_move([1],1)

    # print(len(m_values))
    # for m in m_values.items():
    #     print(m)

    count = 0
    sum = 0

    for i in range(N):
        if i in m_values:
            print(i," : ",m_values[i])
            count += 1
            sum += m_values[i][0]

    print(count)
    # print(depth_counters)

