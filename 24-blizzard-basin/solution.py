# Solution to day 24 of AOC 2022,
# https://adventofcode.com/2022/day/24

import copy
import json


class Basin:

    def __init__(self, raw: str):

        # Key = (x, y) current coordinates of 1 or more blizzards.
        # Value = string of blizzard direction of travel.
        self.blizzards = {}

        self.lines = raw.split('\n')
        x, y = 0, 0
        for row in self.lines:
            x = 0
            for c in row:
                if c in '<>^v':
                    self.blizzards[x, y] = c
                x += 1
            y += 1

        self.right, self.bottom = x - 2, y - 2

        self.expedition = (1, 0)        # "Your expedition begins in the only non-wall position in the top row..."
        self.goal = (x - 2, y - 1)      # "... and needs to reach the only non-wall position in the bottom row."
        self.minute = 0

    def hash_state(self):
        return self.expedition


    def new_minute(self):
        old_blizzards = self.blizzards.copy()

        deltas = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}
        self.blizzards = {}

        for x, y in old_blizzards:
            for direction in old_blizzards[(x, y)]:
                dx, dy = deltas[direction]
                new_x, new_y = x + dx, y + dy

                # If blizzard goes off edge of basin, flip around.
                if new_x > self.right:
                    new_x = 1
                if new_x == 0:
                    new_x = self.right
                if new_y > self.bottom:
                    new_y = 1
                if new_y == 0:
                    new_y = self.bottom

                if (new_x, new_y) in self.blizzards:
                    self.blizzards[(new_x, new_y)] += direction
                else:
                    self.blizzards[(new_x, new_y)] = direction

        self.minute += 1

    def render(self):
        print('minute:', self.minute)
        x, y = 0, 0
        for row in self.lines:
            for c in row:
                if c in '<>^v':
                    c = '.'
                if self.expedition == (x, y):
                    c = 'E'
                elif self.goal == (x, y):
                    c = 'G'
                else:
                    if (x, y) in self.blizzards:
                        blizz_str = self.blizzards[(x, y)]
                        if len(blizz_str) == 1:
                            c = blizz_str
                        else:
                            c = str(len(blizz_str))

                print(c, end='')
                x += 1
            print()
            x = 0
            y += 1
        print()

    def manhattan(self):
        x, y = self.expedition
        return x + y

    def possible_moves(self) -> list:
        """Return a list of possible (x, y) coordinates that expedition could move to next."""
        x, y = self.expedition
        possible = [(x, y)]                                 # "...or you can wait in place."
        for dx, dy in [(1, 0), (0, 1), (0, -1), (0, -1)]:   # "On each minute, you can move up, down, left, or right..."
            px, py = x + dx, y + dy
            if (px, py) == self.goal:
                return[self.goal]

            if (px, py) not in self.blizzards and 1 <= px <= self.right and 1 <= py <= self.bottom:
                possible.append((x + dx, y + dy))
        return possible


def search(this_basin: Basin):
    global LEAST_MINUTES
    global PREVIOUS_STATES

    # print(LEAST_MINUTES, this_basin.minute, this_basin.expedition)

    if this_basin.minute + 1 >= LEAST_MINUTES:      # We've already found a quicker route, so give up.
        return

    if this_basin.minute > 900:                 # Search too long, so give up.
        return

    if this_basin.minute > 5 * this_basin.manhattan():
        return

    hash = this_basin.hash_state()
    if hash in PREVIOUS_STATES:
        if PREVIOUS_STATES[hash] <= this_basin.minute:
            return
        PREVIOUS_STATES[hash] = this_basin.minute

    this_basin.new_minute()                     # Move the blizzards, and add 1 to the minute count.


    # print(this_basin.hash_state())

    if this_basin.expedition == this_basin.goal:
        LEAST_MINUTES = this_basin.minute
        print(LEAST_MINUTES)
        return

    for possible_expedition in this_basin.possible_moves():
        new_basin = copy.deepcopy(this_basin)
        new_basin.expedition = possible_expedition
        search(this_basin=new_basin)


f = open('input.txt')
t = f.read()
f.close()

basin = Basin(raw=t)
# print(basin.blizzards)
# print(basin.expedition, basin.goal)
basin.render()

LEAST_MINUTES = 9999999
PREVIOUS_STATES = {}

search(this_basin=basin)

print('Part 1:', LEAST_MINUTES)
# basin.new_minute()
# basin.render()
#
# basin.new_minute()
# basin.render()
#
# basin.new_minute()
# basin.render()
#
# basin.new_minute()
# basin.render()
#
# basin.new_minute()
# basin.render()
