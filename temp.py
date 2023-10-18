from time import sleep
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import math


def hexagon_vertices(x, y, size):
    angles = np.linspace(0, 2 * np.pi, 7)
    return x + size * np.cos(angles), y + size * np.sin(angles)


def draw_hexagon(center_x, center_y, size, color, alpha=0.25):
    x, y = hexagon_vertices(center_x, center_y, size)
    return plt.fill(x, y, color=color, edgecolor='black', linewidth=0.5, alpha=alpha)


def connect_centers(centers, ax):
    triangles = []
    for i, center1 in enumerate(centers):
        for j, center2 in enumerate(centers):
            distance = math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
            if 15 < distance < 20.1:
                triangle = plt.Polygon([[0, 0], center1, center2], visible=False)
                ax.add_patch(triangle)
                triangles.append(triangle)
    return triangles


def on_click(event):
    global triangles, ax

    for triangle in triangles:
        if triangle.contains_point([event.xdata, event.ydata]):
            # Get the two centers of the triangle
            center1, center2 = triangle.get_xy()[1:]
            # Calculate the center of the corresponding hexagon
            center_hex = ((center1[0] + center2[0]) / 2, (center1[1] + center2[1]) / 2)

            # Find the corresponding hexagon
            for hexagon in hexagons:
                if np.isclose(hexagon.get_xy()[0], center_hex, rtol=1e-05).all():
                    # Change the color of the clicked hexagon
                    new_color = 'red' if hexagon.get_facecolor()[0] == 0 else 'blue'
                    hexagon.set_color(new_color)
                    hexagon.set_alpha(0.25)
                    ax.figure.canvas.draw()
                    break


def main():
    global hexagons, triangles, ax

    fig, ax = plt.subplots()

    centers = []
    for i in range(0, 10):
        for j in range(0, 10):
            centerx = i * (20 - 10 * math.cos(math.pi / 3))
            centery = j * 20 * math.sin(math.pi / 3) if (i % 2 == 0) else (j * 20 * math.sin(
                math.pi / 3)) + 10 * math.sin(math.pi / 3)
            centers.append((centerx, centery))

    hexagons = [draw_hexagon(center[0], center[1], 10, 'blue')[0] for center in centers]
    triangles = connect_centers(centers, ax)

    ax.set_aspect('equal')
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()


main()
