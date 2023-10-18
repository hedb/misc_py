
black_squares = []

def square_key(pos):
    return str(pos[0]) + "," + str(pos[1])

def step(pos):

    if square_key(pos) in black_squares:
        black_squares.remove(square_key(pos))
        pos[2] = pos[2]-1 if (pos[2]>0) else 3
    else :
        black_squares.append(square_key(pos))
        pos[2] = pos[2]+1 if (pos[2]<3) else 0

    if (pos[2]==0 or pos[2]==2):
        pos[1] = pos[1] + ( 1 if pos[2]==0 else -1  )
    else:
        pos[0] = pos[0] + ( 1 if pos[2]==1 else -1  )

    return pos



pos = [0,0,0] # x,y,direction (up:0,right:1,down:2,left:3)
# print('pos:', pos)
previous_length = 0
sequence_as_str = ''


modolu_312 = {}
for i in range(1,10608):
    pos = step(pos)

    modolu_312[i%312] = (i,len(black_squares))

    # if (i %312 == 0 ):
    # print(i,'\t',len(black_squares))

    # print ('-----------------')
    # print(black_squares)
    # print('pos:',pos)


    # diff = len(black_squares)-previous_length
    # previous_length = len(black_squares)
    # if diff > 0 :
    #     sequence_as_str = sequence_as_str + ',+1'
    # else:
    #     sequence_as_str = sequence_as_str + ',-1'




# print (sequence_as_str)
# print (sequence_as_str[-3*50:])

# last_pattern = sequence_as_str[-3*50:]
#
# last_index = 0
# while last_index != -1:
#     last_index = sequence_as_str.find(last_pattern,last_index+1)
#     print(last_index)


def find_num_of_squares(n):
    base = modolu_312[n%312]
    steps = (n-base[0]) / 312
    diff = steps * 36
    n_len = diff + base[1]
    return n_len

# 29952	3020

# 69993	7641
# 69994	7640
# 69995	7639
# 69996	7640
# 69997	7639
# 69998	7638
# 69999	7639



print(29952,find_num_of_squares(29952))

print(69993,find_num_of_squares(69993))
print(69994,find_num_of_squares(69994))
print(69995,find_num_of_squares(69995))
print(69996,find_num_of_squares(69996))
print(69997,find_num_of_squares(69997))
print(69998,find_num_of_squares(69998))
print(69999,find_num_of_squares(69999))

print(format(int(find_num_of_squares(pow(10,18))),'d'))
