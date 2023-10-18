

def calc_digit_sum(n):
    #calc sum of digits in string
    sum = 0
    for x in str(n):
        sum += int(x)
    return sum

# print( calc_digit_sum( 2 ) )

d = {}
for i in range(1,pow(2,32)):
    sum = calc_digit_sum(i)
    d[sum] = d.get(sum, 0) + 1

#print dictionry d
for key, value in d.items():
    print(key, value)

