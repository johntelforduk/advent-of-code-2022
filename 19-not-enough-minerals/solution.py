# Solution to day 19 of AOC 2022,
# https://adventofcode.com/2022/day/19

import structlog
import copy
import random

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
        # print(blueprint_int_list)

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

        # Key = robot type, value = number of these robots we currently have.
        # "Fortunately, you have exactly one ore-collecting robot in your pack that you can use to kickstart the whole
        # operation."
        self.robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0, 'none': 0}

        # Key = name of resource, Value = amount of this resource that we have at the moment.
        self.resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0, 'none': 0}

        self.minute = 0
        self.max_geodes = 0

        log.info('Factory created',
                 costs=self.costs,
                 robots=self.robots,
                 resource=self.resources,
                 minute=self.minute)

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
        return hash(frozenset(self.resources.items())) + 147 * hash(frozenset(self.robots.items()))

    def render(self):
        """Print out status of current this factory."""
        print('Blueprint:', self.blueprint_num, ' Resources:', self.resources, ' Robots:', self.robots)

    def potential(self):
        minutes_left = 1 + 24 - self.minute
        return self.robots['obsidian'] * minutes_left + sum_ints_lt(minutes_left)

def best(factory: Factory):
    # if factory.minute not in explored:
    #     explored.add((factory.resources, factory.robots))
    #     return True

    global explored
    global Q

    hash_key = hash_factory(factory)

    if hash_key not in explored:
        explored[hash_key] = factory
        return True

    prev_best_mins = explored[hash_key].minute
    if factory.minute < prev_best_mins:

        explored[hash_key] = factory
        Q[hash_key] = factory
        return True



    return False
    # # if factory.minute not in bests_robots:
    # #     bests_robots[factory.minute] = factory.robots
    # #     return True
    #
    # best = bests_resources[factory.minute]
    # for resource in best:
    #     if factory.resources[resource] > best[resource]:
    #         best[resource] = factory.resources[resource]
    #         bests_resources[factory.minute] = best
    #         # print(factory.minute, bests_resources)
    #         return True
    #
    # best = bests_robots[factory.minute]
    # for robot in best:
    #     if factory.robots[robot] > best[robot]:
    #         best[robot] = factory.robots[robot]
    #         bests_robots[factory.minute] = best
    #         # print(factory.minute, bests_robots)
    #
    #         return True
    #
    # return False


# procedure DFS_iterative(G, v) is
# def dfs_iterative(g: Factory):
#
# #     let S be a stack
#     S = {}
#
# #     label v as discovered
#     hash = hash_factory(g)
#     S[hash] = 'discovered'
#
#
#     for
# #     S.push(iterator of G.adjacentEdges(v))
# #     while S is not empty do
# #         if S.peek().hasNext() then
# #             w = S.peek().next()
# #             if w is not labeled as discovered then
# #                 label w as discovered
# #                 S.push(iterator of G.adjacentEdges(w))
# #         else
# #             S.pop()
#
#


def another_minute(factory: Factory):
    if factory.minute == 24:
        return

    factory.minute += 1

    global DEPTH
    global Q
    if factory.minute > DEPTH:
        DEPTH = factory.minute
    print(DEPTH, len(Q))

    # print(len(Q), factory.minute, 'Robots:', factory.robots, 'Resources:', factory.resources)

    can_make = factory.can_make_robots()

    factory.make_resources()

    for robot_type in can_make:
        new_factory = copy.deepcopy(factory)
        new_factory.make_a_robot(robot_type=robot_type)

        best(new_factory)


def dfs(current_visited, current_factory):
    global BEST_GEODES

    # if current_factory.minute == 23 and current_factory.robots['geode'] == 0:
    #     return

    if BEST_GEODES > current_factory.potential():
        # print('.', end='')
        return

    if current_factory.resources['geode'] > BEST_GEODES:
        current_factory.render()
        BEST_GEODES = current_factory.resources['geode']
    # current_factory.render()

    current_factory.minute += 1
    if current_factory.minute > 24:
        return

    hash_code = current_factory.hash()
    if hash_code in current_visited:
        if current_visited[hash_code] <= current_factory.minute:
            return

    current_visited[hash_code] = current_factory.minute

    can_make = current_factory.can_make_robots()
    current_factory.make_resources()

    for robot_type in can_make:
        new_factory = copy.deepcopy(current_factory)
        new_factory.make_a_robot(robot_type=robot_type)
        # new_visited = copy.copy(current_visited)
        dfs(current_visited=current_visited, current_factory=new_factory)
    # for neighbour in graph[node]:
    #     dfs(visited, graph, neighbour)


f = open('test1.txt')
t = f.read()
f.close()

part1 = 0
for line in t.split('\n'):
    print(line)
    a_factory = Factory(blueprint=line)
    visited = {}
    BEST_GEODES = 0
    dfs(current_visited=visited, current_factory=a_factory)

    part1 += a_factory.blueprint_num * BEST_GEODES

print('Part 1:', part1)

#
#
#
#     geodes = 0
#     start_factory = Factory(blueprint=line)
#     hashed = hash_factory(start_factory)
#
#     Q = {}
#     Q[hashed] = start_factory
#
#     explored = {}
#
#     DEPTH = 0
#     while len(Q) > 0:
#         # print(len(Q))
#         next_factory_hash = next(iter(Q))
#         next_factory = Q[next_factory_hash]
#         Q.pop(next_factory_hash)
#
#
#
#         another_minute(factory=next_factory)
#         if next_factory.resources['geode'] > geodes:
#             geodes = next_factory.resources['geode']
#
#     print(geodes)
#     part1 += start_factory.blueprint_num * geodes
# #
# print(part1)
#
# # f1 = Factory('Blueprint 3: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 14 clay. Each geode robot costs 2 ore and 16 obsidian.')
# # f2 = copy.copy(f1)
# #
# # f1.robots = {'ore': 1, 'clay': 2, 'obsidian': 3, 'geode': 4, 'none': 5}
# # f2.robots = {'ore': 5, 'clay': 4, 'obsidian': 3, 'geode': 4, 'none': 5}
# #
# # print(f1.robots)
# # print(f2.robots)
