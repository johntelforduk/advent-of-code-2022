# Solution to day 15 of AOC 2022,
# https://adventofcode.com/2022/day/15

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

f = open('input.txt')
t = f.read()
f.close()


def manhatten(x1: int, y1: int, x2: int, y2: int) -> int:
    """For parm pair of coordinates, return the Manhatten distance between them."""
    return abs(x1 - x2) + abs(y1 - y2)


def cannot(sx: int, sy: int, m: int, y) -> (int, int):
    """For parm sensor coordinate, with a nearest sensor of parm Manhatten distance away. Return a tuple which
    is the minimum and maximum possible that a beacon cannot be."""
    vert_dist = abs(sy - y)
    dist_left = m - vert_dist
    if dist_left < 0:
        return None, None
    return sx - dist_left, sx + dist_left


def attempt_reduce(l1: int, h1: int, l2: int, h2: int) -> (int, int):
    if h1 < l2 or h2 < l1:
        return None, None
    return min(l1, l2), max(h1, h2)


def reduce(r: list) -> list:
    t1, t2 = 0, 0
    while t1 < len(r):
        l1, h1 = r[t1]
        while t2 < len(r):
            if t1 != t2:
                l2, h2 = r[t2]
                log.info('In reduce', l1=l1, h1=h1, l2=l2, h2=h2)

                lr, hr = attempt_reduce(l1, h1, l2, h2)
                if (lr, hr) != (None, None):
                    r.remove((l1, h1))
                    r.remove((l2, h2))
                    r.append((lr, hr))
                    return r
            t2 += 1
        t2 = 0
        t1 += 1
    return r


assert manhatten(0, 0, 0, 0) == 0
assert manhatten(0, 0, 2, 2) == 4
assert manhatten(-1, 4, 2, -7) == 14

assert attempt_reduce(0, 2, 10, 19) == (None, None)
assert attempt_reduce(-15, -3, 0, 12) == (None, None)
assert attempt_reduce(1, 10, 3, 9) == (1, 10)
assert attempt_reduce(-10, -1, -3, -1) == (-10, -1)
assert attempt_reduce(1, 7, 3, 10) == (1, 10)
assert attempt_reduce(3, 10, 1, 7) == (1, 10)

# Sensor at x=8, y=7: closest beacon is at x=2, y=10
ranges = []
beacons = set()
for line in t.split('\n'):
    parts = line.split(', ')
    # print(parts)
    sx = int(parts[0].split('=')[1])
    sy = int(parts[1][2:].split(':')[0])
    bx = int(parts[1].split('=')[2])
    by = int(parts[2].split('=')[1])

    m = manhatten(sx, sy, bx, by)
    lx, hx = cannot(sx, sy, m, 2000000)
    if by == 2000000:
        beacons.add((bx, by))

    log.info('Cannot calculated',
             sx=sx,
             sy=sy,
             bx=bx,
             by=by,
             lx=lx,
             hx=hx)

    if lx is not None:
        ranges.append((lx, hx))

print(ranges)

range_len = len(ranges)
shortening = True
while shortening:
    ranges = reduce(ranges)
    new_len = len(ranges)
    shortening = new_len < range_len
    range_len = new_len

print(ranges)

pl, ph = ranges[0]
print(pl, ph)
positions = ph - pl + 1 - len(beacons)

print(beacons)
print(positions)
