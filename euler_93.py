

results = []
numbers = [1,2,3,4]

arr2 = [1,2]


def clean(arr):
    tmp = [x for x in arr if x > 0 and x % 1 == 0]
    ret = list(set(tmp))
    ret.sort()
    return ret

def h2(a,b): #handle_2
    if (a == 0 or b ==0 ):
        tmp = [a + b, a * b, a - b, b - a, 0]
    else :
        tmp = [a+b, a*b, a-b, b-a, a/b, b/a ]

    return clean(tmp)



def h2_a(arr,b):
    ret = []
    for a in arr:
        ret += h2(a,b)
    return clean(ret)


def h3(a,b,c): #handle_3
    ret = []
    tmp = [
        h2_a(h2(a,b),c) ,
        h2_a(h2(a,c),b) ,
        h2_a(h2(b,c),a) ]

    for sublist in tmp:
        for item in sublist:
            ret.append(item)

    return clean(ret)


def h3_a(arr,b,c):
    ret = []
    for a in arr:
        ret += h3(a,b,c)
    return clean(ret)


def h4(a,b,c,d): #handle_3
    ret = []
    tmp = [
        h3_a(h2(a,b),c,d) ,
        h3_a(h2(a,c),b,d) ,
        h3_a(h2(a,d),c,b) ,
        h3_a(h2(b,c),a,d) ,
        h3_a(h2(b,d),c,a) ,
        h3_a(h2(c,d),a,b)
    ]

    for sublist in tmp:
        for item in sublist:
            ret.append(item)

    return clean(ret)




def find_longest_streak(arr):
    arr.sort()
    prev = .5
    streak = 0
    max_streak = 0

    for  x in arr:
        if (x - prev) == 1:
            streak += 1
        else:
            if (streak > max_streak):
                max_streak = streak
            streak =0
        prev = x

    if (streak > max_streak):
        max_streak = streak

    return max_streak


# arr = h4(6,7,8,9)
# print(arr)
# print(find_longest_streak(arr))
# exit()


longest_streak = 0
winning_arr = []


all_results = []

for a in range(0,10):
    for b in range(a+1, 10):
        for c in range(b+1, 10):
            for d in range(c+1, 10):
                current_streak = find_longest_streak(h4(a, b, c, d))
                all_results.append({"digits":[a,b,c,d], "streak":current_streak} )
                if (current_streak > longest_streak):
                    longest_streak = current_streak
                    winning_arr = [a,b,c,d]

print(winning_arr)
# print(longest_streak)
# print (h4(1,2,5,8))
def according_to_streak(elem):
    return elem["streak"]

all_results.sort(key=according_to_streak,reverse=True)
print(all_results)