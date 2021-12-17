#######################
# Advent of Code 2021 #
#       day 17        #
#######################

#run = 'test'
run = 'real'

if run == 'test':
    # target area: x=20..30, y=-10..-5
    x_target_end = 30
    x_target_range = range(20, 31)
    y_target_start = -4
    y_target_end = -11
    y_target_range = range(-4, -11)
    # starting velocities
    x_velocity = -1
    y_velocity = -20
    # maximum range for outer loop
    loop_max_range = 50
else:
    # target area: x=94..151, y=-156..-103
    x_target_end = 151
    x_target_range = range(94, 152)
    y_target_start = -102
    y_target_end = -157
    y_target_range = range(-102, -157)
    x_velocity = -1
    y_velocity = -200
    loop_max_range = 400


# check if the probe is hitting the target zone
def hits_target(x, y):
    if x in x_target_range and y < y_target_start and y > y_target_end:
        return True
    else:
        return False


# returns TRUE when there is still a chance to hit the target
# and FALSE when we are beyond the target, i.e. no way to ever reach it
def still_in_range(x, y):
    if x < x_target_end and y > y_target_end:
        return True
    else:
        return False


# each step changes the position of the probe
# and then calculates new velocities with drag and gravity parameters
def step(x, y, x_velocity, y_velocity):
    x += x_velocity
    y += y_velocity
    if x_velocity > 0:
        x_velocity -= 1
    elif x_velocity < 0:
        x_velocity += 1
    y_velocity -= 1
    return x, y, x_velocity, y_velocity


def velocity_loop(x, y, x_velocity, y_velocity):
    global highest_y_list
    highest_y = 0
    while True:
        x, y, x_velocity, y_velocity = step(x, y, x_velocity, y_velocity)
        if y > highest_y:
                highest_y = y
        # check if we've hit the target
        if hits_target(x, y) is True:
            highest_y_list.append(highest_y)
            break
        # check if we're out of range
        if still_in_range(x, y) is False:
            velocities.pop()
            break


highest_y_list = []
velocities = []

initial_x_velocity = x_velocity
initial_y_velocity = y_velocity


for i in range(1, loop_max_range):
    for ii in range(1, loop_max_range):
        # initialize start position for each loop
        x = 0
        y = 0

        # add start velocities to list
        # it will be poped out if the probe is out of range
        velocities.append([x_velocity, y_velocity])

        # find out if this initial velocities propels the probe into the target or not
        velocity_loop(x, y, x_velocity, y_velocity)

        # try next velocities
        x_velocity = initial_x_velocity + i
        y_velocity = initial_y_velocity + ii

print(f'highest y: {max(highest_y_list)}')
print(f'velocities: {len(velocities)}')
