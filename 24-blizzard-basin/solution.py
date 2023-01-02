# Solution to day 24 of AOC 2022,
# https://adventofcode.com/2022/day/24

import sys

# Key = Minute integer.
# Value = Dictionary, Keys = coordinates of 1 or more blizzards, Value = String of blizzard directions.
BLIZZARD_MINS = {}

RIGHT, BOTTOM = 0, 0            # Edges of the basin.
LINES = []                      # Used for rendering of the basin.
HOME = (1, 0)
GOAL = (0, 0)                   # Will be populated with the coordinates of the goal.

def setup(raw: str):
    print('Pre-calculating blizzard maps.')

    global LINES, RIGHT, BOTTOM, BLIZZARD_MINS, GOAL

    # Key = (x, y) current coordinates of 1 or more blizzards.
    # Value = string of blizzard direction of travel.
    blizzards = {}

    LINES = raw.split('\n')
    x, y = 0, 0
    for row in LINES:
        x = 0
        for c in row:
            if c in '<>^v':
                blizzards[x, y] = c
            x += 1
        y += 1

    RIGHT, BOTTOM = x - 2, y - 2

    # self.expedition = (1, 0)        # "Your expedition begins in the only non-wall position in the top row..."
    GOAL = (x - 2, y - 1)      # "... and needs to reach the only non-wall position in the bottom row."

    deltas = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}
    for minute in range(350):
        BLIZZARD_MINS[minute] = blizzards

        old_blizzards = blizzards.copy()
        blizzards = {}

        for x, y in old_blizzards:
            for direction in old_blizzards[(x, y)]:
                dx, dy = deltas[direction]
                new_x, new_y = x + dx, y + dy

                # If blizzard goes off edge of basin, flip around.
                if new_x > RIGHT:
                    new_x = 1
                if new_x == 0:
                    new_x = RIGHT
                if new_y > BOTTOM:
                    new_y = 1
                if new_y == 0:
                    new_y = BOTTOM

                if (new_x, new_y) in blizzards:
                    blizzards[(new_x, new_y)] += direction
                else:
                    blizzards[(new_x, new_y)] = direction
    print('Blizzard maps calculated.')


def render(exp_x: int, exp_y: int, minute: int):
    print('\nminute:', minute)
    x, y = 0, 0
    for row in LINES:
        for c in row:
            if c in '<>^v':
                c = '.'
            if (exp_x, exp_y) == (x, y):
                c = 'E'
            elif GOAL == (x, y):
                c = 'G'
            else:
                if (x, y) in BLIZZARD_MINS[minute]:
                    blizz_str = BLIZZARD_MINS[minute][(x, y)]
                    if len(blizz_str) == 1:
                        c = blizz_str
                    else:
                        c = str(len(blizz_str))

            print(c, end='')
            x += 1
        print()
        x = 0
        y += 1


def possible_moves(exp_x: int, exp_y: int, minute: int) -> list:
    """Return a list of possible (x, y) coordinates that expedition could move to next."""
    global HOME
    possible = []                                               # "...or you can wait in place."
    for dx, dy in [(0, 0), (1, 0), (0, 1), (0, -1), (0, -1)]:   # "On each minute, you can move up, down, left, or right..."
        px, py = exp_x + dx, exp_y + dy
        if (px, py) == GOAL:                            # Moving to goal is possible, so no other moves needed.
            return[(px, py, minute)]

        if (px, py) == HOME or ((px, py) not in BLIZZARD_MINS[minute] and 1 <= px <= RIGHT and 1 <= py <= BOTTOM):
            possible.append((px, py, minute))

    return possible


def count_non_maxsize(q: dict) -> int:
    num = 0
    for x, y, m in q:
        if q[(x, y, m)] != sys.maxsize:
            num += 1
    return num


f = open('input.txt')
t = f.read()
f.close()

setup(raw=t)
q, dist, prev, completed, lowest = {}, {}, {}, [], sys.maxsize

for minute in range(0, 350):
    for sx, sy in [HOME, GOAL]:
        dist[sx, sy, minute] = sys.maxsize
        prev[sx, sy, minute] = None

    for y in range(1, BOTTOM + 1):
        for x in range(1, RIGHT + 1):
            dist[(x, y, minute)] = sys.maxsize
            prev[(x, y, minute)] = None

hx, hy = HOME
SOURCE = (hx, hy, 0)
dist[SOURCE] = 0
q[SOURCE] = 0

while len(q) != 0:
    len_q = len(q)
    if len_q % 25 == 0:
        print('len_q, lowest:', len(q), lowest)

    # u ← vertex in Q with min dist[u]
    u = min(q, key=q.get)

    del q[u]
    completed.append(u)

    x, y, minute = u

    if minute < lowest:
        if (x, y) == GOAL:
            lowest = min(lowest, minute)

        minute += 1

        if minute < 350:
            for v in possible_moves(exp_x=x, exp_y=y, minute=minute):
                alt = minute

                # if alt < dist[v]:
                if alt < dist[v]:
                    # dist[v] ← alt
                    dist[v] = alt
                    # if v in q:
                    if v not in completed:
                        q[v] = alt
                    # prev[v] ← u
                    prev[v] = u

minute, part1 = 0, None
gx, gy = GOAL
while part1 is None:
    d = dist[(gx, gy, minute)]
    if d != sys.maxsize:
        part1 = d
    minute += 1

print('Part1:', part1)
