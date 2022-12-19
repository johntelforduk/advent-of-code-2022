# Solution to day 18 of AOC 2022,
# https://adventofcode.com/2022/day/18

import structlog
from itertools import combinations

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

f = open('test2.txt')
t = f.read()
f.close()

cubes = []
for line in t.split('\n'):
    cube = [int(term) for term in line.split(',')]
    cubes.append((cube[0], cube[1], cube[2]))

print(cubes)

touchers = 0
for c1, c2 in combinations(cubes, 2):
    # print(c1, c2)
    if touching(c1, c2):
        touchers += 1





print('Part 1:', len(cubes) * 6 - 2 * touchers)

min_x, max_x, min_y, max_y, min_z, max_z = 100000, -100000, 100000, -100000, 100000, -100000
for x, y, z in cubes:
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)

print(min_x, max_x, min_y, max_y, min_z, max_z)
