# Solution to day 5 of AOC 2022,
# https://adventofcode.com/2022/day/5

import copy


def top_crates(stacks: list) -> str:
    top = ''
    for st in stacks:
        top += st[-1]
    return top


f = open('input.txt')
t = f.read()
f.close()

raw_stacks, raw_moves = t.split('\n\n')

stacks1 = []
first_row = True
for l in reversed(raw_stacks.split('\n')):
    if first_row:
        for i in l.split('   '):
            stacks1.append([])
        first_row = False
    else:
        stack = 0
        for i in range(1, len(l), 4):
            crate = l[i]
            if crate != ' ':
                stack_no = (i - 1) // 4
                stacks1[stack_no].append(crate)

stacks2 = copy.deepcopy(stacks1)

for m in raw_moves.split('\n'):
    _, how_many, _, from_stack, _, to_stack = m.split(' ')

    crates = []
    for i in range(int(how_many)):
        crate = stacks1[int(from_stack) - 1].pop()
        stacks1[int(to_stack) - 1].append(crate)
        crate = stacks2[int(from_stack) - 1].pop()
        crates.append(crate)
    crates.reverse()
    stacks2[int(to_stack) - 1] = stacks2[int(to_stack) - 1] + crates

print('Part 1: ' + top_crates(stacks1))
print('Part 2: ' + top_crates(stacks2))
