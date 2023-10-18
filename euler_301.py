# https://projecteuler.net/problem=301
# https://docs.google.com/spreadsheets/d/1D6PYHvvIlNHJOQLM_GfoEDWkPkNrkCHCRr7B-7upKN0/edit#gid=0


def print_xor_test(n):
    l = len(format(3*n, 'b'))
    print(format(n, '0'+str(l)+'b'))
    print(format(2*n, '0'+str(l)+'b'))
    print(format(3*n, '0'+str(l)+'b'))


def verify_property_of_no_consecutive_1(n):
    n = format(n, 'b')
    for i in range(len(n)-1):
        if n[i] == '1' and n[i+1] == '1':
            return False
    return True

# print_xor_test(5)
def calc(NN):
    sum = 0
    for i in range(pow(2, NN)):
        xor_result = i ^ (i*2) ^ (i*3)
        if xor_result == 0: sum+= 1
        # if xor_result != 0 and verify_property_of_no_consecutive_1(i) \
        #     or \
        #     xor_result == 0 and not verify_property_of_no_consecutive_1(i):

            # print (i , xor_result , verify_property_of_no_consecutive_1(i))
            # # if xor_result == 0:
            # print_xor_test(i)
            # print("\n\n")
    return sum

a1 = 1
a2 = 2
for i in range(2,31):
    t = a2
    a2 = a1 + a2
    a1 = t
    print(i, a2 , calc(i) if i<20 else "too big")