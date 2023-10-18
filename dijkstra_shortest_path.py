import sys
import csv


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.distance < other.distance
        return NotImplemented

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        if node in self.vert_dict:
            ret = self.vert_dict[node]
        else:
            self.num_vertices = self.num_vertices + 1
            ret = Vertex(node)
            self.vert_dict[node] = ret
        return ret

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        # self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous


def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


import heapq


def dijkstra(aGraph, start, target):
    print ('''Dijkstra's shortest path''')
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                print(
                    'updated : current = %s next = %s new_dist = %s' \
                    % (current.get_id(), next.get_id(), next.get_distance())
                )
            else:
                print (
                    'not updated : current = %s next = %s new_dist = %s' \
                    % (current.get_id(), next.get_id(), next.get_distance())
                )

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


def create_graph_from_matrix(matrix,problem):
    g = Graph()
    dim = len(matrix)

    g.add_vertex("start")

    for x in range(dim):
        for y in range(dim):
            vertex_id = "{}:{}".format(x,y)
            vertex_id_entrance = vertex_id + "_entrance"
            vertex_id_exit = vertex_id + "_exit"

            g.add_vertex(vertex_id_entrance)
            g.add_vertex(vertex_id_exit)
            g.add_edge(vertex_id_entrance, vertex_id_exit, matrix[x][y])

            if problem == 81:
                if x == 0 and y==0:
                    g.add_edge('start', vertex_id_entrance, 0)
                if x == dim - 1 and y == dim-1:
                    g.add_edge(vertex_id_exit,'end', 0)

                if x > 0:
                    g.add_edge("{}:{}".format(x-1,y) + "_exit",vertex_id_entrance, 0)
                if y > 0:
                    g.add_edge("{}:{}".format(x,y-1) + "_exit",vertex_id_entrance, 0)
            elif problem == 82:
                if x == 0:
                    g.add_edge('start', vertex_id_entrance, 0)
                if x == dim - 1:
                    g.add_edge(vertex_id_exit, 'end', 0)

                if x > 0:
                    g.add_edge("{}:{}".format(x - 1, y) + "_exit", vertex_id_entrance, 0)
                if y > 0:
                    g.add_edge("{}:{}".format(x, y - 1) + "_exit", vertex_id_entrance, 0)
                if y < dim-1:
                    g.add_edge("{}:{}".format(x,y+1) + "_exit",vertex_id_entrance, 0)
            elif problem == 83:
                if x == 0 and y==0:
                    g.add_edge('start', vertex_id_entrance, 0)
                if x == dim - 1 and y == dim-1:
                    g.add_edge(vertex_id_exit,'end', 0)

                if x > 0:
                    g.add_edge("{}:{}".format(x - 1, y) + "_exit", vertex_id_entrance, 0)
                if x < dim-1:
                    g.add_edge("{}:{}".format(x + 1, y) + "_exit", vertex_id_entrance, 0)
                if y > 0:
                    g.add_edge("{}:{}".format(x, y - 1) + "_exit", vertex_id_entrance, 0)
                if y < dim - 1:
                    g.add_edge("{}:{}".format(x, y + 1) + "_exit", vertex_id_entrance, 0)


    return g


def create_sample_graph():

    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'f', 14)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('d', 'e', 6)
    g.add_edge('e', 'f', 9)

    return g

def print_graph_data():
    print('Graph data:')
    for v in g:
        test = 1
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print(
                '( %s , %s, %3d)' % (vid, wid, v.get_weight(w))
            )

if __name__ == '__main__':

    cell_values = []


    with open('p083_matrix.txt') as csv_file:
    #with open('p082_matrix.txt') as csv_file:
    # with open('p081_matrix.txt') as csv_file:

    # with open('p_082_example.txt') as csv_file:
    # with open('p_081_example.txt') as csv_file:
    # with open('p_082_example2.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            cell_values.append(row)

    g = create_graph_from_matrix(cell_values,83)
    # g = create_sample_graph()

    print_graph_data()


    dijkstra(g, g.get_vertex('start'), g.get_vertex('end'))

    target = g.get_vertex('end')
    path = [target.get_id()]
    shortest(target, path)
    print ( 'The shortest path : %s' % (path[::-1]) )
    print ("distance is", target.distance)