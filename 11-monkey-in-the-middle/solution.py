# Solution to day 11 of AOC 2022,
# https://adventofcode.com/2022/day/11

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


class Monkey:

    def __init__(self, definition: str):
        lines = definition.split('\n')

        self.number = int(lines[0].split(' ')[1][:-1])
        self.inspections = 0

        raw_items = lines[1].split(': ')[1]
        self.items = [int(item) for item in raw_items.split(', ')]

        self.operation = lines[2].split(' = ')[1]

        self.divisor = int(lines[3].split(' divisible by ')[1])

        self.true_throw = int(lines[4].split('If true: throw to monkey ')[1])

        self.false_throw = int(lines[5].split('If false: throw to monkey ')[1])

        log.info('Monkey created',
                 number=self.number,
                 inspections=self.inspections,
                 items=self.items,
                 operation=self.operation,
                 divisor=self.divisor,
                 true_throw=self.true_throw,
                 false_throw=self.false_throw)


def turn(ml: list, mn: int):
    monkey = ml[mn]

    while len(monkey.items) > 0:
        monkey.inspections += 1

        old = monkey.items.pop(0)
        # new = eval(monkey.operation) // 3                 # Part 1
        new = eval(monkey.operation) % COMMON_FACTOR        # Part 2

        if (new % monkey.divisor) == 0:
            ml[monkey.true_throw].items.append(new)
        else:
            ml[monkey.false_throw].items.append(new)


def print_monkeys(ml: list):
    for monkey in ml:
        print('Monkey', monkey.number, 'Inspections', monkey.inspections, monkey.items)


f = open('input.txt')
t = f.read()
f.close()

monkeys = []
for monkey_text in t.split('\n\n'):
    monkeys.append(Monkey(definition=monkey_text))

COMMON_FACTOR = 1
for m in monkeys:
    COMMON_FACTOR *= m.divisor
print(COMMON_FACTOR)

for r in range(1, 10001):
    for m_num in range(len(monkeys)):
        turn(ml=monkeys, mn=m_num)

    print('After round', r)
    print_monkeys(ml=monkeys)

inspection_list = []
for m in monkeys:
    inspection_list.append(m.inspections)

t1, t2 = sorted(inspection_list, reverse=True)[0: 2]
print(t1 * t2)
