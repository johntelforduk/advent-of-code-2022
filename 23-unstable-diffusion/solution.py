# Solution to day 23 of AOC 2022,
# https://adventofcode.com/2022/day/23

class Grove:

    def __init__(self, raw: str):

        # Each item in this set is a tuple (x, y).
        self.elves = set()

        self.min_x, self.max_x, self.min_y, self.max_y = 1000, -1000, 1000, -1000

        lines = raw.split('\n')

        x, y, = 0, 0
        while len(lines) > 0:
            row = lines.pop(0)
            for square in row:
                if square == '#':
                    self.elves.add((x, y))
                x += 1
            x = 0
            y += 1

        self.update_min_max()
        self.directions = ['N', 'S', 'W', 'E']

        # Key = Compass direction.
        # Value = List of square that need to be free for that direction to be considered.
        #         The first item in list the place to be moved to if the move goes ahead.
        self.deltas = {'N': [(0, -1), (-1, -1), (1, -1)],
                       'E': [(1, 0), (1, -1), (1, 1)],
                       'S': [(0, 1), (1, 1), (-1, 1)],
                       'W': [(-1, 0), (-1, -1), (-1, 1)]}

    def is_free_direction(self, x: int, y: int, d: str) -> bool:
        """Return True if all 3 places in parm direction from parm coordinates are free. Return False otherwise."""
        for dx, dy in self.deltas[d]:
            if (x + dx, y + dy) in self.elves:
                return False
        return True

    def a_round(self):
        # Key = Coordinates of a place that at least 1 elf is thinking of moving to.
        # Value is list of elves who are thinking of moving there.
        proposals = {}

        for x, y in self.elves:
            chosen_direction, free_directions = None, 0

            # "Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step
            # in the first valid direction:"
            for direction in self.directions:
                this_one_free = self.is_free_direction(x, y, d=direction)
                if this_one_free:
                    free_directions += 1
                    if chosen_direction is None:
                        chosen_direction = direction
            print(x, y, chosen_direction, free_directions)

            # "If no other Elves are in one of those eight positions, the Elf does not do anything during this round."
            if chosen_direction is not None and free_directions != 4:
                dx, dy = self.deltas[chosen_direction][0]   # First item in list is move to square for the direction.

                px, py = x + dx, y + dy
                if (px, py) not in proposals:
                    proposals[(px, py)] = [(x, y)]
                else:
                    proposals[(px, py)].append((x, y))

        print(proposals)

        # "Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose
        # moving to that position. If two or more Elves propose moving to the same position, none of those Elves move."
        for px, py in proposals:                    # 'p'roposed coordinates.
            if len(proposals[(px, py)]) == 1:       # Only 1 elf proposed moving here.
                print(px, py)
                x, y = proposals[(px, py)][0]
                self.elves.remove((x, y))
                self.elves.add((px, py))

        # "Finally, at the end of the round, the first direction the Elves considered is moved to the end of the list
        # of directions."
        first = self.directions.pop(0)
        self.directions.append(first)

        self.update_min_max()

    def update_min_max(self):
        self.min_x, self.max_x, self.min_y, self.max_y = 1000, -1000, 1000, -1000

        for x, y in self.elves:
            self.min_x = min(x, self.min_x)
            self.max_x = max(x, self.max_x)
            self.min_y = min(y, self.min_y)
            self.max_y = max(y, self.max_y)

    def render(self):
        self.update_min_max()
        empties = 0
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.elves:
                    print('#', end='')
                else:
                    print('.', end='')
                    empties += 1
            print()
        print()
        return empties


f = open('input.txt')
t = f.read()
f.close()

grove = Grove(raw=t)

for r in range(10):
    grove.a_round()
part1 = grove.render()

print('Part 1:', part1)
