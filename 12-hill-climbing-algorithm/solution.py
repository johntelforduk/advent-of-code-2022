# Solution to day 12 of AOC 2022
# https://adventofcode.com/2022/day/12

import sys
import structlog
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

structlog.configure(
    processors=[
        # Add callsite parameters.
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),

        # Render the final event dict as JSON.
        structlog.dev.ConsoleRenderer()
    ]
)

log = structlog.get_logger()


f = open('input.txt')
t = f.read()
f.close()

grid, source, target = {}, (0, 0), (0, 0)

z = []
grid_x, grid_y = 0, 0
for row in t.split('\n'):
    grid_x = 0
    x_list = []
    for elevation in row:
        if elevation == 'S':
            grid[grid_x, grid_y] = 'a'
            source = (grid_x, grid_y)
        elif elevation == 'E':
            grid[grid_x, grid_y] = 'z'
            target = (grid_x, grid_y)
        else:
            grid[grid_x, grid_y] = elevation

        x_list.append(ord(grid[grid_x, grid_y]) - ord('a') + 1)
        grid_x += 1
    grid_y += 1
    z.append(x_list)

print(z)

# Fix a gatepost error.
# grid_x -= 1
# grid_y -= 1

log.info('Grid loaded',
         grid_x=grid_x,
         grid_y=grid_y,
         source=source,
         target=target)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = np.arange(0, grid_x)
Y = np.arange(0, grid_y)
X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)

# z = [[1, 2, 1], [4, 5, 6], [7, 8, 9]]
Z = np.array(z)
# Z = np.append(values=z, axis=0)
print(Z)


# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.summer,
                       linewidth=1, antialiased=False)

# Customize the z axis.
ax.set_zlim(0, 26)
ax.set_aspect('equal')
# ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
# ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()




# Implemented pseudo code from, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# function Dijkstra(Graph, source):
#
# create vertex set Q
q, dist, prev = {}, {}, {}
# for each vertex v in Graph:
for v in grid:
    # dist[v] ← INFINITY
    dist[v] = sys.maxsize
    # prev[v] ← UNDEFINED
    prev[v] = None
    # add v to Q
    q[v] = dist[v]
# dist[source] ← 0
dist[source] = 0
q[source] = 0

# while Q is not empty:
while len(q) != 0:

    print('len(q):', len(q))
    # u ← vertex in Q with min dist[u]
    u = min(q, key=q.get)

    # print('u, q[u]:', u, q[u])

    # remove u from Q
    del q[u]

    # for each neighbor v of u still in Q:
    x, y = u
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        v = (x + dx, y + dy)
        climbable = False
        if v in grid:
            elevation = ord(grid[v]) - ord(grid[u])
            climbable = (elevation <= 1)
            # print(v, elevation)

        # TODO v in q yes... but also, is there a path from u to v.
        if v in q and climbable:
            # print('v:', v)

            # print(v)
            # alt ← dist[u] + length(u, v)
            # alt = dist[u] + grid[v]
            # XXX All edges are length one in this graph!!!
            alt = dist[u] + 1


            # if alt < dist[v]:
            if alt < dist[v]:
                # dist[v] ← alt
                dist[v] = alt
                if v in q:
                    q[v] = alt
                # prev[v] ← u
                prev[v] = u

# return dist[], prev[]
print(dist[target])
