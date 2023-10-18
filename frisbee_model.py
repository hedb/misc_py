import numpy as np
import matplotlib.pyplot as plt
import math



def init_global_vars():
    global vy_stamp, vx_stamp, t_stamp, ax_stamp, x_stamp, y_stamp, ALPHA_stamp, ay_stamp
    vy_stamp = []
    vx_stamp = []
    t_stamp = []
    ax_stamp = []
    x_stamp = []
    y_stamp = []
    ALPHA_stamp = []
    ay_stamp = []

def simulation_handler(vy=0, vx=0, frisbee_angle=0, dt=1, time_to_run = 1, y = 0, is_visualize = False):
    global vy_stamp, vx_stamp, t_stamp, ax_stamp, x_stamp, y_stamp, ALPHA_stamp, ay_stamp
    init_global_vars()
    # define constants
    m = 0.175
    p = 1.23
    AREA = 0.0568
    CL0 = 0.1
    CLA = 1.4
    CD0 = 0.08
    CDA = 2.72
    ALPHA0 = -4
    g = -9.81
    ax_Func = lambda: -p * AREA / 2 * (pow(vx,2)*Cd+pow(vy,2)*Cl) / m
    ay_Func = lambda: p * AREA / 2 * (pow(vx,2)*Cl-pow(vy,2)*Cd) / m+g
    ay = 0
    ax = 0
    x = 0
    t = -dt
    while y >= 0:
        t += dt
        if(pow(vx,2) + pow(vy,2)  != 0):
            Teta = math.acos(vx/pow(pow(vx,2) + pow(vy,2), 0.5))*((vy>0)*2-1)
        else:
            Teta = math.pi*((vy>0)*2-1)
        ALPHA = frisbee_angle - Teta
        Cl = CL0 + CLA * ALPHA * math.pi / 180
        Cd = CD0 + CDA * pow((ALPHA - ALPHA0) * math.pi / 180, 2)
        ax = ax_Func()
        ay = ay_Func()
        appendItems(ax, ay, y, x, vy, vx, t,ALPHA)
        vx = vx + ax * dt
        vy = vy + ay * dt
        x = x + vx * dt
        y = y + vy * dt
        if(ax>0):
            print(Cd)
            print(Cl)
            print(vx)
            print(vy)
        if(t>time_to_run):
            break
        #print(x,y,ax,ay)
    # fig, ax = plt.subplots()
    # plt.figure(1,[10.0, 10.0])
    # plt.plot(x_stamp, y_stamp)
    # plt.ylim(-0.02,np.amax(np.array(x_stamp)/6+0.02))
    # ax.plot(x_stamp,y_stamp)
    # ratio = 1.0
    # x_left, x_right = ax.get_xlim()
    # y_low, y_high = ax.get_ylim()
    # ax.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)
    if is_visualize:
        plt.show()
        plt.plot(x_stamp,y_stamp)
        plt.show()


def appendItems(ax, ay, y, x, vy, vx, t, ALPHA):
    global vy_stamp, vx_stamp, t_stamp, ax_stamp, x_stamp, y_stamp, ALPHA_stamp, ay_stamp
    ax_stamp.append(ax)
    ay_stamp.append(ay)
    y_stamp.append(y)
    x_stamp.append(x)
    vy_stamp.append(vy)
    vx_stamp.append(vx)
    t_stamp.append(t)
    ALPHA_stamp.append(ALPHA)


simulation_handler(vy=0, vx=0, frisbee_angle = 0, dt = 1, time_to_run=2, y=10, is_visualize=False)
print(y_stamp)
assert y_stamp[1]>0.2, '\n --- Dropping the frisbee it should fall but with some air resistence. Height should be more than 0.2'

# simulation_handler(3, 14, 30/180*math.pi, dt = 0.01, time_to_run=100,y=0, is_visualize=True)