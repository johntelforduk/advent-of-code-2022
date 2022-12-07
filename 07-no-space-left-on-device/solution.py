# Solution to day 7 of AOC 2022,
# https://adventofcode.com/2022/day/7

def all_the_dirs(s: str) -> list:
    r = []
    for i in range(len(s)):
        if s[i] == '/':
            r.append(s[0: i + 1])
    return r


class FileSystem:

    def __init__(self):
        self.prefix = '/'

        # key = object prefix + filename, value = size.
        self.files = {}

    def cd(self, arg: str):
        if arg == '/':
            # cd / switches the current directory to the outermost directory, /.
            self.prefix = '/'

        elif arg == '..':
            # cd .. moves out one level: it finds the directory that contains the current directory, then makes that
            # directory the current directory.
            last_fslash = self.prefix[:-1].rfind('/')
            self.prefix = self.prefix[0: last_fslash + 1]

        else:
            # cd x moves in one level: it looks in the current directory for the directory named x and makes it
            # the current directory.
            self.prefix += arg + '/'

    def add_file(self, fn: str, size: int):
        self.files[self.prefix + fn] = size


test_fs = FileSystem()
assert test_fs.prefix == '/'
test_fs.cd('adir')
assert test_fs.prefix == '/adir/'
test_fs.add_file(fn='john', size=1024)
assert '/adir/john' in test_fs.files
test_fs.cd('bdir')
assert test_fs.prefix == '/adir/bdir/'
test_fs.cd('..')
assert test_fs.prefix == '/adir/'
test_fs.cd('/')
assert test_fs.prefix == '/'

assert all_the_dirs(s='/a.txt') == ['/']
assert all_the_dirs(s='/abc/def/john.txt') == ['/', '/abc/', '/abc/def/']

f = open('input.txt')
t = f.read()
f.close()

fs = FileSystem()
for line in t.split('\n'):
    terms = line.split(' ')
    if terms[0] == '$' and terms[1] == 'cd':
        fs.cd(terms[2])

    elif terms[0] not in ['$', 'dir']:
        fs.add_file(fn=terms[1], size=int(terms[0]))

dir_sizes = {}
for file in fs.files:
    print(file)

    for d in all_the_dirs(s=file):
        if d in dir_sizes:
            dir_sizes[d] = dir_sizes[d] + fs.files[file]
        else:
            dir_sizes[d] = fs.files[file]

print(dir_sizes)

unused = 70000000 - dir_sizes['/']
print(unused)
required = 30000000 - unused
print(required)

part1, part2 = 0, 70000000
for d in dir_sizes:
    s = dir_sizes[d]
    if s <= 100000:
        part1 += s
    if required <= s < part2:
        part2 = s

print('Part 1:', part1)
print('Part 2:', part2)
