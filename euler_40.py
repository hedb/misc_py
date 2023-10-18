

s = '0.'
for i in range(1,1000):
    s += str(i)

def get_digit(i):
    return s[i+1]

print(s)
print(get_digit(12))
print(get_digit(9))
print(get_digit(23))
print(get_digit(225))
print(get_digit(518))
print(get_digit(519))