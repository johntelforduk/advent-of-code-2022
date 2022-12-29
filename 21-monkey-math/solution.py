# Solution to day 21 of AOC 2022,
# https://adventofcode.com/2022/day/21

f = open('input.txt')
t = f.read()
f.close()

# Queue of monkeys that have been converted to numbers.
q = []

# Key = Monkey name, Value = number or formula string
monkeys = {}

# Key = Term in a formula, Value = list of monkeys that include that term.
operands_to_monkeys = {}


def add_val_to_dict_list(d: dict, k: str, v: str):
    if k not in d:
        d[k] = [v]
    else:
        d[k] = d[k].append(v)

def contains_lower(s: str) -> bool:
    for c in s:
        if c.islower():
            return True
    return False


assert contains_lower('4 + lgvd') is True
assert contains_lower('4') is False
assert contains_lower('32 - 2') is False



for line in t.split('\n'):
    monkey, term = line.split(': ')
    if term.isnumeric():
        monkeys[monkey] = term
        q.append(monkey)
    else:
        operand1, _, operand2 = term.split(' ')
        add_val_to_dict_list(operands_to_monkeys, operand1, monkey)
        add_val_to_dict_list(operands_to_monkeys, operand2, monkey)
        monkeys[monkey] = term

print('monkeys:', monkeys)
print('terms_to_monkeys:', operands_to_monkeys)
print('q:', q)


while len(q) > 0:
    operand = q.pop(0)
    # print('operand:', operand)
    for monkey in operands_to_monkeys[operand]:
        # print('monkey:', monkey)
        term = monkeys[monkey]
        term = term.replace(operand, monkeys[operand])

        if contains_lower(term):
            monkeys[monkey] = term
        else:
            monkeys[monkey] = str(int(eval(term)))
            if monkey != 'root':
                q.append(monkey)

print()
print('monkeys:', monkeys)
# print('terms_to_monkeys:', operands_to_monkeys)
print('q:', q)

print('Part 1:', monkeys['root'])