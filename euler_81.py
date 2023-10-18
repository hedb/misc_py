

import heapq
import sys
from functools import total_ordering
import csv

cell_values = []

with open('p081_matrix.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        cell_values.append(row)

# print(cell_values)
# exit()
#
# cell_values = \
#     [
#     [131, 673, 234, 103, 18],
#     [201, 96, 342, 965, 150],
#     [630, 803, 746, 422, 111],
#     [537, 699, 497, 121, 956],
#     [805, 732, 524, 37, 331]
#     ]


MAT_LEN = len(cell_values)

input_matrix =  [    [0 for j in range(0,MAT_LEN)]      for i in range(0,MAT_LEN)]


heap = []


@total_ordering
class Node:
    weight = 0
    val = 0
    x = 0
    y = 0
    from_x = 0
    from_y = 0
    def __init__(self, weight, val,x,y,from_x, from_y):
        self.weight = weight
        self.val = val
        self.x = x
        self.y = y
        self.from_x = from_x
        self.from_y = from_y

    def __lt__(self, other):
        return self.weight  < other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __str__(self):
        return "w:{} v:{} ({},{}) from({},{})".format(self.weight, self.val, self.x, self.y, self.from_x, self.from_y)

for i in range(0,MAT_LEN):
    for j in range(0,MAT_LEN):
        weight = cell_values[0][0] if (i == 0 and j == 0) else sys.maxsize

        n = Node(weight,cell_values[i][j],j,i, None, None)
        heapq.heappush( heap, n )
        input_matrix[j][i] = n



while len(heap) > 0:
    current = heapq.heappop(heap)
    if (current.x < MAT_LEN-1):
        n = input_matrix[current.x+1][current.y]
        if (n.weight > current.weight + n.val):
            n.weight = current.weight + n.val
            n.from_x = current.x
            n.from_y = current.y

    if (current.y < MAT_LEN-1):
        n = input_matrix[current.x][current.y+1]
        if (n.weight > current.weight + n.val):
            n.weight = current.weight + n.val
            n.from_x = current.x
            n.from_y = current.y


    heapq.heapify(heap) # doesn't affect the immutable items in the heap

    if (current.x == MAT_LEN-1 and current.y == MAT_LEN-1):
        break


for i in range(0,MAT_LEN):
    for j in range(0,MAT_LEN):
        print (input_matrix[i][j])





