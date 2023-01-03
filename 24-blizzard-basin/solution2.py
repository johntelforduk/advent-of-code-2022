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

    global LINES, RIGHT, BOTTOM, BLIZZARD_MINS, GOAL, HOME

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
    for minute in range(2000):
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


def possible_moves(exp_x: int, exp_y: int, minute: int, start_at: (int, int), end_at: (int, int)) -> list:
    """Return a list of possible (x, y) coordinates that expedition could move to next."""
    possible = []                                               # "...or you can wait in place."
    for dx, dy in [(0, 0), (1, 0), (0, 1), (0, -1), (-1, 0)]:   # "On each minute, you can move up, down, left, or right..."
        px, py = exp_x + dx, exp_y + dy
        if (px, py) == end_at:                            # Moving to goal is possible, so no other moves needed.
            return[(px, py, minute)]

        if (px, py) == start_at or ((px, py) not in BLIZZARD_MINS[minute] and 1 <= px <= RIGHT and 1 <= py <= BOTTOM):
            possible.append((px, py, minute))

    return possible


def shortest_path(start_min: int, max_min: int, start_at: (int, int), end_at: (int, int)) -> int:
    q, dist, prev, completed, lowest = {}, {}, {}, [], sys.maxsize

    for minute in range(start_min, max_min):
        for sx, sy in [start_at, end_at]:
            dist[sx, sy, minute] = sys.maxsize
            prev[sx, sy, minute] = None

        for y in range(1, BOTTOM + 1):
            for x in range(1, RIGHT + 1):
                dist[(x, y, minute)] = sys.maxsize
                prev[(x, y, minute)] = None

    hx, hy = start_at
    source = (hx, hy, start_min)
    dist[source] = start_min
    q[source] = start_min

    while len(q) != 0:
        len_q = len(q)
        if len_q % 25 == 0:
            print('len_q, lowest:', len(q), lowest)

        # u ← vertex in Q with min dist[u]
        u = min(q, key=q.get)

        del q[u]
        completed.append(u)

        x, y, minute = u
        # print(x, y)

        if minute < lowest:
            if (x, y) == end_at:
                lowest = min(lowest, minute)

            minute += 1

            if minute < max_min:
                for v in possible_moves(exp_x=x, exp_y=y, minute=minute, start_at=start_at, end_at=end_at):
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

    minute, part = start_min, None
    gx, gy = end_at
    while part is None:
        d = dist[(gx, gy, minute)]
        if d != sys.maxsize:
            part = d
        minute += 1

    return part


f = open('input.txt')
t = f.read()
f.close()

setup(raw=t)
leg1 = shortest_path(start_min=0, max_min=275, start_at=HOME, end_at=GOAL)
print(leg1)
leg2 = shortest_path(start_min=leg1, max_min=600, start_at=GOAL, end_at=HOME)
print(leg2)
leg3 = shortest_path(start_min=leg2, max_min=1500, start_at=HOME, end_at=GOAL)
print('part2:', leg3)
