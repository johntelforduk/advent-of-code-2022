# Solution to day 9 of AOC 2022,
# https://adventofcode.com/2022/day/9

import pygame


def touching(hx: int, hy: int, tx: int, ty: int) -> bool:
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if hx == tx + dx and hy == ty + dy:
                return True
    return False


def knot_move(hx: int, hy: int, tx:int, ty: int) -> (int, int):
    # Due to the aforementioned Planck lengths, the rope must be quite short; in fact, the head (H) and tail (T) must
    # always be touching (diagonally adjacent and even overlapping both count as touching).
    if touching(hx, hy, tx, ty):
        return tx, ty

    # If the head is ever two steps directly up, down, left, or right from the tail, the tail must also move one step
    # in that direction so it remains close enough.
    if hy == ty:
        if hx > tx:
            return hx - 1, ty
        else:
            return hx + 1, ty

    if hx == tx:
        if hy > ty:
            return tx, hy - 1
        else:
            return tx, hy + 1

    # Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one
    # step diagonally to keep up.
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            if touching(hx, hy, tx + dx, ty + dy):
                return tx + dx, ty + dy

    raise "Error - can't find a move."


assert knot_move(0, 0, 1, 0) == (1, 0)
assert knot_move(10, 12, 10, 13) == (10, 13)
assert knot_move(5, 10, 4, 11) == (4, 11)
assert knot_move(67, 78, 67, 78) == (67, 78)

assert knot_move(0, 0, 2, 0) == (1, 0)
assert knot_move(3, 3, 1, 3) == (2, 3)
assert knot_move(0, 0, 0, -2) == (0, -1)
assert knot_move(10, 100, 10, 98) == (10, 99)

assert knot_move(2, 1, 1, 3) == (2, 2)
assert knot_move(3, 2, 1, 3) == (2, 2)


f = open('input.txt')
t = f.read()
f.close()

# hx, hy, tx, ty = 0, 0, 0, 0

length = 10
rope = [(0, 0)] * length
print(rope)

tail_visits = set()
tail_visits.add(rope[length - 1])
for motion in t.split('\n'):
    direction, raw_steps = motion.split(' ')
    steps = int(raw_steps)
    print(direction, steps)

    for i in range(steps):
        # Move the head.
        hx, hy = rope[0]
        if direction == 'U':
            hy -= 1
        elif direction == 'D':
            hy += 1
        elif direction == 'R':
            hx += 1
        else:
            hx -= 1
        rope[0] = (hx, hy)

        # Move each of the other (non-head) knots.
        for k in range(1, length):
            ax, ay = rope[k -1]
            bx, by = rope[k]

            rope[k] = knot_move(ax, ay, bx, by)

        tail_visits.add(rope[length - 1])

print(len(tail_visits))


lx, ly, mx, my = 0, 0, 0, 0
for x, y in tail_visits:
    lx = min(lx, x)
    ly = min(ly, y)
    mx = max(mx, x)
    my = max(my, y)

width, height = mx - lx, my - ly

print(lx, ly, mx, my, width, height)
scale = 2

pygame.init()                                               # Initialize the game engine.

screen_size = [scale * (width + 1) + 10, scale * (height + 1) + 10]  # [width, height]
screen = pygame.display.set_mode(screen_size)

black = (0, 0, 0)  # Black.
white = (255, 255, 255)  # White

screen.fill(white)

for x, y in tail_visits:
    render_x = (x - lx)
    render_y = (y - ly)
    screen.fill(color=black, rect=[5 + render_x * scale, 5 + render_y * scale, scale, scale])

# screen.fill(color=off_colour, rect=[10,10,2, 2])

screenshot_name = 'd9_' + str(length) + '.png'
pygame.image.save(screen, screenshot_name)
pygame.display.flip()
