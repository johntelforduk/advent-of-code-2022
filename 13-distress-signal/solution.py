# Solution to day 13 of AOC 2022
# https://adventofcode.com/2022/day/13

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




def check_order(p1, p2) -> str:

    # If both values are integers,
    if type(p1) == type(p2) == int:
        # the lower integer should come first. If the left integer is lower than the right integer, the inputs are in
        # the right order.
        if p1 < p2:
            return "right"

        # If the left integer is higher than the right integer, the inputs are not in the right order.
        elif p1 > p2:
            return "wrong"

        else:
            # Otherwise, the inputs are the same integer; continue checking the next part of the input.
            return "continue"

    # If exactly one value is an integer, convert the integer to a list which contains that integer as its only value,
    # then retry the comparison.
    if type(p1) is int:
        return check_order([p1], p2)
    elif type(p2) is int:
        return check_order(p1, [p2])

    assert type(p1) == type(p2) == list
    # If the left list runs out of items first, the inputs are in the right order.
    if len(p1) == 0 and len(p2) > 0:
        return "right"
    # If the right list runs out of items first, the inputs are not in the right order.
    elif len(p2) == 0 and len(p1) > 0:
        return "wrong"
    # If the lists are the same length and no comparison makes a decision about the order,
    # continue checking the next part of the input.
    elif len(p1) == len(p2) == 0:
        return "continue"

    p1, p2 = p1.copy(), p2.copy()           # Not sure this is necessary.
    h1, h2 = p1.pop(0), p2.pop(0)
    result = check_order(h1, h2)
    if result != 'continue':
        return result
    else:
        return check_order(p1, p2)


def lowest(p: list) -> (list, list):
    """For parm list of lists, return lowest list, and remainder of parm list."""
    if len(p) == 1:
        return p[0], []

    p = p.copy()
    best = p[0]
    for i in range(1, len(p)):
        if check_order(best, p[i]) == "wrong":
            best = p[i]

    p.remove(best)
    return best, p


assert check_order([1,1,3,1,1], [1,1,5,1,1]) == "right"
assert check_order([[1],[2,3,4]],  [[1],4]) == "right"
assert check_order([9], [[8,7,6]]) == "wrong"
assert check_order([[4,4],4,4],  [[4,4],4,4,4]) == "right"
assert check_order([7,7,7,7], [7,7,7]) == "wrong"
assert check_order([], [3]) == "right"
assert check_order([[[]]],  [[]]) == "wrong"
assert check_order([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]) == "wrong"

f = open('input.txt')
t = f.read()
f.close()

part1 = 0
index = 1
d1, d2 = [[2]], [[6]]
packets = [d1, d2]
for pair in t.split('\n\n'):
    # print(pair)

    s1, s2 = pair.split('\n')
    l1, l2 = eval(s1), eval(s2)
    packets.append(l1)
    packets.append(l2)

    check = check_order(l1, l2)
    print(l1, l2, check)

    if check == "right":
        part1 += index

    index += 1


print(packets)
sorted_packets = []
while len(packets) > 0:
    this_lowest, packets = lowest(packets)
    sorted_packets.append(this_lowest)

i1, i2 = sorted_packets.index(d1) + 1, sorted_packets.index(d2) + 1

print('Part 1:', part1)
print('Part 2:', i1 * i2)
