# Solution to day 24 of AOC 2022,
# https://adventofcode.com/2022/day/24

class Basin:

    def __init__(self, raw: str):

        # Key = (x, y) current coordinates of 1 or more blizzards.
        # Value = list of blizzard direction of travel.
        self.blizzards = {}

        self.lines = raw.split('\n')
        x, y = 0, 0
        for row in self.lines:
            x = 0
            for c in row:
                if c in '<>^v':
                    self.blizzards[x, y] = [c]
                x += 1
            y += 1

        self.right, self.bottom = x - 2, y - 2

        self.expedition = (1, 0)        # Current coordinates of the expedition.
        self.goal = (x - 2, y - 1)      # Coordinates of the goal square.
        self.minute = 0

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
                    self.blizzards[(new_x, new_y)].append(direction)
                else:
                    self.blizzards[(new_x, new_y)] = [direction]

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
                        blizz_list = self.blizzards[(x, y)]
                        if len(blizz_list) == 1:
                            c = blizz_list[0]
                        else:
                            c = str(len(blizz_list))

                print(c, end='')
                x += 1
            print()
            x = 0
            y += 1
        print()


f = open('test2.txt')
t = f.read()
f.close()

basin = Basin(raw=t)
# print(basin.blizzards)
# print(basin.expedition, basin.goal)
basin.render()

basin.new_minute()
basin.render()

basin.new_minute()
basin.render()

basin.new_minute()
basin.render()

basin.new_minute()
basin.render()

basin.new_minute()
basin.render()
