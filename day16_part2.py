#######################
# Advent of Code 2021 #
#   day 16 - part 2   #
#######################

raw_file = 'day16.txt'
#raw_file = 'day16_test.txt'

with open(raw_file) as file:
    input = file.readlines()

data = data = [row.strip() for row in input]
data = [x for x in data]


# convert input including leading zeros
h_size = len(data[0]) * 4
bin_input = (bin(int(data[0], 16))[2:]).zfill(h_size)
print(f'input as hex: {data}')
print(f'input converted to binary: {bin_input}')


# function to convert hex value to binary, most significant bit first (no leading zeros)
def hex_to_binary(hex_value):
    int_value = int(hex_value, base=16)
    bin_value = bin(int_value)
    return bin_value[2:]  # cut of the 0b
# *****************************************************


# convert binary to integer - has to be inputted as string because of the leading zeros!
def binary_to_decimal(binary_value):
    binary_value = '0b' + binary_value
    return int(binary_value, 2)
# *****************************************************


# the package contains literals in pairs of 5
def literal_packet(transmission):
    number = ''
    while True:
        first = transmission[0]
        number = number + transmission[1:5]
        transmission = transmission[5:]
        # 0 indicates the last literal
        if first == '0':
            break
    number = binary_to_decimal(number)
    return number, transmission
# *****************************************************


def read_packet(transmission):
    global packets
    subpacket_list = []
    result = 0
    print('*******')
    # *** get packet version
    packet_version = transmission[:3]
    packet_version = binary_to_decimal(packet_version)
    print(f'packet_version: {packet_version}')
    # *** add to sum
    packets += packet_version

    # *** get packet ID
    packet_id = transmission[3:6]
    packet_id = binary_to_decimal(packet_id)
    print(f'packet_id: {packet_id}')

    # *** cut first six bits off
    transmission = transmission[6:]

    # ID: 4 -> package represents a literal value
    if packet_id == 4:
        print('literal package')
        result, transmission = literal_packet(transmission)
    elif packet_id != 4:
        if transmission[:1] == '0':
            # 15-bit:
            fifteen = transmission[1:16]
            subpackets_length = binary_to_decimal(fifteen)
            print(f'operator 15-bits with length of subpackets: {subpackets_length}')

            subpacket = transmission[16:16+subpackets_length]
            while subpacket:
                sub_list, subpacket = read_packet(subpacket)
                subpacket_list.append(sub_list)
            transmission = transmission[16+subpackets_length:]
        elif transmission[:1] == '1':
            eleven = transmission[1:12]
            subpackets_count = binary_to_decimal(eleven)
            print(f'operator 11-bits with {subpackets_count} subpackets')
            transmission = transmission[12:]
            while subpackets_count >= 1:
                sub_list, transmission = read_packet(transmission)
                subpacket_list.append(sub_list)
                subpackets_count -= 1
        if packet_id == 0:
            result = sum(subpacket_list)
        elif packet_id == 1:
            result = 1
            for x in subpacket_list:
                result *= x
        elif packet_id == 2:
            result = min(subpacket_list)
        elif packet_id == 3:
            result = max(subpacket_list)
        elif packet_id == 5:
            if subpacket_list[0] > subpacket_list[1]:
                result = 1
        elif packet_id == 6:
            if subpacket_list[0] < subpacket_list[1]:
                result = 1
        elif packet_id == 7:
            if subpacket_list[0] == subpacket_list[1]:
                result = 1

    return result, transmission

packets = 0
solution, rest = read_packet(bin_input)

print('*******')
print(f'part1 - sum of package versions: {packets}')
print('*******')
print(f'part2 - THE SOLUTION: {solution}')
print('*******')
