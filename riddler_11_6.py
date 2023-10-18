import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
import math


plt.gca().set_aspect('equal', adjustable='box')
points_to_reflect = []
points_dict = set()
# alpha = math.pi / 36
alpha = 1

def get_point_key(p):
    return "_" + str(p[0]) + "_" + str(p[1])

def plot_point(p, style= 'bo'):
    plot(p[0], p[1], style)

def register_point(p):
    if get_point_key(p) in points_dict:
        print (get_point_key(p) + " already painted")
    else:
        points_to_reflect.append(p)
        points_dict.add(get_point_key(p))

def reflect_point(type, p):
    if type == 1:
        ret = (p[0],-1*p[1])
        return ret
    else:
        if p[0] > 0:
            beta = math.atan(p[1]/p[0])
        else :
            beta = math.atan(p[1]/p[0]) + math.pi

        r = math.sin(beta-alpha) * math.sqrt(p[0]*p[0] + p[1]*p[1])
        stepx =  r * math.sin(alpha)
        stepy =  r * math.cos(alpha)
        ret = ( p[0] + 2 * stepx , p[1] - 2 * stepy )
        return ret

plot([-100,100],[0,0])
# plot([0,0],[-100,100])
plot([-50,50],[-50*math.tan(alpha),50*math.tan(alpha)])

# plot_point( ( 100/math.atan(alpha),100) )


# register_point( (25,-25) )
# register_point( (40,-100) )
# register_point( (10,10) )
# register_point( (30,90) )

register_point( (10,50) )
register_point( (10,100) )
# register_point( (10,30) )
# register_point( (-23,10) )
# register_point( (-50,50) )
# register_point( (-30,-15) )
# register_point( (-20,-50) )
# register_point( (20,-30) )

for i in range(0,1000):
    p = points_to_reflect.pop(0) if len(points_to_reflect) > 0 else None
    if p is None: break
    plot_point(p)
    p_reflected1 = reflect_point(1, p)
    plot_point(p_reflected1)
    register_point(p_reflected1)
    p_reflected2 = reflect_point(2, p)
    plot_point(p_reflected2)
    # plot([p[0],p_reflected2[0]], [p[1],p_reflected2[1]] )
    register_point(p_reflected2)




plt.show()