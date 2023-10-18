import random




N = 100000
same = 0

for i in range(0,N):
    arr = [random.randint(0,1),random.randint(0,1),random.randint(0,1)]
    i1 = random.randint(0,2)
    i2 = random.randint(0,2)
    if arr[i1] == arr[i2]:
        same += 1



# print (same/N)