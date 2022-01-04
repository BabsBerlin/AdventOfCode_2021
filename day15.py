#######################
# Advent of Code 2021 #
#       day 15        #
#######################

import heapq

'''
PART 2:
the full map of the cave for part2 is generated in day15_helper.py
it is saved to the file 'day15_big_data.txt'
'''

#raw_file = 'day15_big_data.txt'
raw_file = 'day15.txt'

with open(raw_file) as file:
    data = [row.strip() for row in file.readlines()]


def find_neighbors(x, y):
    all_neighbors = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
    neighbors = []
    for n in all_neighbors:
        if n[0] in range(len(data)) and n[1] in range(len(data)):
            neighbors.append(n)
    return neighbors


def find_shortest_path(data):
    start = (0, 0)
    end = (len(data) - 1, len(data[0]) - 1)
    dist_queue = [(0, start)]

    # initialize queue with shortest part, containing start position
    dist_queue = [(0, start)]
    visited = set()
    # initialize a risk_matrix with high values each, 0 at the start
    risk_matrix = [[99999 for _ in range(len(data[0]))] for _ in range(len(data))]
    risk_matrix[0][0] = 0

    while dist_queue:
        # get shortest path so far from the queue
        dist, node = heapq.heappop(dist_queue)

        # when we reach the end position, return the lowest distance
        if node == end:
            return dist

        # if the were already there, go to next
        if node in visited:
            continue

        # mark node as visited and retrieve indices
        visited.add(node)
        row, col = node

        # check neighbors for shorter distance
        neighbors = find_neighbors(row, col)
        for neighbor in neighbors:
            n_row, n_col = neighbor[0], neighbor[1]
            newdist = dist + int(data[n_row][n_col])

            if newdist < risk_matrix[n_row][n_col]:
                risk_matrix[n_row][n_col] = newdist
                heapq.heappush(dist_queue, (newdist, neighbor))


shortest_path = find_shortest_path(data)

print(f'shortest path: {shortest_path}')
