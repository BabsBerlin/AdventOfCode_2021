#######################
# Advent of Code 2021 #
#   day 21 - part1    #
#######################


player = {'p_one': {'pos': 8, 'points': 0}, 'p_two': {'pos': 2, 'points': 0}}
dice = {'last_side': 0, 'turns': 0}
losing_player = ''


def dice_roll(current_player):
    global dice
    # player rolls three times
    three_turns = ((dice['last_side'] + 1) % 100) + ((dice['last_side'] + 2) % 100) + ((dice['last_side'] + 3) % 100)
    dice['last_side'] += 3
    dice['turns'] += 3
    player[current_player]['pos'] += three_turns % 10
    if player[current_player]['pos'] > 10:
        player[current_player]['pos'] = (player[current_player]['pos'] % 10)
    player[current_player]['points'] += player[current_player]['pos']


def check_score(current_player):
    if player[current_player]['points'] >= 1000:
        return True
    else:
        return False


print(f'player one: points: {player["p_one"]["points"]} position: {player["p_one"]["pos"]}')
print(f'player two: points: {player["p_two"]["points"]} position: {player["p_two"]["pos"]}')


# play the game - the 200 was just a wild guess :-)
for x in range(200):
    dice_roll('p_one')
    if check_score('p_one'):
        losing_player = 'p_two'
        break
    dice_roll('p_two')
    if check_score('p_two'):
        losing_player = 'p_one'
        break


print(f'player one: points: {player["p_one"]["points"]} position: {player["p_one"]["pos"]}')
print(f'player two: points: {player["p_two"]["points"]} position: {player["p_two"]["pos"]}')

solution = player[losing_player]['points'] * dice['turns']
print(f'solution: {solution}')
