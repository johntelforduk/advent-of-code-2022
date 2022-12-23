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

# class Robot:
#     def __init__(self):

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
        print(blueprint_int_list)

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
        self.resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}

        self.minute = 0

        log.info('Factory created',
                 costs=self.costs,
                 robots=self.robots,
                 resource=self.resources,
                 minute=self.minute)

    def can_make_robots(self):
        """Return list of types of robot types that factory can currently make."""
        can_make = []
        for robot_type in self.costs:
            got_enough = True
            these_costs = self.costs[robot_type]
            for needed_resource in these_costs:
                if needed_resource not in self.resources:
                    got_enough = False
                elif these_costs[needed_resource] > self.resources[needed_resource]:
                    got_enough = False
            if got_enough:
                can_make.append(robot_type)
        return can_make

    def make_resources(self):
        """Make all of the current fleet of robots collect their resources."""
        for robot in self.robots:
            if robot not in self.resources:
                self.resources[robot] = self.robots[robot]
            else:
                self.resources[robot] += self.robots[robot]

    def make_a_robot(self, robot_type: str):
        # if robot_type == 'none':
        #     return
        these_costs = self.costs[robot_type]
        for needed_resource in these_costs:
            self.resources[needed_resource] -= these_costs[needed_resource]
            assert self.resources[needed_resource] >= 0

        if robot_type in self.robots:
            self.robots[robot_type] += 1
        else:
            self.robots[robot_type] = 1

def ahead(factory: Factory):
    if factory.minute not in bests_resources:
        bests_resources[factory.minute] = factory.resources
        return True

    if factory.minute not in bests_robots:
        bests_robots[factory.minute] = factory.robots
        return True

    something_ahead = False
    best = bests_resources[factory.minute]
    for resource in best:
        if factory.resources[resource] > best[resource]:
            best[resource] = factory.resources[resource]
            something_ahead = True
    if something_ahead:
        bests_resources[factory.minute] = best
        return True

    something_ahead = False
    best = bests_robots[factory.minute]
    for robot in best:
        if factory.robots[robot] > best[robot]:
            best[robot] = factory.robots[robot]
            something_ahead = True
    if something_ahead:
        bests_robots[factory.minute] = best
        return True

    return False



def another_minute(factory: Factory):


    can_make = factory.can_make_robots()
    # random.shuffle(can_make)

    factory.make_resources()

    if not ahead(factory):
        return


    if factory.minute == 24:
        if factory.resources['geode'] > 0:
            print(factory.minute, factory.resources)
        return

    factory.minute += 1

    for robot_type in can_make:
        new_factory = copy.deepcopy(factory)
        new_factory.make_a_robot(robot_type=robot_type)
        another_minute(factory=new_factory)

f = open('test1.txt')
t = f.read()
f.close()

for line in t.split('\n'):
    print(line)

    bests_resources = {}
    bests_robots = {}
    start_factory = Factory(blueprint=line)
    another_minute(factory=start_factory)

    #
    #
    #
    #
    # print(factory.can_make_robots())
    #
    # factory.make_resources()
    # print(factory.resources)
    #
    # factory.make_resources()
    # print(factory.resources)
    #
    # print(factory.can_make_robots())
    #
    # factory.make_a_robot(robot_type='clay')
    # print(factory.robots)
    # print(factory.resources)

