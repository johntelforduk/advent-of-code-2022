# Solution to day 17 of AOC 2022,
# https://adventofcode.com/2022/day/17

import structlog

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

class Chamber:
    def __init__(self):
        self.width = 7
        self.top = 0
        self.grid = {}

        self.current_rock = None
        self.current_rock_x = None
        self.current_rock_y = None

    def render(self):
        """Print out the chamber."""

        render_grid = self.grid.copy()

        # Add the current rock to the render grid.
        if self.current_rock is not None:
            for x, y in self.current_rock.shape:
                render_grid[x + self.current_rock_x, y + self.current_rock_y] = '@'

        print()
        for y in range(self.top - 7, 0):
            print('|', end='')
            for x in range(self.width):
                if (x, y) in render_grid:
                    print(render_grid[(x, y)], end='')
                else:
                    print('.', end='')
            print('|')
        print('+' + '-' * self.width + '+')

    def add_rock(self, rock_type: int):
        self.current_rock = Rock(rock_type)

        # Each rock appears so that its left edge is two units away from the left wall...
        self.current_rock_x = 2

        # and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one).
        self.current_rock_y = self.top - self.current_rock.height - 3 - 1

        # log.info('Rock added',
        #          current_rock_x=self.current_rock_x,
        #          current_rock_y=self.current_rock_y)

    def jet(self, direction: str):
        # log.info('Start jet', direction=direction, falling=self.current_rock.falling,
        #          current_rock_x=self.current_rock_x,
        #          current_rock_width=self.current_rock.width,
        #          width=self.width)
        # if self.current_rock.falling:

        # TODO Check that move won't cause the falling rock to hit existing rocks.

        if self.can_jet(direction):
            if direction == '<':
                self.current_rock_x -= 1
            else:
                assert direction == '>'
                self.current_rock_x += 1

        # log.info('End jet', direction=direction, falling=self.current_rock.falling,
        #          current_rock_x=self.current_rock_x,
        #          current_rock_width=self.current_rock.width,
        #          width=self.width)

    def find_top(self) -> int:
        """Return the y position of the highest piece of rock in the caves."""
        lowest = 0
        for _, y in self.grid:
            lowest = min(lowest, y)
        return lowest

    def fall(self) -> bool:
        """Attempt to drop the current rock. If it is dropped ok, return True, otherwise return False."""
        if self.can_fall():
            self.current_rock_y += 1
            return True

        # Add the current shape to the cave.
        for x, y in self.current_rock.shape:
            self.grid[x + self.current_rock_x, y + self.current_rock_y] = '#'
        self.top = self.find_top()
        return False

    def can_fall(self) -> int:
        for x, y in self.current_rock.shape:
            if (x + self.current_rock_x, y + self.current_rock_y + 1) in self.grid:
                return False
            if y + self.current_rock_y + 1 >= 0:
                return False
        return True

    def can_jet(self, direction: str) -> bool:
        offset = 1
        if direction == '<':
            if self.current_rock_x <= 0:
                return False
            offset = -1
        else:
            assert direction == '>'
            if self.current_rock_x + self.current_rock.width >= self.width - 1:
                return False
        for x, y in self.current_rock.shape:
            if (x + self.current_rock_x + offset, y + self.current_rock_y) in self.grid:
                return False
        return True



class Rock:
    def __init__(self, rock_type: int):
        rock_maps = [{(0, 0), (1, 0), (2, 0), (3, 0)},
                     {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
                     {(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)},
                     {(0, 0), (0, 1), (0 ,2), (0, 3)},
                     {(0, 0), (1, 0), (0, 1), (1, 1)}]

        self.shape = rock_maps[rock_type]
        self.width = self.find_width
        self.height = self.find_height
        self.falling = True

        # log.info('Rock created',
        #          rock_type=rock_type,
        #          shape=self.shape,
        #          shape_type=type(self.shape),
        #          width=self.width,
        #          height=self.height)

    @property
    def find_width(self):
        max_x = 0
        for x, _ in self.shape:
            max_x = max(max_x, x)
        return max_x

    @property
    def find_height(self):
        max_y = 0
        for _, y in self.shape:
            max_y = max(max_y, y)
        return max_y


f = open('input.txt')
t = f.read()
f.close()

c = Chamber()

rock = 0
c.add_rock(rock_type=rock)

i = 0

rocks_stopped = 0
while rocks_stopped < 2022:
    d = t[i]
    i += 1
    if i >= len(t):
        i = 0

    c.jet(direction=d)
    # print(d)
    did_fall = c.fall()
    if not did_fall:
        rock = (rock + 1) % 5
        c.add_rock(rock_type=rock)
        rocks_stopped += 1
        if rocks_stopped % 100 == 0:
            c.render()
            print(rocks_stopped)

print(rocks_stopped, c.top)
