# Solution to day 12 of AOC 2022
# https://adventofcode.com/2022/day/12

import sys
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

grid, source, target = {}, (0, 0), (0, 0)

grid_x, grid_y = 0, 0
for row in t.split('\n'):
    grid_x = 0
    for elevation in row:
        if elevation == 'S':
            grid[grid_x, grid_y] = 'a'
            source = (grid_x, grid_y)
        elif elevation == 'E':
            grid[grid_x, grid_y] = 'z'
            target = (grid_x, grid_y)
        else:
            grid[grid_x, grid_y] = elevation

        grid_x += 1
    grid_y += 1

# Fix a gatepost error.
grid_x -= 1
grid_y -= 1

log.info('Grid loaded',
         grid_x=grid_x,
         grid_y=grid_y,
         source=source,
         target=target)


# Implemented pseudo code from, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# function Dijkstra(Graph, source):
#
# create vertex set Q
q, dist, prev = {}, {}, {}
# for each vertex v in Graph:
for v in grid:
    # dist[v] ← INFINITY
    dist[v] = sys.maxsize
    # prev[v] ← UNDEFINED
    prev[v] = None
    # add v to Q
    q[v] = dist[v]
# dist[source] ← 0
dist[source] = 0
q[source] = 0

# while Q is not empty:
while len(q) != 0:

    print('len(q):', len(q), q)
    # u ← vertex in Q with min dist[u]
    u = min(q, key=q.get)

    print('u, q[u]:', u, q[u])

    # remove u from Q
    del q[u]

    # for each neighbor v of u still in Q:
    x, y = u
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        v = (x + dx, y + dy)
        climbable = False
        if v in grid:
            elevation = ord(grid[v]) - ord(grid[u])
            climbable = (elevation <= 1)
            print(v, elevation)

        # TODO v in q yes... but also, is there a path from u to v.
        if v in q and climbable:
            print('v:', v)

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

# return dist[], prev[]
print(dist[target])
