# Solution to day 22 of AOC 2022,
# https://adventofcode.com/2022/day/22

class Board:

    def __init__(self, text: str):

        raw_board, raw_path = text.split('\n\n')

        board_list = raw_board.split('\n')
        x, y = 1, 1

        self.max_x, self.max_y = 0, 0

        # Key = (x, y) tuple, coordinates of the square on the grid.
        # Value = '.' for space, and '#' for wall.
        self.grid = {}

        self.x, self.y = None, y        # My current position on the board.
        for row in board_list:
            for square in row:
                if square != ' ':
                    self.grid[(x, y)] = square
                    if self.x is None:
                        self.x, self.y = x, y
                    self.max_x = max(self.max_x, x)
                    self.max_y = max(self.max_y, y)
                x += 1
            x = 1
            y += 1

        # print(self.grid)

        print('self.x, self.y:', self.x, self.y)

        print(raw_path)

        path = list(raw_path)
        self.instructions = []
        distance = 0
        while len(path) > 0:
            s = path.pop(0)
            if s.isdigit():
                distance = 10 * distance + int(s)
            else:
                self.instructions.append(distance)
                distance = 0
                self.instructions.append(s)
        if distance > 0:
            self.instructions.append(distance)

        # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
        self.facing = 0

        # Key = (x, y) coordinates.
        # Value = symbol for direction that we were facing when we left those coordinates.
        self.path = {}

    def counterclockwise(self):
        self.facing = (self.facing - 1) % 4

    def clockwise(self):
        self.facing = (self.facing + 1) % 4

    def rotate_instr(self, d: str):
        if d == 'R':
            self.clockwise()
        else:
            assert d == 'L'
            self.counterclockwise()
        assert 0 <= self.facing <= 3        # After the rotation, we should still have a valid facing value.

    def facing_to_symbol(self) -> str:
        """Return the symbol that can be rendered for current facing direction."""
        f_to_s = {0: '>', 1: 'v', 2: '<', 3: '^'}
        return f_to_s[self.facing]

    def next_square(self) -> (int, int):
        """Return the (x, y) coordinates of the next square."""

        # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
        deltas = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}

        dx, dy = deltas[self.facing]
        x, y = self.x + dx, self.y + dy

        if (x, y) in self.grid:
            return x, y

        # Next square is off the edge of the board.
        # So search in opposite direction for opposite edge of board.
        dx *= -1
        dy *= -1

        x, y = self.x, self.y
        while (x + dx, y + dy) in self.grid:
            x += dx
            y += dy
        return x, y

    def can_move(self) -> bool:
        """Return True if the next square that we would attempt to move into is an empty space '.'.
        Return False if it is a wall, '#'."""
        return self.grid[self.next_square()] == '.'

    def move_one_step(self):
        """If it is possible to move, then move us one step.
        Otherwise, don't move at all."""
        self.path[self.x, self.y] = self.facing_to_symbol()

        if self.can_move():
            self.x, self.y = self.next_square()
            assert self.grid[(self.x, self.y)] == '.'
            self.path[self.x, self.y] = self.facing_to_symbol()

    def render(self):
        """Print the board, including trail followed by us, to the screen."""
        for y in range(1, 1 + self.max_y):
            for x in range(1, 1 + self.max_x):
                if (x, y) in self.grid:
                    s = self.grid[(x, y)]
                    if (x, y) in self.path:
                        s = self.path[(x, y)]
                else:
                    s = ' '
                print(s, end='')
            print()

    def walk(self):
        """Follow the walking instructions."""
        while len(self.instructions) > 0:
            next_instr = self.instructions.pop(0)

            if isinstance(next_instr, int):
                steps = next_instr
                while steps > 0:
                    self.move_one_step()
                    steps -= 1
            else:
                self.rotate_instr(d=next_instr)


f = open('input.txt')
t = f.read()
f.close()

board = Board(text=t)
print(board.instructions)
board.walk()
board.render()
print('Part 1:', 1000 * board.y + 4 * board.x + board.facing)

# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.rotate_instr('R')
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.rotate_instr('L')
# board.move_one_step()
# board.move_one_step()
# board.rotate_instr('R')
# board.move_one_step()
# board.rotate_instr('R')
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.rotate_instr('L')
# board.move_one_step()
# board.rotate_instr('R')
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.rotate_instr('R')
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
# board.move_one_step()
#
# board.render()
