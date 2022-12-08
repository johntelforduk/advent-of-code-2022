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

part1, part2 = 0, 0
for x in range(max_x + 1):
    for y in range(max_y + 1):

        h = grid[(x, y)]

        blockers = set()

        deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        best_dist = [0, 0, 0, 0]
        done = [False, False, False, False]

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

                if check != 0:
                    for d in range(len(deltas)):
                        if not done[d]:
                            dx, dy = deltas[d]
                            tx, ty = x + check * dx, y + check * dy

                            if (tx, ty) in grid:
                                best_dist[d] = check
                                if grid[(tx, ty)] >= h:
                                    done[d] = True

        # print(x, y, best_dist)

        multi = 1
        for a in best_dist:
            multi *= a
        part2 = max(part2, multi)

        if len(blockers) == 4:      # north + south + east + west == 4 blockers
            col = 'green'
        else:
            part1 += 1
            col = 'red'

        ax.bar3d(x, y, 0, 0.5, 0.5, h, color=col)

print('Part 1:', part1)
print('Part 2:', part2)

plt.gca().invert_xaxis()
plt.show()
