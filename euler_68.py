import itertools

l1 = list(range(6,11))
l1 = list(itertools.permutations(l1))

l2 = list(range(1,6))
l2 = list(itertools.permutations(l2))

combined = []
combined_matching = []

for beginning in l1:
    for ending in l2:
        # combined.append( (beginning,ending) )
        match = True
        for i in range(5):
            # print (beginning[i],ending[(i-1)%5],ending[i], " = ", beginning[i]+ending[(i-1)%5]+ending[i])
            if beginning[i]+ending[(i-1)%5]+ending[i] != 14:
                match = False
                break
        if match:
            starting_point = beginning.index(6)
            for i in range(5):
                i = (i + starting_point) % 5
                print (beginning[i],ending[(i-1)%5],ending[i], " = ", beginning[i]+ending[(i-1)%5]+ending[i])
            print ("\n\n\n")
            combined_matching.append( (beginning,ending) )

print(combined_matching)

