import numpy as np
import matplotlib.pyplot as plt

# https://matplotlib.org/gallery/pie_and_polar_charts/polar_scatter.html
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)

# Option 1

# ax.plot(np.linspace(0, 1.5*np.pi, 10), np.ones(10)*5, color='b', linestyle=':')


# Option 2

N = 150
r = 2 * np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)
area = 200 * r**2
colors = theta
c = ax.scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)


plt.show()