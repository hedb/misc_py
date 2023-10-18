import random

N = 10000

toss_sum = 0
for n in range(0,N):
    got_match = False
    toss_count = 0
    prev_coin = coin = -1

    while not got_match :
        toss_count +=1
        coin = random.randint(0,1)
        # if (coin == 0 and prev_coin == 0): # 0, 0 : 6
        if (coin == 1 and prev_coin == 0): # 1, 0 : 4
            got_match = True
        prev_coin = coin

    toss_sum += toss_count

print( 'Average toss needed is ' + str(toss_sum / N))
