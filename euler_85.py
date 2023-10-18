

def calc_number_of_sub_rect(Rect):
    s = 0
    for i in range(0,Rect[0]):
        for j in range(0,Rect[1]):
            s += (Rect[0]-i) * (Rect[1]-j)
    return s








target = 2000000
best_so_far = (-1,target+1)

for w in range(0,100):
    for h in range(w,100):
        n = calc_number_of_sub_rect((w,h))
        diff = abs(target-n)
        print((w,h),n)
        if (diff < best_so_far[1]):
            best_so_far = ((w,h),diff)

print(best_so_far)
