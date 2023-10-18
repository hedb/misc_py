import time
ts = time.time()

N = 10000000


s = set()
for i in range(0,N,3) :
    s.add(i)

for i in range(0,N,5) :
    s.add(i)

print(sum(s), time.time() - ts)


ts = time.time()
s = 0
for i in range(0,N) :
    if i%3 == 0 or i%5 == 0:
        s+=i


print(s,time.time() - ts)




