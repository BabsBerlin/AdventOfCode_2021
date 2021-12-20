import numpy as np
from itertools import product


# get data input
#raw_file = 'day20_test.txt'
raw_file = 'day20_f.txt'
#raw_file = 'day20.txt'

with open(raw_file) as file:
    input = file.readlines()

data = [row.strip() for row in input]
data = [[y for y in x] for x in data]
data = np.asarray(data)
# **************************************

# get decoder string
#raw_decoder = 'day20_decoder_test.txt'
raw_decoder = 'day20_decoder_f.txt'
#raw_decoder = 'day20_decoder.txt'

with open(raw_decoder) as file:
    decoder = file.readlines()
# **************************************
decoder_first = decoder[0][0]
decoder_last = decoder[0][-1]
print(f'first decoder: {decoder_first}')
print(f'last decoder: {decoder_last}')


# function to pad '.' around the image
def pad_with_point(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', '.')
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector
# **************************************


# function to pad '#' around the image
def pad_with_hash(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', '#')
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector
# **************************************


# find indices of surrounding pixels
def find_neighbors(t):
    ranges = [(x-1, x, x+1) for x in t]
    neighbors = list(product(*ranges))
    return neighbors
# **************************************


# convert binary to integer
def binary_to_decimal(binary_value):
    binary_value = '0b' + binary_value
    return int(binary_value, 2)
# *****************************************************


# convert 3x3 to number
def convert_neighbors(map, neighbors):
    binary = ''
    for n in neighbors:
        x = n[0]
        y = n[1]
        if x not in range(map.shape[0]) or y not in range(map.shape[1]):
            return None
        else:
            if map[x][y] == '#':
                binary = binary + '1'
            else:
                binary = binary + '0'
    return binary_to_decimal(binary)
# **************************************


# STEP 1: pad the data with 2 rows/cols
trench_map_1= np.pad(data, 2, pad_with_point)

#trench_map_1 = np.pad(data, 2, pad_with1)

# copy data to new map in which pixel are changed   
trench_map_1_converted = trench_map_1.copy()

# STEP 2: convert each pixel according to encoder
# the outer edge is not converted   
for index, values in np.ndenumerate(trench_map_1):
    # find neighbors
    neighbors = find_neighbors(index)
    # convert to number
    n_number = convert_neighbors(trench_map_1, neighbors)
    # map that number with encoder and change respective pixel in the new map
    if n_number:  # i.e. ignores edges
        trench_map_1_converted[index[0]][index[1]] = decoder[0][n_number]

# STEP 3: switch outer border to decoders first symbol since all '.' will be converted to that   
trench_map_1_converted[0] = decoder_first
trench_map_1_converted[-1] = decoder_first
trench_map_1_converted[:,0] = decoder_first
trench_map_1_converted[:,-1] = decoder_first

# STEP 4: pad a second time with 2 rows/cols and '#'
if decoder_first == '#':
    trench_map_2_pad= np.pad(trench_map_1_converted, 2, pad_with_hash)
else:
    trench_map_2_pad= np.pad(trench_map_1_converted, 2, pad_with_point)
    

# copy data to new map in which pixel are changed   
trench_map_final = trench_map_2_pad.copy()

# STEP 5: convert each pixel according to encoder
# the outer edge is not converted 
for index, values in np.ndenumerate(trench_map_2_pad):
    # find neighbors
    neighbors = find_neighbors(index)
    # convert to number
    n_number = convert_neighbors(trench_map_2_pad, neighbors)
    # on the edges
    if n_number:
        trench_map_final[index[0]][index[1]] = decoder[0][n_number]

# STEP 6: switch outer row/col back to '.'
trench_map_final[0] = '.'
trench_map_final[-1] = '.'
trench_map_final[:,0] = '.'
trench_map_final[:,-1] = '.'


#print('final map')
#for line in trench_map_final:
#    print(line)

count = (trench_map_final == '#').sum()
print(f'solution: {count}')
      