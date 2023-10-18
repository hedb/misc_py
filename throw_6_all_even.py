import random
import math

N = 1000
number_of_throws = 0
number_of_attempts = 0

for i in range(1,N):
    tmp_number_of_throws = 0
    tmp_throw_series = []
    while True:
        successful_attempt = False
        tmp_number_of_throws += 1
        r = math.floor(random.random()*6+1)
        if  (r % 2 == 1):
            break
        tmp_throw_series.append(r)
        if (r == 6):
            successful_attempt = True
            print(tmp_throw_series)
            break

    if (successful_attempt):
        number_of_throws += tmp_number_of_throws
        number_of_attempts += 1

print ("Threw: " + str(N) + ", All even till 6: " + str(number_of_attempts) + ", avg number of throws: " + str(number_of_throws/number_of_attempts) )

