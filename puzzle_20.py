import math
import random

N = 10

def generate_arr():
    ret = []
    for i in range(0,N):
        d = random.random()
        d =  1 if d < 0.4  else (2 if d < 0.8 else 3)
        ret.append(d)
    return ret

def count_blocks(arr):
    previous = -1
    block_number = 0

    for i in arr:
        if i != previous:
            block_number += 1
            previous = i
    return block_number

num_of_trials = 100000
sum_of_blocks = 0

for i in range(0,num_of_trials):
    arr = generate_arr()
    num_of_blocks = count_blocks(arr)
    # print(arr, num_of_blocks)
    sum_of_blocks += num_of_blocks

print(sum_of_blocks/num_of_trials)