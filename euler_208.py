

d = [None,None,None,None,None]

d[0] = [0.951056516,    -0.690983006,	-0.951056516,	-0.690983006	]
d[1] = [-0.363271264,   -1.118033989,	-0.951056516,	0.690983006	    ]
d[2] = [-1.175570505,   0,		        0.363271264,	1.118033989	    ]
d[3] = [-0.363271264,   1.118033989,	1.175570505,	0		        ]
d[4] = [0.951056516,    0.690983006,	0.363271264,	-1.118033989	    ]



def is_at_start(pos,x,y,):

    return (pos == 0 and abs(x) < 0.0001 and abs(y) < 0.0001)




def calc_position( moves_in_num ):

    moves = list('{0:b}'.format(moves_in_num))[1:]

    pos = x = y =0

    for step in moves:
        if step == 1:
            x += d[pos][0]
            y += d[pos][1]
            pos = (pos+1) % 5
        else:
            x += d[pos][2]
            y += d[pos][3]
            pos = (pos - 1) % 5

    # return moves_in_num,moves,pos,x,y, is_at_start(pos,x,y)
    return is_at_start(pos,x,y)

sum = 0
for i in range(1,pow(2,25)):
    if calc_position(i):
        sum += 1

print(sum)

