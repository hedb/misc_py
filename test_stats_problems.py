
import random

N=100
sum = 0
succesful_series = 0
for n in range(1,N):
    i=0
    x=-1
    arr = []
    while x!=6 :
        x = random.randint(1,6)
        arr.append(x)
        i+=1
        if x%2==1:
            break
    if x==6:
        sum += i
        succesful_series += 1
        print(arr)

print(sum/succesful_series)
