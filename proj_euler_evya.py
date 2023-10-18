import random
def p493(x):
    k=0
    for i in range (0,x):
        urn=[]
        selected=[]
        for j in range(0,700):
            urn.append(int(j/10))

        for h in range(0,200):

            p=random.randint(0,len(urn)-1)

            selected.append(urn[p])
            del urn[p]
        for l in range(0,7):
            if l in selected:
                k=k+1

    print(k)

#p493(10000)




F = open("poker.txt",'r')
Print(F)
