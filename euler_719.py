from  math import *
import time


perm_cache = {}
def get_permutations(offset,string_length,token_length) :
    key = '{}_{}_{}'.format(offset,string_length,token_length)
    if key in perm_cache: return perm_cache[key]

    if string_length <= 0: return None
    else :
        ret = []
        for i in range(1,token_length+1):
            if i > string_length: continue
            tmp = [(offset,offset+i)]
            tmp1 = get_permutations(offset+i,string_length-i,token_length)
            if tmp1 !=None:
                for op in tmp1:
                    ret.append(tmp + op)
            else:
                ret.append(tmp)

        perm_cache[key] = ret
        return ret

# print ( get_permutations(0,4,3) )

assert get_permutations(0,1,1) == [   [(0, 1)]    ]
assert get_permutations(0,2,1) == [ [(0, 1), (1, 2)] ]
assert get_permutations(0,3,1) == [[(0, 1), (1, 2), (2, 3)]]
assert get_permutations(0,2,2) == [ [(0, 1), (1, 2)],   [(0, 2)]    ]
assert get_permutations(0,3,2) == \
    [   [(0, 1), (1, 2), (2, 3)],
        [(0, 1), (1, 3)],
        [(0, 2), (2, 3)]
        ]
assert get_permutations(0,4,3) == \
    [   [(0, 1), (1, 2), (2, 3), (3, 4)],
        [(0, 1), (1, 2), (2, 4)],
        [(0, 1), (1, 3), (3, 4)],
        [(0, 1), (1, 4)],
        [(0, 2), (2, 3), (3, 4)],
        [(0, 2), (2, 4)],
        [(0, 3), (3, 4)]
        ]

TN = 0
start = time.time()

for r in range(2,int(pow(10,6)) +1):
    sq = r*r
    sq_str = str(sq)
    r_l = floor( log10(r) + 1 )
    sq_l = floor( log10(sq) + 1 )
    permutations = get_permutations(0,sq_l,r_l)

    is_print1 =  (round(log2(r)) == log2(r))
    is_print2 = r%10000==0


    options = ', ' ;match_sign = '';is_perfect_square = False
    for p in permutations:
        tmp = ''; candidate_sum = 0;
        for t in p:
            token_s =sq_str[t[0]:t[1]]
            # tmp +=  token_s + '+'
            candidate_sum += int(token_s)
        # options += tmp[:-1] + ', '
        if candidate_sum == r:
            # match_sign ='-------'
            is_perfect_square = True

    if is_perfect_square:
        TN += sq


    if is_print1 or is_print2:
        prefix = '-----' if is_print1 else ''
        print (prefix,r,sq,time.time() - start)

print(TN)

