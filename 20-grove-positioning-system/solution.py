# Solution to day 20 of AOC 2022,
# https://adventofcode.com/2022/day/20

f = open('input.txt')
t = f.read()
f.close()


def singly_linked_list(start: list) -> dict:
    linked_list, prev = {}, None
    for i in start:
        if prev is None:
            linked_list[i] = start[len(start) - 1]
        else:
            linked_list[i] = prev
        prev = i
    return linked_list


class Circle:
    def __init__(self, start: list):

        # Key = value of item in circle.
        # Value = (before, next)... links in both directions.
        self.graph = {}

        backwards = singly_linked_list(start)
        other_way = start.copy()
        other_way.reverse()
        forwards = singly_linked_list(other_way)

        for i in backwards:
            b = backwards[i]
            f = forwards[i]
            self.graph[i] = (b, f)

    def render(self):
        start = next(iter(self.graph))
        item = start
        print(item, end=' ')
        _, item = self.graph[item]
        while item != start:
            print(item, end=' ')
            _, item = self.graph[item]

        print()

    def move_forwards(self, s):
        sm1, sp1 = self.graph[s]
        _, sp2 = self.graph[sp1]

        sm1_b, sm1_f = self.graph[sm1]
        self.graph[sm1] = (sm1_b, sp1)

        # sp1_b, sp1_f = self.graph[sp1]
        self.graph[sp1] = (sm1, s)

        _, s_f = self.graph[s]
        self.graph[s] = (s_f, sp2)

        _, sp2_f = self.graph[sp2]
        self.graph[sp2] = (s, sp2_f)

    def move_backwards(self, s):
        sm1, sp1 = self.graph[s]
        sm2, _ = self.graph[sm1]

        sm2_b, sm2_f = self.graph[sm2]
        self.graph[sm2] = (sm2_b, s)

        sm1_b, sm1_f = self.graph[sm1]
        self.graph[sm1] = (s, sp1)

        s_b, s_f = self.graph[s]
        self.graph[s] = (sm2, sm1)

        sp1_b, sp1_f = self.graph[sp1]
        self.graph[sp1] = (sm1, sp1_f)

    def after_zero(self, n: int) -> int:
        current = 0
        for i in range(n):
            _, current = self.graph[current]
        return current


encrypted = [int(line) for line in t.split('\n')]
print(encrypted)
circle = Circle(start=encrypted)
# circle.render()

unique = set()
for i in encrypted:
    if i in unique:
        print(i)
    unique.add(i)
    for j in range(abs(i)):
        if i > 0:
            circle.move_forwards(i)
        else:
            circle.move_backwards(i)

print(len(unique))

# circle.render()
print(circle.after_zero(n=1000) + circle.after_zero(n=2000) + circle.after_zero(n=3000))



# circle.move_backwards(4)
# circle.move_backwards(4)
#
# circle.move_forwards(4)
# # circle.move_forwards(4)

# circle.render()

# print(circle.graph)
# print()

# print(encrypted)
# mixed = encrypted.copy()
#
# def move(circle: list, subject: int) -> list:
#
#     subject_pos = circle.index(subject)
#
#     new_pos = 1 + subject_pos + subject
#     if new_pos < 0:
#         new_pos = new_pos % (len(circle)) - 1
#     elif new_pos > len(circle) + 1:
#         new_pos = new_pos % (len(circle)) - 1
#
#
#     circle[subject_pos] = 'xxx'
#     circle.insert(new_pos, subject)
#     circle.remove('xxx')
#     print(subject, circle)
#     return circle
#
#
# mixed = move(mixed, 1)
# # print(mixed)
# mixed = move(mixed, 2)
# # print(mixed)
# mixed = move(mixed, -3)
# # print(mixed)
# mixed = move(mixed, 3)
# # print(mixed)
# mixed = move(mixed, -2)
# # print(mixed)
