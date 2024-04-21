
import math
class NavigationMesh:
    def add_mesh (self, vertices, triangles):
        pass
    def get_distance (self, start, end):
        return 0

if __name__ == "__main__":
    vertices_array = [
        {1: [0, 0, 0]},
        {2: [0, 1, 0]},
        {3: [0, 0, 1]},
        {4: [0, 1, 1]}
        ,
        {5: [1, 0, 0]},
        {6: [1, 1, 0]},
        {7: [1, 0, 1]},
        {8: [1, 1, 1]},
    ]
    triangles_array = [
        [1, 2, 3], #down
        [2, 3, 4], #down

        [5,6,7],  # up
        [6,7,8],  # up

        [1,2,5],  # front
        [2,5,6],  # front

        [3,4,7],  # back
        [4,7,8],  # back

        [1,3,5],  # left
        [3,5,7],  # left

        [2,4,6],  # right
        [4,6,8],  # right
    ]

    N = NavigationMesh()
    N.add_mesh(vertices_array, triangles_array)
    d = N.get_distance( [0,0,0],[1,1,1])
    assert abs(d - (math.sqrt(2) + 1)) < 0.0001