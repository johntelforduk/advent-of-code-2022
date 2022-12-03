# Solution to day 3 of AOC 2022,
# https://adventofcode.com/2022/day/3

def priority(s: str) -> int:
    # 'a' = 97, 'A' = 65
    ascii_val = ord(s)
    return ascii_val - 96 if ascii_val > 96 else ascii_val - 64 + 26


f = open('input.txt')
t = f.read()
f.close()

part1, part2 = 0, 0
waltz = 0
triple_common = set()
for rucksack in t.split():
    items_per_comp = len(rucksack) // 2
    comp1 = set(rucksack[0:items_per_comp])
    comp2 = set(rucksack[items_per_comp:])
    common = comp1.intersection(comp2).pop()

    part1 += priority(s=common)

    if waltz == 0:
        triple_common = set(rucksack)
    else:
        triple_common = triple_common.intersection(rucksack)

    if waltz == 2:
        part2 += priority(s=triple_common.pop())

    waltz = (1 + waltz) % 3


print('Part 1:', part1)
print('Part 2:', part2)
