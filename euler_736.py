import sys
from dataclasses import dataclass
import time



@dataclass
class FuncPath:
    path: []
    result: (int,int)
    count: (int,int)


def r( i:(int,int) ) -> (int,int):
    return (i[0]+1,2*i[1])

def s( i:(int,int) ) -> (int,int):
    return (2*i[0],i[1]+1)

initial = FuncPath(path=[],result=(45,90),count=(0,0))
q = [ initial ]

ts = time.time()

def explore1():
    j = 10

    # how_many_options_with_r_s_equals = {}
    for i in range(1,pow(2,15)):
        f = q.pop(0)
        if i == int(pow(2,j)):
            j += 1
            ts1 = time.time()
            # print ( i, ' : ',  ts1 - ts )
            ts = ts1

        # if (f.result[0] == f.result[1]):
        l = len(f.path)
        if (l%2 == 0):
            print ( [ i.__name__ for i in f.path] ,'\t',f.result, '\t', f.result[0]/ f.result[1], '\t',l, '\t',f.count[0], '\t',f.count[1])
            # if f.count[0] == f.count[1]:
            #     if l in how_many_options_with_r_s_equals:
            #         # how_many_options_with_r_s_equals[l] += [ [ i.__name__ for i in f.path] ]
            #         how_many_options_with_r_s_equals[l] += 1
            #     else:
            #         # how_many_options_with_r_s_equals[l] = [ [ i.__name__ for i in f.path] ]
            #         how_many_options_with_r_s_equals[l] = 1
            if (f.result[0] == f.result[1]):
                print('-----------------------------------------------------------------')
                exit(100)

        q.append( FuncPath(f.path + [r],r(f.result) , (f.count[0]+1,f.count[1]) ))
        q.append( FuncPath(f.path + [s],s(f.result) , (f.count[0],f.count[1]+1) ))
    # print (how_many_options_with_r_s_equals)




def explore_r_s_of_equal_size():
    for i in range(1,100):
        tmp = initial
        for j in range(0,i):
            tmp = FuncPath(path= tmp.path + [r],result=r( tmp.result), count=(tmp.count[0]+1,tmp.count[1]) )
        for j in range(0,i):
            tmp = FuncPath(path= tmp.path + [s],result=s( tmp.result), count=(tmp.count[0],tmp.count[1]+1) )

        print ( [ i1.__name__ for i1 in tmp.path] ,'\t',tmp.result, '\t', tmp.result[0]/ tmp.result[1], '\t',i)
        if (tmp.result[0] == tmp.result[1]):
            print('-----------------------------------------------------------------')
            exit(100)


def explore_s_Longer_by_2_and_r():
    for i in range(1,100):
        tmp = initial
        for j in range(0,i+2):
            tmp = FuncPath(path= tmp.path + [s],result=s( tmp.result), count=(tmp.count[0],tmp.count[1]+1) )
        for j in range(0,i):
            tmp = FuncPath(path= tmp.path + [r],result=r( tmp.result), count=(tmp.count[0]+1,tmp.count[1]) )

        print ( [ i1.__name__ for i1 in tmp.path] ,'\t',tmp.result, '\t', tmp.result[0]/ tmp.result[1], '\t',   i)
        if (tmp.result[0] == tmp.result[1]):
            print('-----------------------------------------------------------------')
            exit(100)

def rs_expend(path):
    ret = []
    for i,r_stretch in enumerate(path):
        for j in range(0,r_stretch):
            ret.append(s)
        if i<len(path)-1:
            ret.append(r)
    return ret



def fill_all_perm(path,next_index,sum_till_here,total_sum,all_paths,res):
    if next_index == len(path):
        if sum_till_here == total_sum:
            # all_paths.append(rs_expend(path))
            test_path(rs_expend(path), res)
        return

    for i in range(0,total_sum-sum_till_here+1):
        path[next_index] = i
        fill_all_perm(path,next_index+1,sum_till_here+i,total_sum,all_paths,res)

def path_to_str(path):
    return str([ i.__name__ for i in path])

def explore_all_r_s_permutations(r_count:int,s_more_than_r:int):
    res = { 'val':sys.maxsize }
    # for N in range(1,r_count):
    for N in range(r_count,r_count+1):
        all_paths = []
        slots = N+1
        path = slots * [0]
        fill_all_perm(path,0,0,N+s_more_than_r,all_paths,res)

        for path in all_paths:
            test_path(path, res)

    return res


def test_path(path, res):
    tmp = (45, 90)
    for step in path:
        tmp = step(tmp)
    # print(path_to_str(path), '\t', tmp, '\t', tmp[0] / tmp[1], '\t', len(path))
    print( tmp, '\t', tmp[0] / tmp[1], '\t', len(path))
    if (tmp[0] == tmp[1]):
        print('-----------------------------------------------------------------')
        exit(100)
    abs_diff = max(tmp[0] / tmp[1], tmp[1] / tmp[0]) - 1
    if abs_diff == res['val']:
        res['data'] = {'path': path_to_str(path), 'v0': tmp[0], 'v1': tmp[1], 'val': max(tmp[0] / tmp[1], tmp[1] / tmp[0])}
    elif abs_diff < res['val']:
        res['val'] = abs_diff
        res['data'] = {'path': path_to_str(path), 'v0': tmp[0], 'v1': tmp[1], 'val': max(tmp[0] / tmp[1], tmp[1] / tmp[0])}


# https://projecteuler.net/problem=736
# https://docs.google.com/spreadsheets/d/11sqtXVSjt5q-6s9GJ58dMOxssiM-d2dDX9TRDMS-CYE/edit#gid=0

# explore_all_equal_size_permutations(5)

N = 45

v1 = explore_all_r_s_permutations(N,0)
# v2 = explore_all_r_s_permutations(N,2)

print(v1['data'])
# print(v2['data'])