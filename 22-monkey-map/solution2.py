# Solution to day 22 of AOC 2022,
# https://adventofcode.com/2022/day/22

class Board:

    def __init__(self, text: str, cube_units: int):

        self.cube_units = cube_units

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

        # # Net for test data.
        # self.net = {(2, 1, 0): (3, 2, 1, 'x = -y'),
        #             (2, 2, 1): (0, 1, 3, 'x = -x'),
        #             (1, 1, 3): (2, 0, 0, 'y = +x')}

        # Net for puzzle input.
        # Key = (x, y, facing direction of exit), where x, y are face coordinates of face being exited.
        # Value = (x, y, facing direction of entry, formula), where x, y, are face coordinates of being entered.
        self.net = {(1, 1, 0): (2, 0, 3, 'x = +y'),
                    (2, 0, 1): (1, 1, 2, 'y = +x'),

                    (1, 2, 0): (2, 0, 2, 'y = -y'),
                    (2, 0, 0): (1, 2, 2, 'y = -y'),

                    (1, 1, 2): (0, 2, 1, 'x = +y'),
                    (0, 2, 3): (1, 1, 0, 'y = +x'),

                    (1, 2, 1): (0, 3, 2, 'y = +x'),
                    (0, 3, 0): (1, 2, 3, 'x = +y'),

                    (1, 0, 2): (0, 2, 0, 'y = -y'),
                    (0, 2, 2): (1, 0, 0, 'y = -y'),

                    (2, 0, 3): (0, 3, 3, 'x = +x'),
                    (0, 3, 1): (2, 0, 1, 'x = +x'),

                    (1, 0, 3): (0, 3, 0, 'y = +x'),
                    (0, 3, 2): (1, 0, 1, 'x = +y')}

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

    def next_square(self) -> (int, int, int):
        """Return the (x, y) coordinates of the next square."""

        # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
        deltas = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}

        dx, dy = deltas[self.facing]
        x, y = self.x + dx, self.y + dy

        if (x, y) in self.grid:
            return x, y, self.facing

        # Next square is off the edge of the board.

        # cf = current face
        # nf = new face

        cf_x, cf_y = self.current_face()
        nf_x, nf_y, nf_f, formula = self.net[cf_x, cf_y, self.facing]

        # print(nf_x, nf_y, nf_f, formula)

        # Formula is like, "x = -y"
        right_side = formula.split(' = ')[1]
        sign = right_side[0]
        operand = right_side[1]

        # self.facing = nf_f

        cf_lx, cf_ty, cf_rx, cf_by = self.face_corners(cf_x, cf_y)
        nf_lx, nf_ty, nf_rx, nf_by = self.face_corners(nf_x, nf_y)

        # New face facing direction implies half of our new coordinate.
        # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)

        if sign == '+':
            if operand == 'x':
                offset = self.x - cf_lx
            else:
                offset = self.y - cf_ty
        else:
            assert sign == '-'
            if operand == 'x':
                offset = cf_rx - self.x
            else:
                offset = cf_by - self.y

        if nf_f == 0:
            y = nf_ty + offset
            return nf_lx, y, nf_f

        elif nf_f == 1:
            x = nf_lx + offset
            return x, nf_ty, nf_f

        # XXX
        elif nf_f == 2:
            y = nf_ty + offset
            return nf_rx, y, nf_f

        elif nf_f == 3:
            x = nf_lx + offset
            return x, nf_by, nf_f

    def can_move(self) -> bool:
        """Return True if the next square that we would attempt to move into is an empty space '.'.
        Return False if it is a wall, '#'."""
        # print('next_square:', self.next_square())
        x, y, _ = self.next_square()
        return self.grid[x, y] == '.'

    def move_one_step(self):
        """If it is possible to move, then move us one step.
        Otherwise, don't move at all."""
        self.path[self.x, self.y] = self.facing_to_symbol()

        if self.can_move():
            self.x, self.y, self.facing = self.next_square()
            assert self.grid[(self.x, self.y)] == '.'
            self.path[self.x, self.y] = self.facing_to_symbol()

        # print()
        # self.render()

    def current_face(self):
        """Return the (x, y) coordinates of the face we are currently standing on in the net."""
        x = (self.x - 1) // self.cube_units
        y = (self.y - 1) // self.cube_units
        return x, y

    def face_corners(self, x: int, y: int) -> (int, int, int, int):
        """For parm face (x, y) coordinates, return the coords of its,
             top-left corner,
             bottom-right corner."""
        lx, ty = 1 + x * self.cube_units, 1 + y * self.cube_units
        rx, by = (x + 1) * self.cube_units, (y + 1) * self.cube_units
        return lx, ty, rx, by

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

# For test data, each edge of the cube is 4 units long.
# board = Board(text=t, cube_units=4)

board = Board(text=t, cube_units=50)

print(board.instructions)
board.walk()
board.render()
print('board.x, board.y, board.facing:', board.x, board.y, board.facing)
print('Part 2:', 1000 * board.y + 4 * board.x + board.facing)
