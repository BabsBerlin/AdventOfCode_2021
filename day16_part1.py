#######################
# Advent of Code 2021 #
#   day 16 - part 1   #
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
print(f'input converted to binary: {bin_input}')

print(f'input as hex: {data}')
print(f'input converted to binary: {bin_input}')
print('*******')
# *****************************************************


# function to convert hex value to binary,
# most significant bit first (no leading zeros)
def hex_to_binary(hex_value):
    int_value = int(hex_value, base=16)
    bin_value = bin(int_value)
    return bin_value[2:]  # cut of the 0b
# *****************************************************


# convert binary to integer - has to be string input because of the leading zeros!
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


def read_packet(packets, transmission):
    print('*******')
    if len(transmission) < 7:
        return packets, transmission
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
        _, transmission = literal_packet(transmission)

    # elif ID != 4
    else:
        print('calling operator package')
        if transmission[:1] == '0':
            # 15-bit:
            fifteen = transmission[1:16]
            subpackets_length = binary_to_decimal(fifteen)
            print(f'length of 15-subpackets: {subpackets_length}')

            subpacket = transmission[16:16+subpackets_length]
            transmission = transmission[16+subpackets_length:]
            packets, rest = read_packet(packets, subpacket)
        elif transmission[:1] == '1':
            eleven = transmission[1:12]
            subpackets_count = binary_to_decimal(eleven)
            print(f'number of 11-subpackets: {subpackets_count}')
            transmission = transmission[12:]
            packets, transmission = read_packet(packets, transmission)
    if len(transmission) > 7:
        packets, transmission = read_packet(packets, transmission)
    return packets, transmission


packets = 0
packets, rest = read_packet(packets, bin_input)

print('*******')
print(f'sum of package versions: {packets}')
print('*******')
