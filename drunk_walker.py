import random
import math


def main():
    NUM_OF_RUNS = 100
    N = 1000*100

    for directions in range(2,20):
        avg_distance = calc_distance_per_direction_no(directions, N, NUM_OF_RUNS)
        print('{directions} : {avg_distance}'.format(directions=directions,avg_distance=avg_distance))


def calc_distance_per_direction_no(DIRECTIONS, N, NUM_OF_RUNS):
    UNIT_ANGLE = 2 * math.pi / DIRECTIONS
    sum_distances = 0
    for i in range(NUM_OF_RUNS):
        distance, x, y = calc_distance(DIRECTIONS, N, UNIT_ANGLE)
        sum_distances += distance
    return sum_distances/NUM_OF_RUNS


def calc_distance(DIRECTIONS, N, UNIT_ANGLE):
    x = y = 0
    for i in range(N):
        direction = random.randint(0, DIRECTIONS-1)
        alpha = direction * UNIT_ANGLE
        dx = math.cos(alpha)
        dy = math.sin(alpha)
        # print('{dx},{dy}'.format(dx=dx,dy=dy))
        x = x + dx
        y = y + dy
        # print('{x},{y}'.format(x=x, y=y))
    distance = math.sqrt(x * x + y * y)
    return distance,x,y


if __name__ == "__main__":
    main()
