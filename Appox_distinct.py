import random

num = []
distinct = {}

for i in range(1,1000000):
    x = random.randint(1, 1000)
    num.append(x)
    distinct[x] = 1

print("distinct =" + str(len(distinct)))


calc_approx_distinct()
