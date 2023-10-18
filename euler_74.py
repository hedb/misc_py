
import math


factorial_dict = {}
for i in range(0,10):
    factorial_dict[i] = math.factorial(i)


def get_chain_length(n,already_visited):
    s = 0
    for d in [int(d) for d in str(n)]:
        s+=factorial_dict[d]
    if (s in already_visited):
        ret = 1
    else:
        already_visited[s] = True
        ret = 1+get_chain_length(s,already_visited)

    return ret



counter = 0
for i in range(0,100000):
    ret = get_chain_length(i,{})
    if (ret == 60):
        counter += 1

print(counter)