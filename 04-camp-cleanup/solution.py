# Solution to day 4 of AOC 2022,
# https://adventofcode.com/2022/day/4


f = open('input.txt')
t = f.read()
f.close()


def get_range(s: str) -> (int, int):
    l, u = s.split('-')
    return int(l), int(u)


def subsumes(a, b, c, d) -> bool:
    return a <= c and b >= d


def overlaps(a, b, c, d) -> bool:
    return b >= c and a <= d or d >= a and c <= b


part1, part2 = 0, 0
for pair in t.split():
    r1, r2 = pair.split(',')
    l1, u1 = get_range(r1)
    l2, u2 = get_range(r2)

    if subsumes(l1, u1, l2, u2) or subsumes(l2, u2, l1, u1):
        part1 += 1
    if overlaps(l1, u1, l2, u2):
        part2 += 1

print('Part 1:', part1)
print('Part 2:', part2)
