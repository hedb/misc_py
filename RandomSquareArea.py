import random

N = 1000000

sum = 0
for i in range(1,N):
    x1 = random.random()
    y1 = random.random()
    x2 = random.random()
    y2 = random.random()
    sum += abs((x1-x2)*(y1-y2))

print(sum/N)