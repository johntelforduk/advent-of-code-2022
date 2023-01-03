# Solution to day 25 of AOC 2022,
# https://adventofcode.com/2022/day/25

def dec_to_base(n: int, b: int):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def base_five_digit_to_snafu(d: int) -> (str, str):
    conversion = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, -2), 4: (1, -1),
                  5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (2, -2), 9: (2, -1)}
    return conversion[d]


def snafu_to_decimal(s: str) -> int:
    conversion = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    dec = 0
    for i in s:
        dec *= 5
        dec += conversion[i]
    return dec


def decimal_to_snafu(dec: int) -> str:
    to_b5 = dec_to_base(dec, 5)

    carry = 0
    result = []
    for d in to_b5[::-1]:
        d += carry
        carry, this_unit = base_five_digit_to_snafu(d)

        result.append(this_unit)

    if carry > 0:
        result.append(carry)

    d_to_s_digit = {2: '2', 1: '1', 0: '0', -1: '-', -2: '='}
    snafu = ''
    for d in result[::-1]:
        snafu = snafu + d_to_s_digit[d]
    return snafu


f = open('input.txt')
t = f.read()
f.close()

total = 0
for s in t.split('\n'):

    s_to_d = snafu_to_decimal(s)
    b5 = dec_to_base(s_to_d, 5)

    total += snafu_to_decimal(s)

print('Part 1:', decimal_to_snafu(total))
