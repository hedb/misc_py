import time
import csv

import itertools



FULL_MATRIX = []

with open('p345_matrix.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        FULL_MATRIX.append(row)


def get_partial_matrix(full,d):
    ret = []
    for x in range(d):
        ret.append([])
        for y in range(d):
            ret[x].append(FULL_MATRIX[x][y])
    return ret


def print_matrix(m):
    d = len(m)
    for x in range(d):
        for y in range(d):
            print(m[x][y], '\t', end='')
        print('')




def calc_max(m):
    d = len(m)

    res_prev = [m[0][0], [(0,0)] ]
    for i in range(2,d+1):
        tmp_m = get_partial_matrix(m,i)

        new_coordinate = (i-1,i-1)
        res_prev[1].append( new_coordinate )

        changed = [ new_coordinate ]
        while len(changed) > 0:
            replacement_target = changed.pop()
            replacement_candidate = None
            best_sum_so_far = 0

            for coord in res_prev[1]:
                current_sum = tmp_m [replacement_target[0]][replacement_target[1]] + tmp_m[coord[0]][coord[1]]
                new_sum = tmp_m [replacement_target[0]][coord[1]] + tmp_m[coord[0]][replacement_target[1]]
                diff = new_sum - current_sum
                if diff > 0 and new_sum > best_sum_so_far:
                    best_sum_so_far = diff
                    replacement_candidate = coord

            if replacement_candidate!= None:
                res_prev[1][replacement_candidate[1]] = (replacement_target[0],replacement_candidate[1])
                res_prev[1][replacement_target[1]] = ( replacement_candidate[0] , replacement_target[1] )

                changed.append( res_prev[1][replacement_candidate[1]] )
                changed.append( res_prev[1][replacement_target[1]] )


        res_prev[0] = 0
        for j,coord in enumerate(res_prev[1]):
            res_prev[0] += tmp_m[coord[0]][coord[1]]

    return res_prev


def calc_naive_max(m):
    d = len(m)
    perm = itertools.permutations( [x for x in range(d)] )
    ret = []
    for p in list(perm):
        tmp = []
        for x,y in enumerate(p):
            tmp.append( m[x][y] )
        if sum(tmp) > sum(ret):
            ret = tmp
    return sum(ret),ret


for i in range(2,12):

    start = time.time()
    m = get_partial_matrix(FULL_MATRIX,i)

    res = calc_naive_max(m)
    res1 = calc_max(m)

    print('\n\n')
    print_matrix(m)

    print("Naive: ",res, "  Advanced: ",res1)


    print(time.time() - start, ' seconds')





