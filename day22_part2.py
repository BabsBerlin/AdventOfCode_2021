#######################
# Advent of Code 2021 #
#   day 22 - part2    #
#######################

'''
This one was BAD, had to heavily rely on hints to solve it.
I am sure some parts can be optimized, i.e. written smarter, but I am not going to touch it ever again. ;-)
'''

import numpy as np
import time
start_time = time.time()

raw_file = 'day22.txt'
#raw_file = 'day22_test2.txt'

with open(raw_file) as file:
    data = [row.strip() for row in file.readlines()]


# function to extract coordinates
def extract_coords(x, start_coordinates):
    # extract the start and end x,y,z coordinates
    x, y, z = [c[2:].split('..') for c in x[start_coordinates:].split(',')]
    cuboid = (int(x[0]), int(y[0]), int(z[0]), int(x[1]), int(y[1]), int(z[1]))
    return cuboid


# check if the new_cuboid is intersecting with an existing one, i.e. needs clipping
def do_they_intersect(new_cuboid, old_cuboid):
    x_min, y_min, z_min, x_max, y_max, z_max = old_cuboid
    x_min_NEW, y_min_NEW, z_min_NEW, x_max_NEW, y_max_NEW, z_max_NEW = new_cuboid
    if x_min <= x_max_NEW and y_min <= y_max_NEW and z_min <= z_max_NEW \
            and x_min_NEW <= x_max and y_min_NEW <= y_max and z_min_NEW <= z_max:
        return True
    else:
        return False

cuboids = set()

# for each line of the input
for line in data:
    # extract the cuboid data: x,y,z start and end
    if 'on' in line:
        new_cuboid = extract_coords(line, 3)
    else:
        new_cuboid = extract_coords(line, 4)

    x_min_NEW, y_min_NEW, z_min_NEW, x_max_NEW, y_max_NEW, z_max_NEW = new_cuboid

    # add first cuboid
    if cuboids == set():
        cuboids.add(new_cuboid)
    # from line two on
    else:
        temp_cuboids = set()
        # loop through each existing cuboit
        for c in cuboids:
            # check if it interferes with the new cuboid
            if do_they_intersect(new_cuboid, c):
                x_min, y_min, z_min, x_max, y_max, z_max = c

                # if so, clip out the new cuboid out of the existing one:
                # *** x ***
                if x_min <= x_min_NEW <= x_max:
                    temp_cuboids.add((x_min, y_min, z_min, x_min_NEW-1, y_max, z_max))
                    x_min = x_min_NEW
                if x_min <= x_max_NEW <= x_max:
                    temp_cuboids.add((x_max_NEW+1, y_min, z_min, x_max, y_max, z_max))
                    x_max = x_max_NEW

                # *** y ***
                if y_min <= y_min_NEW <= y_max:
                    temp_cuboids.add((x_min, y_min, z_min, x_max, y_min_NEW-1, z_max))
                    y_min = y_min_NEW
                if y_min <= y_max_NEW <= y_max:
                    temp_cuboids.add((x_min, y_max_NEW+1, z_min, x_max, y_max, z_max))
                    y_max = y_max_NEW

                # *** z ***
                if z_min <= z_min_NEW <= z_max:
                    temp_cuboids.add((x_min, y_min, z_min, x_max, y_max, z_min_NEW-1))
                    z_min = z_min_NEW
                if z_min <= z_max_NEW <= z_max:
                    temp_cuboids.add((x_min, y_min, z_max_NEW+1, x_max, y_max, z_max))
                    z_max = z_max_NEW
            else:
                temp_cuboids.add(c)
        if temp_cuboids:
            cuboids = temp_cuboids

        # after all the clipping, add the new cuboid if it was supposed to be "on"
        if 'on' in line:
            cuboids.add(new_cuboid)

volume = 0
for cube in cuboids:
    volume += ((cube[3] - cube[0])+1) * ((cube[4] - cube[1])+1) * ((cube[5] - cube[2])+1)

print(f'volume: {volume}')

print("--- %s seconds ---" % round((time.time() - start_time), 6))
