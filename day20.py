import numpy as np
from itertools import product


# get data input
#raw_file = 'day20_test.txt'
#raw_file = 'day20_f.txt'
raw_file = 'day20.txt'

with open(raw_file) as file:
    input = file.readlines()

data = [row.strip() for row in input]
data = [[y for y in x] for x in data]
data = np.asarray(data)
print(f'original shape: {data.shape}')
for line in data:
    print(line)
# **************************************

count = (data == '#').sum()
print(f'solution: {count}')
# get decoder string
#raw_decoder = 'day20_decoder_test.txt'
#raw_decoder = 'day20_decoder_f.txt'
raw_decoder = 'day20_decoder.txt'

with open(raw_decoder) as file:
    decoder = file.readlines()

#print(decoder)
print(len(decoder[0]))
# **************************************


# function to pad '.' around the image
def pad_with1(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', '.')
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector
# **************************************

# function to pad '#' around the image
def pad_with2(vector, pad_width, iaxis, kwargs):
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


# convert binary to integer - has to be inputted as string because of the leading zeros!
def binary_to_decimal(binary_value):
    binary_value = '0b' + binary_value
    return int(binary_value, 2)
# *****************************************************


# convert 3x3 to number
def convert_neighbors(map, neighbors):
    #s = ''
    binary = ''
    for n in neighbors:
        x = n[0]
        y = n[1]
        if x not in range(map.shape[0]) or y not in range(map.shape[1]):
            return None
        else:
            #s = s + data[x][y]
            if map[x][y] == '#':
                binary = binary + '1'
            else:
                binary = binary + '0'
    return binary_to_decimal(binary)
# **************************************



# STEP 1: pad the data with 2 rows/cols using '.'
trench_map_1 = np.pad(data, 2, pad_with1)
print(f'shape padded: {trench_map_1.shape}')
#for line in trench_map_1:
#    print(line)
# **************************************


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

#for line in trench_map_1_converted:
#    print(line) 

# STEP 3: switch outer border to '#' since all zeros will be converted to that   
trench_map_1_converted[0] = '#'
trench_map_1_converted[-1] = '#'
trench_map_1_converted[:,0] = '#'
trench_map_1_converted[:,-1] = '#'

# STEP 4: pad a second time with 2 rows/cols and '#'
trench_map_2_pad= np.pad(trench_map_1_converted, 2, pad_with2)

print('*******')
for line in trench_map_1_converted:
    print(line)
print('*******')
for line in trench_map_2_pad:
    print(line)

# **************************************
# copy data to new map in which pixel are changed   
trench_map_final = trench_map_2_pad.copy()
#print(f'shape trench_map_new: {trench_map_final.shape}')

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


print('final map')
for line in trench_map_final:
    print(line)

count = (trench_map_final == '#').sum()
print(f'solution: {count}')
      