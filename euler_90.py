
needed_numbers =  [(0,1),(0,4), (0,9) , (1,6) , (2,5) , (3,6) , (4,9) , (6,4) , (8,1) ]

def can_generate_number(n,cube1,cube2):
    ret = False
    if (cube1[n[0]] and cube2[n[1]] ):
        ret = True
    elif (cube1[n[1]] and cube2[n[0]]):
        ret = True
    return ret

def can_generate_numbers(cube1,cube2):
    ret = True
    for n in needed_numbers:
        ret = can_generate_number(n,cube1,cube2)
        if (not ret):
            break
    return ret


def prepare_cube_for_69(cube) :
    if (cube[6] or cube[9]):
        cube[6] = cube[9] = True

def create_cube(arr):
    ret = {}
    for n in range(0,10):
        ret[n] = False
    for n in arr:
        ret[n] = True
    prepare_cube_for_69(ret)
    return ret

# cube1 = create_cube([0, 5, 6, 7, 8, 9])
# cube2 = create_cube([1, 2, 3, 4, 8, 9])


# print (can_generate_numbers(cube1,cube2))

def generate_all_possible_cubes():
    ret = []
    tmp_arr = [0,0,0,0,0,0]
    for i1 in range(0,10):
        for i2 in range(i1+1,10):
            for i3 in range(i2+1,10):
                for i4 in range(i3+ 1, 10):
                    for i5 in range(i4+ 1, 10):
                        for i6 in range(i5+ 1, 10):
                            ret.append(create_cube([i1,i2,i3,i4,i5,i6]))
    return ret

possible_cubes = generate_all_possible_cubes()
possible_cubes_len = len(possible_cubes)
distinct_num = 0

for i in range(0,possible_cubes_len):
    for j in range(i+1,possible_cubes_len):
        if (can_generate_numbers(possible_cubes[i],possible_cubes[j])):
            distinct_num += 1

print(distinct_num)


