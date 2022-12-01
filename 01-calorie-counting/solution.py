# Solution to day 1 of AOC 2022,
# https://adventofcode.com/2022/day/1

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

elves = t.split('\n\n')
total_cals = []
for elf in elves:
    cals = 0
    for food in elf.split('\n'):
        cals += int(food)
    total_cals.append(cals)

print('Part 1:', max(total_cals))
print('Part 2:', sum(sorted(total_cals, reverse=True)[:3]))
