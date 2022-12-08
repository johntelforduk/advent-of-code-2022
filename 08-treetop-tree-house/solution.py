# Solution to day 8 of AOC 2022,
# https://adventofcode.com/2022/day/8

import matplotlib.pyplot as plt

f = open('input.txt')
t = f.read()
f.close()

max_x, max_y = 0, 0
grid, x, y = {}, 0, 0

for l in t.split('\n'):
    max_y = max(y, max_y)
    for t in l:
        max_x = max(x, max_x)
        h = int(t)
        grid[(x, y)] = h
        x += 1
    x = 0
    y += 1

assert max_x == max_y

print(max_x, max_y)
print(grid)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.set_xlim3d(-0.5, 0.5 + max_x)
ax.set_ylim3d(-0.5, 0.5 + max_y)

part1 = 0
for x in range(max_x + 1):
    for y in range(max_y + 1):

        h = grid[(x, y)]

        blockers = set()
        if x not in [0, max_y] and y not in [0, max_y]:
            for check in range(max_x + 1):
                # print(x, y, h, check)

                if grid[(x, check)] >= h:    # Blocker on y axis.
                    if check < y:
                        blockers.add('south')
                    elif check > y:
                        blockers.add('north')
                if grid[(check, y)] >= h:    # Blocker on x axis.
                    if check < x:
                        blockers.add('west')
                    elif check > x:
                        blockers.add('east')

        if len(blockers) == 4:      # north + south + east + west == 4 blockers
            col = 'green'
        else:
            part1 += 1
            col = 'red'

        ax.bar3d(x, y, 0, 0.5, 0.5, h, color=col)

print(part1)

plt.gca().invert_xaxis()
plt.show()
