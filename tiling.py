from time import sleep

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
import math

def hexagon_triangles_vertices(x, y, size):
    angles = np.linspace(0, 2 * np.pi, 7)
    hexagon_triangles = []
    for i in range(len(angles)):
        hexagon_triangles.append(
            {
                'x': [x, x + size * np.cos(angles[i]), x + size * np.cos(angles[(i+1)%len(angles)])],
                'y': [y, y + size * np.sin(angles[i]), y + size * np.sin(angles[(i+1)%len(angles)])]
            }
        )
    return hexagon_triangles

def draw_hexagon(center_x, center_y, size, color, alpha=0.25):
    polygons = []
    hexagon_triangles = hexagon_triangles_vertices(center_x, center_y, size)
    for triangle in hexagon_triangles:
        print(triangle)
        polygons.append( plt.fill(triangle['x'],triangle['y'], color=color, edgecolor='black', linewidth=0.5, alpha=alpha) )
    return polygons

def connect_centers(centers, ax):
    for i, center1 in enumerate(centers):
        for j, center2 in enumerate(centers):
            distance = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
            if 15 < distance < 20.1:
                ax.plot([center1[0], center2[0]], [center1[1], center2[1]], 'k-', linewidth=0.5)


def on_click(event):
    global hexagons, ax

    # Find the hexagon that was clicked
    for index, hexagon in enumerate(hexagons):
        if hexagon.contains(event)[0]:
            # Change the color of the clicked hexagon
            new_color = 'red' if hexagon.get_facecolor()[0] == 0 else 'blue'
            hexagon.set_color(new_color)
            hexagon.set_alpha(0.25)
            ax.figure.canvas.draw()

def main():
    global hexagons, ax

    fig, ax = plt.subplots()

    centers = []
    for i in range(0, 10):
        for j in range(0, 10):
            centerx = i * (20 - 10 * math.cos(math.pi / 3))
            centery = j * 20 * math.sin(math.pi / 3) if (i % 2 == 0) else (j * 20 * math.sin(math.pi / 3)) + 10 * math.sin(math.pi / 3)
            centers.append((centerx, centery))
    centers = [(0,0)]
    hexagons = []
    for center in centers:
        hexagons += draw_hexagon(center[0], center[1], 10, 'blue')[0]
    # connect_centers(centers, ax)

    ax.set_aspect('equal')

    # Connect the on_click function to the button_press_event
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()

main()
