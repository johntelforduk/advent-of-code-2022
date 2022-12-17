# Solution to day 16 of AOC 2022
# https://adventofcode.com/2022/day/16

import sys
import structlog
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


def shortest(from_valve: str, to_valve: str) -> int:
    """Return the shortest time needed to travel between the parm valves."""
    # Implemented pseudo code from, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # function Dijkstra(Graph, source):

# shortest_found = sys.maxsize
# checked = 0
# for source in working_valves:
    q = q_start.copy()
    dist = dist_start.copy()
    prev = prev_start.copy()

    # dist[source] ← 0
    dist[from_valve] = 0
    q[from_valve] = 0

    # while Q is not empty:
    while len(q) != 0:

        # print('len(q):', len(q))
        # u ← vertex in Q with min dist[u]
        u = min(q, key=q.get)

        # print('u, q[u]:', u, q[u])

        # remove u from Q
        del q[u]

        # for each neighbor v of u still in Q:
        # x, y = u
        for v in network[u]:
            # v = (x + dx, y + dy)
            # climbable = False
            # if v in network:
            #     elevation = ord(network[v]) - ord(network[u])
            #     climbable = (elevation <= 1)
            #     # print(v, elevation)
            #
            # # TODO v in q yes... but also, is there a path from u to v.
            # if v in q and climbable:
                # print('v:', v)

                # print(v)
                # alt ← dist[u] + length(u, v)
                # alt = dist[u] + grid[v]
                # XXX All edges are length one in this graph!!!
            alt = dist[u] + 1


            # if alt < dist[v]:
            if alt < dist[v]:
                # dist[v] ← alt
                dist[v] = alt
                if v in q:
                    q[v] = alt
                # prev[v] ← u
                prev[v] = u

    return dist[to_valve]
    # return dist[], prev[]
#     checked += 1
#     shortest_found = min(shortest_found, dist[target])
#     print('Checked, len(sources), shortest:', checked, len(working_valves), shortest_found)
#
# print(shortest_found)


f = open('input.txt')
t = f.read()
f.close()

# Network is Key=valve letters, Value = list valve letters that can be directly reached from it.
# working_valve is list of tuples, (valve letters, flow rate)
network, working_valves = {}, {}

for row in t.split('\n'):
    abridged = (row.replace('Valve ', '')
                .replace('has flow rate=', '')
                .replace('; tunnels lead to valves', '')
                .replace('; tunnel leads to valve', '')
                .replace(',', ''))
    abridged_list = abridged.split(' ')
    try_valve = abridged_list.pop(0)

    flow_rate = int(abridged_list.pop(0))

    network[try_valve] = abridged_list

    if flow_rate > 0:
        working_valves[try_valve] = flow_rate

    log.info('Parsed row',
             row=row,
             abridged=abridged,
             valve=try_valve,
             flow_rate=flow_rate,
             abridged_list=abridged_list)


    # for elevation in row:
    #     if elevation in ['a', 'S']:
    #         network[grid_x, grid_y] = 'a'
    #         working_valves.append((grid_x, grid_y))
    #     elif elevation == 'E':
    #         network[grid_x, grid_y] = 'z'
    #         target = (grid_x, grid_y)
    #     else:
    #         network[grid_x, grid_y] = elevation
    #
    #     grid_x += 1
    # grid_y += 1

log.info('File read',
         working_valves=working_valves,
         network=network,
         len_working_valves=len(working_valves))

# create vertex set Q
q_start, dist_start, prev_start = {}, {}, {}
# for each vertex v in Graph:
for v in network:
    # dist[v] ← INFINITY
    dist_start[v] = sys.maxsize
    # prev[v] ← UNDEFINED
    prev_start[v] = None
    # add v to Q
    q_start[v] = dist_start[v]

short_cache = {}
visitable_valves = working_valves.copy()
visitable_valves['AA'] = 0

for f in visitable_valves:
    for t in working_valves:
        if f != t:
            short_cache[f, t] = shortest(f, t)


def total_pressure(visit_order: list) -> int:
    time_remaining = 26
    current_valve = 'AA'

    pressure = 0
    for next_valve in visit_order:
        distance = short_cache[current_valve, next_valve]
        flow_rate = working_valves[next_valve]
        time_remaining -= (distance + 1)
        if time_remaining > 0:
            pressure += time_remaining * flow_rate     # The -1 is for the time needed to open the valve.
        current_valve = next_valve

    return pressure

def swap(l, pos1, pos2):
    l[pos1], l[pos2] = l[pos2], l[pos1]
    return l

assert swap([1, 2, 3, 4, 5], 1, 3) == [1, 4, 3, 2, 5]
assert swap([5, 4, 3, 2, 1], 4, 0) == [1, 4, 3, 2, 5]


def time_to_visit(l: list) -> int:
    current_valve = 'AA'
    total_time = 0
    for valve in l:
        total_time += short_cache[current_valve, valve] + 1
        current_valve = valve
    return total_time

# print(time_to_visit(['BB']))

# for i in range(len(try_order)):
#     for j in range(len(try_order)):
#         if i != j:
#             curr_pressure = total_pressure(try_order)
#             try_order = swap(try_order, i, j)
#             try_pressure = total_pressure(try_order)
#             if try_pressure < curr_pressure:        # If it was better before trying the swap, put it back the way it was.
#                 try_order = swap(try_order, i, j)
#             print(try_order, curr_pressure, try_pressure)
#
# print(total_pressure(try_order))

try_valves = []
for valve in working_valves:
    try_valves.append(valve)

print(try_valves)

very_best = 0

while True:
    available = try_valves.copy()

    me_valves, elephant_valves = [], []
    # print(time_to_visit(me_valves))
    while len(available) > 0 and min(time_to_visit(me_valves), time_to_visit(elephant_valves)) < 26:
        if time_to_visit(me_valves) < 26:
            me_valves.append(available.pop(random.randrange(len(available))))

        if time_to_visit(elephant_valves) < 26:
            elephant_valves.append(available.pop(random.randrange(len(available))))

    best = total_pressure(me_valves) + total_pressure(elephant_valves)

    same_run = 0
    while same_run < 1000:
        choice = random.randrange(3)
        if choice == 0:
            i, j = random.randrange(len(me_valves)), random.randrange(len(me_valves))
            me_valves = swap(me_valves, i, j)
        elif choice == 1:
            i, j = random.randrange(len(elephant_valves)), random.randrange(len(elephant_valves))
            elephant_valves = swap(elephant_valves, i, j)
        else:
            i, j = random.randrange(len(me_valves)), random.randrange(len(elephant_valves))
            x = me_valves[i]
            me_valves[i] = elephant_valves[j]
            elephant_valves[j] = x

        new_pressure = total_pressure(me_valves) + total_pressure(elephant_valves)
        if new_pressure > best:
            best = new_pressure
            if best > very_best:
                very_best = best
                print(very_best)
            same_run = 0
        else:
            same_run += 1
            if choice == 0:
                me_valves = swap(me_valves, i, j)
            elif choice == 1:
                elephant_valves = swap(elephant_valves, i, j)
            else:
                x = me_valves[i]
                me_valves[i] = elephant_valves[j]
                elephant_valves[j] = x
