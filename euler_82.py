
import heapq
import sys
from functools import total_ordering
import time

from recordclass import recordclass

import csv

from enum import Enum     # for enum34, or the stdlib version




Edge = recordclass("Edge",('x','y','direction'),defaults=(None,)*3)
Direction = Enum('Direction', 'up down right')


cell_values = []
MATRIX_DIM = 0
iteration_number = 0



Stack = []
Min_path_so_far = []


resolve_path_steps = []
path_steps_enumerating = []


def open_path_possibilties():
    while len(path_steps_enumerating) > 0 :
        edge = path_steps_enumerating.pop(0)
        if edge.x < MATRIX_DIM-1:
            path_steps_enumerating.append(Edge(edge.x+1,edge.y,Direction.right))
        if edge.y < MATRIX_DIM-1 and edge.direction != Direction.up:
            path_steps_enumerating.append(Edge(edge.x,edge.y+1,Direction.down))
        resolve_path_steps.append(edge)




def find_min_path(x,y,sum_so_far = 0,direction=0):
    global iteration_number,MATRIX_DIM
    iteration_number +=1


    if x == MATRIX_DIM-1:
        return sum_so_far + cell_values[x][y]

    sum_path_up = find_min_path(x,y-1,sum_so_far+cell_values[x][y],-1) if y>0 and direction!=1 else 10**20
    sum_path_down = find_min_path(x,y+1,sum_so_far+cell_values[x][y],1) if y<MATRIX_DIM-1 and direction!=-1 else 10**20
    sum_path_right = find_min_path(x+1,y,sum_so_far+cell_values[x][y],0) # protected from first step

    real_min = min(sum_path_down,sum_path_right,sum_path_up)

    return real_min



def find_recursive():
    global total_min_path
    for i in range(0,len(cell_values)):
        #min_sum = find_min_path(0,i,0)
        min_sum = find_min_path(0,i)
        if min_sum < total_min_path:
            total_min_path = min_sum

    print(total_min_path)
    print(iteration_number)


with open('p082_matrix.txt') as csv_file:
# with open('p_082_example.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        cell_values.append(row)

total_min_path = 10**20

MATRIX_DIM = len(cell_values)
Min_path_so_far = [[0 for i in range(MATRIX_DIM)] for j in range(MATRIX_DIM)]


# find_recursive()

for i in range(30):
    resolve_path_steps = []
    resolve_path_steps = []
    path_steps_enumerating.append( Edge(0, 0, Direction.right) )
    MATRIX_DIM = i
    now = time.time()
    open_path_possibilties()
    print(i,len(resolve_path_steps), time.time()-now)