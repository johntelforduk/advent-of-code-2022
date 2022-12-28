# Solution to day 19 of AOC 2022,
# https://adventofcode.com/2022/day/19

import copy


def sum_ints_lt(n: int):
    return n * (n - 1) // 2


assert sum_ints_lt(1) == 0
assert sum_ints_lt(2) == 1
assert sum_ints_lt(3) == 3
assert sum_ints_lt(6) == 15


class Factory:

    def __init__(self, blueprint: str):
        blueprint_stripped = (blueprint.replace('Blueprint ', '')
                              .replace(': Each ore robot costs ', ' ')
                              .replace(' ore. Each clay robot costs ', ' ')
                              .replace(' ore. Each obsidian robot costs ', ' ')
                              .replace(' ore and ', ' ')
                              .replace(' clay. Each geode robot costs ', ' ')
                              .replace(' ore and ', ' ')
                              .replace(' obsidian.', ''))

        print(blueprint_stripped)

        blueprint_int_list = [int(quantity) for quantity in blueprint_stripped.split(' ')]

        self.blueprint_num = blueprint_int_list[0]

        # Key = robot type, Value = dict of resources needed to make 1 of this robot type.
        self.costs = {
            'ore': {'ore': blueprint_int_list[1]},
            'clay': {'ore': blueprint_int_list[2]},
            'obsidian': {'ore': blueprint_int_list[3],
                         'clay': blueprint_int_list[4]},
            'geode': {'ore': blueprint_int_list[5],
                      'obsidian': blueprint_int_list[6]},
            'none': {}}

        # Key = Resource type, the most amount of it we will even need per minute.
        # This implies the max number of this kind of robot that we'll ever need,
        self.max_needed = {'ore': max(blueprint_int_list[1],
                                      blueprint_int_list[2],
                                      blueprint_int_list[3],
                                      blueprint_int_list[5]),
                           'clay': blueprint_int_list[4],
                           'obsidian': blueprint_int_list[6]}

        # Key = robot type, value = number of these robots we currently have.
        # "Fortunately, you have exactly one ore-collecting robot in your pack that you can use to kickstart the whole
        # operation."
        self.robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}

        # Key = name of resource, Value = amount of this resource that we have at the moment.
        self.resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}

        self.minute = 0

    def can_make_robots(self) -> list:
        """Return list of types of robot types that factory can currently make."""
        can_make = []
        for robot_type in self.costs:
            got_enough = True
            robot_needs = self.costs[robot_type]
            for needed_resource in robot_needs:
                if robot_needs[needed_resource] > self.resources[needed_resource]:
                    got_enough = False
            if got_enough:
                can_make.append(robot_type)
        return can_make

    def make_resources(self):
        """Make all of the current fleet of robots create their resources."""
        for robot in self.robots:
            self.resources[robot] += self.robots[robot]

    def make_a_robot(self, robot_type: str):
        if robot_type != 'none':
            these_costs = self.costs[robot_type]
            for needed_resource in these_costs:
                self.resources[needed_resource] -= these_costs[needed_resource]
                assert self.resources[needed_resource] >= 0
            self.robots[robot_type] += 1

    def hash(self):
        """Return a hash key value on status of the robot. This can be used as a dictionary key. Robot status
        is based on amount of resources produced so far and number of robots in the estate. Hence the hash is a tuple
        consisting of each resource amount and each robot type quantity."""
        return (self.resources['ore'],
                self.resources['clay'],
                self.resources['obsidian'],
                self.resources['geode'],
                self.robots['ore'],
                self.robots['clay'],
                self.robots['obsidian'],
                self.robots['geode'])

    def render(self):
        """Print out status of current this factory."""
        print('Blueprint:', self.blueprint_num, ' Resources:', self.resources, ' Robots:', self.robots)

    def potential(self):
        """Calculate the maximum number of geodes that this factory could possibly produce. Return the sum of,
             number of geodes produced already,
             number of geodes that existing estate of geode robots will produce in the remaining time,
             number of geodes that new robots will produce, assuming that a geode robot is produced every minute
             from now on."""
        minutes_left = 1 + 32 - self.minute
        return self.resources['geode'] + self.robots['geode'] * minutes_left + sum_ints_lt(minutes_left)


def dfs(current_visited, current_factory):
    global BEST_GEODES

    # Is this the most geodes that we've seen this blueprint produce?
    if current_factory.resources['geode'] > BEST_GEODES:
        current_factory.render()
        BEST_GEODES = current_factory.resources['geode']

    # If out of time, give up.
    current_factory.minute += 1
    if current_factory.minute > 32:
        return

    if BEST_GEODES > current_factory.potential():
        return

    # Is this a state of the factory that we've seen before?
    # And if we've seen it before, was it reached in less time?... if so, end this search.
    hash_code = current_factory.hash()
    if hash_code in current_visited:
        if current_visited[hash_code] <= current_factory.minute:
            return
    current_visited[hash_code] = current_factory.minute

    # can_make = current_factory.can_make_robots()

    # In the last minute, we do not need to produce a robot, as there will be no time to use it to make resources.
    if current_factory.minute == 32:
        can_make = ['none']
    else:
        can_make = current_factory.can_make_robots()

        # Always make a geode robot whenever possible.
        if 'geode' in can_make:
            can_make = ['geode']

        else:
            # Don't bothe making robots for resource that we already have enough of.
            for check_resource in ['ore', 'clay', 'obsidian']:
                if check_resource in can_make and current_factory.robots[check_resource] >= current_factory.max_needed[check_resource]:
                    can_make.remove(check_resource)

            # In the penultimate minute, we only need to produce geode robots.
            if current_factory.minute == 31:
                if 'geode' in can_make:
                    can_make = ['geode']
                else:
                    can_make = ['none']

            # In the pre-penultimate minute, we only need to produce geode, ore, or obsidian robots (ie. no clay robots).
            elif current_factory.minute == 30:
                if 'clay' in can_make:
                    can_make.remove('clay')

    current_factory.make_resources()

    for robot_type in can_make:
        new_factory = copy.deepcopy(current_factory)
        new_factory.make_a_robot(robot_type=robot_type)
        dfs(current_visited=current_visited, current_factory=new_factory)


f = open('input.txt')
t = f.read()
f.close()

part2 = 1
for line in t.split('\n')[:3]:              # "Now, only the first three blueprints in your list are intact."
    print(line)
    a_factory = Factory(blueprint=line)
    visited = {}
    BEST_GEODES = 0
    dfs(current_visited=visited, current_factory=a_factory)

    part2 *= BEST_GEODES

print('Part 2:', part2)
