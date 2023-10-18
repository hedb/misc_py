import numpy as np
import matplotlib
import platform
import matplotlib.pyplot as plt
import random
from scipy.interpolate import CubicSpline
from matplotlib.widgets import Button
from matplotlib.patches import Polygon


if platform.system() == 'Linux':
    matplotlib.use('Qt5Agg')
else:
    matplotlib.use('TkAgg')

# Generate random points
x = [0] + sorted(random.sample(range(1, 200), 3)) + [200]
y = [50] + random.sample(range(0, 200), 3) + [150]

# Create cubic spline interpolation
cs = CubicSpline(x, y)

# Generate smooth path
x_smooth = np.arange(0, 200, 0.1)
y_smooth = cs(x_smooth)

# Create a plot
fig, ax = plt.subplots()
ax.plot(x_smooth, y_smooth)

def add_car(ax, cs, x_smooth, y_smooth, width, height):
    # Generate random coordinates for the lower left corner of the rectangle
    x = random.randint(0, 200 - width)
    y = random.randint(0, 200 - height)

    # Calculate the position of the car relative to the path at the car's x-coordinate
    intersection_index = np.argmax(x_smooth >= x)
    position_relative_to_path = y + height / 2 - y_smooth[intersection_index]

    # Create a trapezoid with the wide base oriented towards the line based on the position relative to the path
    if position_relative_to_path > 0:
        trapezoid_points = [(x, y), (x + width, y), (x + width * 0.75, y + height), (x + width * 0.25, y + height)]
        ray_start_y = y
    else:
        trapezoid_points = [(x, y + height), (x + width, y + height), (x + width * 0.75, y), (x + width * 0.25, y)]
        ray_start_y = y + height

    trapezoid = Polygon(trapezoid_points, edgecolor='black', facecolor='none')
    ax.add_patch(trapezoid)


    # Find the intersection of the ray (aligned with the car body) with the smooth path
    intersection_index = np.argmax(x_smooth >= x)

    # Calculate the distance between the car's left edge and the intersection point
    intersection_x, intersection_y = x_smooth[intersection_index], y_smooth[intersection_index]
    distance = np.sqrt((intersection_x - x) ** 2 + (intersection_y - (y + height / 2)) ** 2)

    # Display the distance on the left side of the car
    distance_text = ax.text(x - 30, y + height / 2, f"{distance:.2f}", fontsize=10, color='blue', verticalalignment='center')

    # Plot the directed ray line using a distinct line
    ray_line = ax.plot([x, intersection_x], [ray_start_y, intersection_y], linestyle='--', color='green', linewidth=1.5)[0]


    # Append the car, text, and ray line to the car_artists list
    car_artists.extend([trapezoid, distance_text, ray_line])

car_artists = []

# Function to randomize a car
def randomize_car(event):
    # Clear the car_artists list
    for artist in car_artists:
        artist.remove()
    car_artists.clear()

    # Randomize a new car
    add_car(ax, cs, x_smooth, y_smooth, 5, 20)

    # Redraw the canvas
    fig.canvas.draw_idle()

# Add the initial car
randomize_car(None)

# Add a button for randomizing a new car
button_axes = plt.axes([0.8, 0.05, 0.1, 0.075])
button = Button(button_axes, 'Randomize Car', color='lightgray', hovercolor='0.975')
button.on_clicked(randomize_car)



# Configure the fullscreen setting based on the backend
if matplotlib.get_backend() == 'TkAgg':
    manager = plt.get_current_fig_manager()
    if platform.system() == 'Windows':
        manager.window.state('zoomed')
    elif platform.system() == 'Darwin':  # Mac OS
        manager.window.attributes('-fullscreen', True)
elif matplotlib.get_backend() == 'Qt5Agg':
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()


# Display the plot
plt.show()
