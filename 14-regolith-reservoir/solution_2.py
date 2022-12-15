# Solution to day 14 of AOC 2022,
# https://adventofcode.com/2022/day/14

import pygame
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


def drop_one_step(x: int, y: int) -> (int, int, bool):
    """Make grain of sand at parm coordinates drop by one grid position. Return False if the grain can't drop
    anymore, True otherwise."""
    tries = [(0, 1), (-1, 1), (1, 1)]
    for dx, dy in tries:
        if (x + dx, y + dy) not in cave and y + 1 < floor:
            return x + dx, y + dy, True
    return x, y, False


def drop_sand(x: int, y: int) -> bool:
    """Drop sand into cave at parm position. Return True if spout is blocked, False otherwise."""
    if (x, y) in cave:
        return True
    can_move = True
    while can_move:
        x, y, can_move = drop_one_step(x, y)
        # if y > my:
        #     in_abyss = True
    cave[x, y] = 'o'
    return False


f = open('input.txt')
t = f.read()
f.close()

cave = {}

for line in t.split('\n'):
    path = [eval(point) for point in line.split(' -> ')]
    x, y = path.pop(0)
    log.info('After pop', x=x, y=y)
    for nx, ny in path:
        next_x, next_y = nx, ny
        log.info('In loop', nx=nx, ny=ny)
        if x == nx:
            while ny != y:
                cave[x, ny] = '#'
                if ny < y:
                    ny += 1
                else:
                    ny -= 1
            cave[x, ny] = '#'
        else:
            assert y == ny
            while nx != x:
                cave[nx, y] = '#'
                if nx < x:
                    nx += 1
                else:
                    nx -= 1
            cave[nx, y] = '#'
        x, y = next_x, next_y

print(cave)

# XXX

my = -10000
for x, y in cave:
    my = max(my, y)

floor = my + 2


part2 = 0
done = False
while not done:
    done = drop_sand(500, 0)
    part2 += 1
part2 -= 1

print(part2)

lx, ly, mx, my = 10000, 10000, -10000, -10000
for x, y in cave:
    lx = min(lx, x)
    ly = min(ly, y)
    mx = max(mx, x)
    my = max(my, y)

width, height = mx - lx, my - ly

for x in range(lx -1, mx + 2):
    cave[x, floor] = '#'

print(lx, ly, mx, my, width, height, floor)


scale = 10
border = 3

pygame.init()                                               # Initialize the game engine.

screen_size = [scale * (width + 2 * border), scale * (height + 2 * border)]  # [width, height]
screen = pygame.display.set_mode(screen_size)

wall = (0, 0, 0)  # Black.
background = (255, 255, 255)  # White
sand = (150, 75, 0)

screen.fill(background)

for x, y in cave:
    render_x = (x - lx)
    render_y = (y - ly)

    if cave[x, y] == '#':
        screen.fill(color=wall, rect=[(render_x + 3) * scale, (render_y + 3) * scale, scale, scale])
    if cave[x, y] == 'o':
        pygame.draw.circle(screen,
                           color=sand,
                           center=(scale // 2 + (render_x + 3) * scale, scale // 2 + (render_y + 3) * scale), radius=scale // 2.5)

# screen.fill(color=off_colour, rect=[10,10,2, 2])

screenshot_name = 'd14_2.png'
pygame.image.save(screen, screenshot_name)
pygame.display.flip()
