# Solution to day 5 of AOC 2022,
# https://adventofcode.com/2022/day/5

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
            # print('a')
        first_row = False
    else:
        stack = 0
        for i in range(1, len(l), 4):
            crate = l[i]
            if crate != ' ':
                stack_no = (i - 1) // 4
                stacks1[stack_no].append(crate)

print(stacks1)


for m in raw_moves.split('\n'):
    _, how_many, _, from_stack, _, to_stack = m.split(' ')
    print(how_many, from_stack, to_stack)
    for i in range(int(how_many)):
        crate = stacks1[int(from_stack) - 1].pop()
        stacks1[int(to_stack) - 1].append(crate)

print(stacks1)

for s in stacks1:
    print(s[-1], end='')
print()
