

from numpy import genfromtxt


EPSILON = 0.00001

ONLY_INTERIOR = False


def isBetween(a, b, c):
    crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > EPSILON:
        return False

    dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
    if dotproduct < 0:
        return False

    squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
    if dotproduct > squaredlengthba:
        return False

    return True




def do_segments_intersect( p0_x,  p0_y,  p1_x,  p1_y, p2_x,  p2_y,  p3_x,  p3_y):

    s1_x = p1_x - p0_x
    s1_y = p1_y - p0_y
    s2_x = p3_x - p2_x
    s2_y = p3_y - p2_y

    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
    t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)

    ret = False
    if ONLY_INTERIOR:
        if (s > 0 and s < 1 and t > 0 and t < 1) :
            ret = True
    else:
        if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
            ret = True

    # print ('{},{},{},{},{},{},{},{} => {}'.format(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y,ret))
    return ret,s,t




def does_contain_origin1(a,b,c):
    global ONLY_INTERIOR

    if isBetween(a,b,(0,0)) or isBetween(a,c,(0,0)) or isBetween(b,c,(0,0)) :
        if ONLY_INTERIOR:
            ret = False # origin is on one of the edges
        else:
            ret = True
    else :
        intersect1 = do_segments_intersect(0,0,a[0],a[1], b[0],b[1],c[0],c[1] )
        intersect2 = do_segments_intersect(0,0,b[0],b[1], a[0],a[1],c[0],c[1] )
        intersect3 = do_segments_intersect(0,0,c[0],c[1], b[0],b[1],a[0],a[1] )

        ret = not intersect1 and not intersect2 and not intersect3
        # print("({},{}),({},{}),({},{}) yields: {},{},{} => {}".format(
        #     a[0],a[1],b[0],b[1],c[0],c[1],intersect1,intersect2,intersect3,ret))

    return ret


def does_contain_origin(x,y,z):
    # line that passes through x & (0,0)
    # y = ax + b => b=0, a=x[1]/x[2]
    a = x[0]/x[1]

    out_of_bounds_point = (1001,1000*a)
    res = do_segments_intersect(x[0],x[1],out_of_bounds_point[0],out_of_bounds_point[1],y[0],y[1],z[0],z[1])

    return res



# assert does_contain_origin( (1,1), (0.1,10), (10,0.1) ) == False
#
# assert does_contain_origin( (-10,0), (10,0), (0,-10) ) == True
#
# assert do_segments_intersect(0,0,0,10,-5,5,5,5) == True
# assert do_segments_intersect(0,0,0,10,-5,11,5,11) == False
#
# assert do_segments_intersect(0,0,0,10,-5,10,5,10) == True
#
# assert do_segments_intersect(0,0,0,-10,-10,0,10,0) == True
#
#
# assert does_contain_origin( (-340,495), (-153,-910), (835,-947) ) == True
# assert does_contain_origin( (-175,41), (-421,-714), (574,-645) ) == False
# assert does_contain_origin( (-10,0), (10,1), (0,10) ) == False
# assert does_contain_origin( (-10,0), (10,1), (0,-10) ) == True




path = './p102_triangles.txt'
# path = 'C:/Users/hedbn/PycharmProjects/misc/p102_triangles_test.txt'
my_data = genfromtxt(path, delimiter=',')

my_data = [
    [-4,-4,-1,-4,-4,-1],
    [-6,-2,-1,-4,-4,-1]
]


sum = 0
for i,line in enumerate(my_data):
    is_contain_origin = does_contain_origin( (line[0], line[1]) , (line[2], line[3]) , (line[4], line[5]))
    print(i,line,is_contain_origin)
    if is_contain_origin:
        sum += 1
print (sum)



