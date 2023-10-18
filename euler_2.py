

n3 = 0
n1= 1
n2= 1
s =0
while n1<4000000:
    n1 = n3+n2
    n3 = n2
    n2 = n1
    if n1%2 == 0 :
        print(n1)
        s +=n1
print(n1)
print(s)