# Solution to day 18 of AOC 2022,
# https://adventofcode.com/2022/day/18

import structlog
from itertools import combinations
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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


def touching(c1, c2):
    x1, y1, z1 = c1
    x2, y2, z2 = c2
    return (abs(x1 - x2) == 1 and y1 == y2 and z1 == z2
            or x1 == x2 and abs(y1 - y2) == 1 and z1 == z2
            or x1 == x2 and y1 == y2 and abs(z1 - z2) == 1)

assert touching((1, 1, 1), (2, 1, 1)) is True
assert touching((1, 2, 1), (1, 1, 1)) is True
assert touching((1, 1, 1), (1, 1, 0)) is True
assert touching((1, 1, 1), (1, 2, 2)) is False


def escape(cs: set, c, tried: set):
    """Return True if there is a path from the parm cell to escape from the droplet, without visiting one of the
    previously tried cells. Otherwise return False."""
    x, y, z = c

    # We've escaped!
    if (x < min_x or x > max_x
        or y < min_y or y > max_y
        or z < min_z or z > max_z):
        return True

    # We hit a wall.
    if (x, y, z) in cs:
        return False

    # Attempt escape in all possible directions.
    for dx, dy, dz in [(-1, 0, 0), (0, -1, 0), (0, 0, -1),
                       (1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        new_x, new_y, new_z = x + dx, y + dy, z + dz
        if (new_x, new_y, new_z) not in tried:
            tried.add((new_x, new_y, new_z))
            if escape(cs, c=(x + dx, y + dy, z + dz), tried=tried):
                return True

    # No escape.
    return False


def inside(cs: set, c) -> bool:
    """Return True if the parm coordinate is an empty cell inside the droplet. Otherwise return False."""
    if c in cs:
        return False
    return escape(cs=cs, c=c, tried=set()) is False


f = open('input.txt')
t = f.read()
f.close()

cubes = set()
for line in t.split('\n'):
    cube = [int(term) for term in line.split(',')]
    cubes.add((cube[0], cube[1], cube[2]))

print(cubes)

def approx_surface_area(cs: set) -> int:
    touchers = 0
    for c1, c2 in combinations(cs, 2):
        if touching(c1, c2):
            touchers += 1
    return len(cs) * 6 - 2 * touchers


def plot(cs_out: set, cs_in):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Vertices of a cube.
    # ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
    colours = ['black', 'white']
    alphas = [0.03, 1]
    pair = [cs_out, cs_in]
    i = 0
    for cs in pair:
        for x, y, z in cs:
            v = np.array([[x, y, z], [x + 1, y, z], [x + 1, y + 1, z], [x, y + 1, z],
                          [x, y, z + 1], [x + 1, y, z + 1], [x + 1, y + 1, z + 1], [x, y + 1, z + 1]])

            ax.scatter3D(v[:, 0], v[:, 0], v[:, 0], s=0)  # Needed to set the bounds of the plotting space.

            faces = [[v[0], v[1], v[2], v[3]],
                     [v[4], v[5], v[6], v[7]],
                     [v[1], v[5], v[6], v[2]],
                     [v[0], v[4], v[7], v[3]],
                     [v[3], v[2], v[6], v[7]],
                     [v[0], v[1], v[5], v[4]]]


            # Plot faces.
            ax.add_collection3d(Poly3DCollection(faces,
                                                 facecolors=colours[i], linewidths=0.1, edgecolors=colours[i], alpha=alphas[i]))
        i += 1

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


print('Part 1:', approx_surface_area(cs=cubes))

min_x, max_x, min_y, max_y, min_z, max_z = 100000, -100000, 100000, -100000, 100000, -100000
for x, y, z in cubes:
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)

print(min_x, max_x, min_y, max_y, min_z, max_z)


# print(inside(cs=cubes, c=(2, 2, 5)))

insiders = set()
for x in range(min_x - 1, max_x + 1):
    for y in range(min_y - 1, max_y + 1):
        for z in range(min_z - 1, max_z + 1):
            if inside(cs=cubes, c=(x, y, z)):
                insiders.add((x, y, z))

print(insiders)
print(approx_surface_area(insiders))

print('Part 2:', approx_surface_area(cs=cubes) - approx_surface_area(insiders))

plot(cs_out=cubes, cs_in=insiders)
