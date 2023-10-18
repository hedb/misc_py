import math
import random

def find_max_xor(arr):
    max_so_far = 0
    a = b = 0

    for i in arr:
        for j in arr:
            if i^j > max_so_far:
                max_so_far = i^j
                a = i
                b = j
    return max_so_far,"{0:14b}".format(max_so_far).replace(" ","0"),a,"{0:14b}".format(a).replace(" ","0"),b,"{0:14b}".format(b).replace(" ","0")


def find_max_xor_o_n(arr1):
    arr = []
    L = 0
    for i in arr1:
        L = max(L,math.ceil(math.log2(i)))

    for i in arr1:
        arr.append( ("{0:"+str(L)+"b}").format(i).replace(" ","0") )

    return (L,arr)





# for i in range(1,100):
#     print(str(random.randint(0,10000)) + ", ",end='')

arr = [190, 895, 346, 3421, 9008, 4923, 1317, 5723, 6050, 5772, 8370, 2754, 1396, 9745, 1814, 9696, 1727, 6544, 5830, 9884, 5638, 7881, 6648, 2819, 4092, 5596, 3180, 8307, 48, 3210, 8759, 717, 2433, 5316, 3967, 9797, 5447, 5135, 5648, 1369, 8895, 3569, 6022, 5293, 7582, 3084, 2490, 8966, 9615, 9668, 6155, 8104, 3293, 24, 7416, 1087, 1255, 7184, 9459, 1912, 8376, 1241, 6149, 3860, 2068, 2670, 7314, 1502, 132, 4561, 579, 8739, 3400, 855, 9438, 9706, 5873, 6514, 7543, 8540, 4601, 3820, 7014, 3806, 3089, 2685, 3532, 4119, 1049, 7127, 1277, 1650, 4775, 8137, 5738, 4751, 4307, 9725, 7427]
# arr = [7,6,3]

ret = find_max_xor(arr)
print(ret)

ret = find_max_xor_o_n(arr)
print(ret)