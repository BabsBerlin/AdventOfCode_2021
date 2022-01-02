#######################
# Advent of Code 2021 #
#        day 18       #
#######################
import json
import math
from itertools import permutations

#raw_file = 'day18.txt'
raw_file = 'day18_test.txt'

with open(raw_file) as file:
    input = file.readlines()

data = data = [row.strip() for row in input]
data = [json.loads(x) for x in data]


# devide the data into two lists:
# one stores the values and the other one the respective bracket level/depth
def find_level(number, level, values, levels):
    for t in number:
        if isinstance(t, int):
            levels.append(level)
            values.append(t)
        else:
            level += 1
            find_level(t, level, values, levels)
            level -= 1
    return values, levels


def explode(values, levels):
    for i, level in enumerate(levels):
        if level == 5:
            # adjust left neighbor
            if i-1 in range(len(values) - 1):
                values[i-1] += values[i]
            # adjust right neighbor
            if i+2 in range(len(values)):
                values[i+2] += values[i+1]
            # exploding pair becomes number 0
            values[i+1] = 0
            values.pop(i)
            levels[i+1] = levels[i] - 1
            levels.pop(i)
            # stop after first explosion
            return True
    return False


def split(values, levels):
    for i, value in enumerate(values):
        if value >= 10:
            # calculate new values
            value_left = value // 2
            value_right = math.ceil(value / 2)
            new_level = levels[i] + 1
            # add new values
            values[i] = value_left
            levels[i] = new_level
            values.insert(i + 1, value_right)
            levels.insert(i + 1, new_level)
            # stop after one split
            return True
    return False


def action(values, levels):
    action = True
    while action:
        explosion = True
        while explosion:
            explosion = explode(values, levels)
        if action:
            action = split(values, levels)
        else:
            action = explode(values, levels)
    return values, levels


def magnitude(values, levels):
    if len(values) == 2:
        return (3 * values[0]) + (2 * values[1])
    for i, left in enumerate(values):
        search_for_pair = True
        next = i+1
        while search_for_pair:
            if next in range(len(values)):
                if levels[i] == levels[next]:
                    right = values[next]
                    values[i] = (3 * left) + (2 * right)
                    values.pop(next)
                    levels[i] -= 1
                    levels.pop(next)
                    search_for_pair = False
                else:
                    next += 1
            else:
                search_for_pair = False
    return magnitude(values, levels)


# PART 1
# get first line
values, levels = find_level(data[0], 1, [], [])
# continue with all lines after
for line in data[1:]:
    # add new line
    temp_values, temp_levels = find_level(line, 1, [], [])
    values.extend(temp_values)
    levels.extend(temp_levels)
    levels = [x + 1 for x in levels]
    # check for explosions and splits
    values, levels = action(values, levels)

print(f'part1: the magnitude is {magnitude(values, levels)}')


# PART 2
magnitudes = []

for pair in permutations(range(len(data)), 2):
    line1 = data[pair[0]]
    line2 = data[pair[1]]
    # get first line
    values, levels = find_level(line1, 1, [], [])
    # add second line
    temp_values, temp_levels = find_level(line2, 1, [], [])
    values.extend(temp_values)
    levels.extend(temp_levels)
    levels = [x + 1 for x in levels]
    # check for explosions and splits
    values, levels = action(values, levels)

    magnitudes.append(magnitude(values, levels))

print(f'part2: the max magnitude of all combinations is {max(magnitudes)}')
