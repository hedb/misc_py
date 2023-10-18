import math



top_range = 1000*1000

best_so_far = 0
pair = None


for i in range(1,top_range) :
    top_candidate = math.floor(i*3/7)
    candidate = top_candidate / i
    if (candidate > best_so_far and candidate < 3/7):
        best_so_far = candidate
        pair = [top_candidate,i]


print('{} produce {}, target is {}'.format(str(pair),best_so_far,3/7))

