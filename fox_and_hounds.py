import itertools
import math

foxes = ['f1','f','f']
hounds = ['h','h']

all_arr = foxes + hounds

perm = list(itertools.permutations(all_arr))

print(len(perm),perm)


def check_if_f1_in_last_place(arr):
    ret = True
    encountered_f1 = False

    for x in arr:
        if x == 'f1':
            encountered_f1 = True; continue
        if encountered_f1 and x == 'h':
            ret = False
            break

    return ret

def check_if_f1_after_hound(arr):
    ret = False
    is_previous_is_hound = False
    for x in arr:
        if x == 'f1' and is_previous_is_hound:
            ret = True; break
        is_previous_is_hound = x == 'h'
    return ret



f1_after_hound = list(filter(check_if_f1_after_hound,perm))
print(len(f1_after_hound),f1_after_hound)


f1_in_last_place = list(filter(check_if_f1_in_last_place,perm))
print(len(f1_in_last_place),f1_in_last_place)


f1_after_hound = list(filter(check_if_f1_after_hound,f1_in_last_place))
print(len(f1_after_hound),f1_after_hound)