# Solution to day 6 of AOC 2022,
# https://adventofcode.com/2022/day/6

f = open('input.txt')
t = f.read()
f.close()

MARKER_LEN = 14
i, found = 0, False
while not found:
    check = t[i:(i + MARKER_LEN)]
    s = set()
    for e in check:
        s.add(e)
    print(s)
    found = len(s) == MARKER_LEN
    if not found:
        i += 1
print(i + MARKER_LEN)
