import math
import random
import matplotlib.pyplot as plt

NUM_OF_VERTICES = 1000
ALLOWED_DISTANCE = 1
FRAME = 1.5

# vertices = [(0,0)]
# vertices = [(0,0), (1,0)]
# vertices = [(0,0), (0,1)]
vertices = [(0,0), (0,1), (0.86602540378443864676372317075294,0.5)]

def add_new_vertice(vertices):
    candidate_approved = False
    candidate = None
    while not candidate_approved:
        origin_vertice = vertices[random.randint(0,len(vertices)-1)]
        candidate = (
            origin_vertice[0] + (random.random()*2-1)*ALLOWED_DISTANCE,
            origin_vertice[1] + (random.random()*2-1)*ALLOWED_DISTANCE
        )
        candidate_approved = True
        for v in vertices:
            if (math.pow(v[0]-candidate[0],2) + math.pow(v[1]-candidate[1],2)) > math.pow(ALLOWED_DISTANCE,2):
                candidate_approved = False;
                break;
    return candidate



for i in range(1,NUM_OF_VERTICES+1):
    vertices.append(add_new_vertice(vertices))



fig = plt.figure()
ax = fig.add_subplot(111)

print(vertices)

ax.scatter(FRAME,FRAME, color = 'r')
ax.scatter(-1*FRAME,FRAME, color = 'r')
ax.scatter(-1*FRAME,-1*FRAME, color = 'r')
ax.scatter(FRAME,-1*FRAME, color = 'r')

for v in vertices:
    # plt.plot(vertices[1][0],vertices[1][1], linestyle='--')
    ax.scatter(v[0],v[1], color = 'b')



plt.show()