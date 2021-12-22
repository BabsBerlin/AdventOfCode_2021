#######################
# Advent of Code 2021 #
#   day 22 - part1    #
#######################

import numpy as np
import itertools
import time
start_time = time.time()

# raw_file = 'day22.txt'
raw_file = 'day22_test2.txt'

with open(raw_file) as file:
    input = file.readlines()

data = [row.strip() for row in input]


# function to extract coordinates
def extract_coords(x, start_coordinates):
    # extract the min max values for the coordinate ranges
    x = [c[2:].split('..') for c in x[start_coordinates:].split(',')]
    # create all coordinates
    temp = []
    for s in x:
        s = [*range(int(s[0]), int(s[1])+1)]
        temp.append(s)
    return list(itertools.product(*temp))


final_coords = set()
for line in data:
    # print(line)
    if 'on' in line:
        final_coords.update(extract_coords(line, 3))
    else:
        off_coords = extract_coords(line, 4)
        final_coords = {x for x in final_coords if x not in off_coords}


print(len(final_coords))
print("--- %s seconds ---" % round((time.time() - start_time), 6))
