# Solution to day 20 of AOC 2022,
# https://adventofcode.com/2022/day/20

class Circle:
    def __init__(self, text: str):

        self.encrypted = []
        position = 0
        for line in text.split('\n'):
            pair = (811589153 * int(line), position)
            self.encrypted.append(pair)
            if line == '0':
                self.zero = pair
            position += 1

    def render(self):
        # print(self.encrypted)
        for value, _ in self.encrypted:
            print(value, end=' ')
        print()

    def move(self, subject, n: int):
        curr_pos = self.encrypted.index(subject)

        n = n % (len(self.encrypted) - 1)
        new_pos = curr_pos + n + 1

        if new_pos > len(self.encrypted):
            new_pos -= len(self.encrypted)

        self.encrypted.insert(new_pos, (99999999, 99999999))
        self.encrypted.remove(subject)
        position = self.encrypted.index((99999999, 99999999))
        self.encrypted[position] = subject

    def after_zero(self, n: int) -> int:
        pos = self.encrypted.index(self.zero)
        pos = (pos + n) % len(self.encrypted)

        value, _ = self.encrypted[pos]
        return value


f = open('input.txt')
t = f.read()
f.close()
circle = Circle(text=t)

start = circle.encrypted.copy()
for mix in range(10):
    for i in start:
        num, _ = i
        circle.move(subject=i, n=num)

print('Part 2:', circle.after_zero(n=1000) + circle.after_zero(n=2000) + circle.after_zero(n=3000))
