# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A):

    if len(A) < 2:
        return -1

    A1 = []
    for i,v in enumerate(A):
        A1.append((i,v))

    A1 = sorted( A1, key=lambda elem: elem[1] )

    adjacent_pairs = []
    prev = current = next_current = None

    for e in A1:
        if current == None:
            current = [e]; continue
        elif e[1] == current[0][1]:
            current.append(e)
        else:
            next_current = [e]
            # met new value
            if prev != None:
                for x in prev:
                    for y in current:
                        adjacent_pairs.append( (x[0],y[0]) )

            prev = current
            current = next_current
    # closing term
    if prev!=None:
        for x in prev:
            for y in current:
                adjacent_pairs.append((x[0], y[0]))


    min_pair = None
    for e in adjacent_pairs:
        if   min_pair == None  or abs(e[0]-e[1])<min_pair :
            min_pair = abs(e[0]-e[1])

    if min_pair==None:
        min_pair = -1

    return min_pair


arr = [0,3,3,7,5,3,11,1]
print( solution(arr) )

arr = [1,4,7,3,3,5]
print( solution(arr) )

print( solution(    []       ) )

print( solution(    [1]       ) )

print( solution(    [1,1,1]       ) )


print( solution(    [1,12,1]       ) )
