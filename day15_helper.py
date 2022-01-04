#######################
# Advent of Code 2021 #
# day 15 - helper p2  #
#######################

""" 
copies the input 5x to the right and 5x below,
increasing the value by the pattern below:
8 9 1 2 3
9 1 2 3 4
1 2 3 4 5
2 3 4 5 6
3 4 5 6 7 
"""

raw_file = 'day15.txt'

with open(raw_file) as file:
    data = [row.strip() for row in file.readlines()]
 
new_data = data.copy()
temp_data = data.copy()

## to extend to the right!
for x in range(1,5):
    #print(f'updating {x}')    
    for rowindex,i in enumerate(temp_data):
        #print(f'line data: {data[rowindex]} and line new: {new2[rowindex]}')
        newline = new_data[rowindex]
        for c in i:
            if int(c) == 9:
                newline = newline + str(1)
            else:
                newline = newline + str(int(c) + 1)
        #print(f'newline: {newline}')
        
        temp_data[rowindex] = newline[-len(data):] #len(data)           
        new_data[rowindex] = newline
    
# to extend below
big_data = new_data.copy()
temp_data = new_data.copy()

for x in range(1,5):
    #print(f'updating {x}')    
    for rowindex, i in enumerate(temp_data):
        new_row = ''
        for c in i:
            if int(c) == 9:
                new_row = new_row + str(1)
            else:
                new_row = new_row + str(int(c) + 1)
        big_data.append(new_row)
        temp_data[rowindex] = new_row

for n in big_data:
    print(n)
    
with open('day15_big_data.txt', 'w') as f:
    for n in big_data:
        f.write(n)
        f.write('\n')
    
    #f.write(big_data)

print(f'initial length: {len(data[0])} x {len(data)}')
print(f'new length: {len(big_data[0])} x {len(big_data)}')
