# Solution to day 2 of AOC 2022,
# https://adventofcode.com/2022/day/2


def decrypt(s: str) -> str:
    code = {'A': 'rock', 'X': 'rock',
            'B': 'paper', 'Y': 'paper',
            'C': 'scissors', 'Z': 'scissors'}
    return code[s]


def outcome_points(opp: str, me: str) -> int:
    beats = [('rock', 'scissors'), ('scissors', 'paper'), ('paper', 'rock')]
    if (me, opp) in beats:          # We won!
        return 6
    if opp == me:                   # A draw.
        return 3
    return 0                        # If we didn't win and it wasn't a draw, we must have lost.


def shape_points(me: str) -> int:
    score = {'rock': 1, 'paper': 2, 'scissors': 3}
    return score[me]


def decrypt_aim(s: str) -> str:
    code = {'X': 'loose', 'Y': 'draw', 'Z': 'win'}
    return code[s]


def my_choice(opp: str, aim: str) -> str:
    target_points = {'win': 6, 'draw': 3, 'loose': 0}[aim]
    for test in ['rock', 'paper', 'scissors']:
        if outcome_points(opp, test) == target_points:
            return test
    return ''


f = open('input.txt')
t = f.read()
f.close()

part1, part2 = 0, 0
for r in t.split('\n'):
    o, m = r.split(' ')

    o_choice, m_choice = decrypt(o), decrypt(m)
    part1 += outcome_points(o_choice, m_choice)
    part1 += shape_points(m_choice)

    m_aim = decrypt_aim(m)
    m_choice = my_choice(o_choice, m_aim)
    part2 += outcome_points(o_choice, m_choice)
    part2 += shape_points(m_choice)

print('Part 1:', part1)
print('Part 2:', part2)

