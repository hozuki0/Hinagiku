import re
import sys


def main():
    test_message = [
        '1d6+10',
        '1d6+10 < 5',
        '1d6+10 < 5 [RoR2]',

        '1D6+10',
        '1D6+10 < 5',
        '1D6+10 < 5 [RoR2]'
    ]
    for n in test_message:
        print(f"DiceRoll:{is_dice_roll(n)}")
        dice_info = parse_dice(n)
        print(f"DiceCount:{dice_info[0]} & DiceSideCount:{dice_info[1]}")
        print(f"HasCondition:{has_conditional_expression(n)}")
        print("")


def is_dice_roll(message):
    return ('d' in message or 'D' in message) and '+' in message


def parse_dice(message):
    lower_message = message.lower()
    first_d_pos = lower_message.find('d')
    temp_str_array = []
    for n in range(first_d_pos):
        temp_str_array += [lower_message[n]]
    dice_count = int(''.join(temp_str_array))
    lower_message = lower_message[first_d_pos +
                                  1:len(lower_message) - first_d_pos - 1]
    first_plus_pos = lower_message.find('+')

    temp_str_array = []
    for n in range(first_plus_pos):
        temp_str_array += [lower_message[n]]
    dice_side = int(''.join(temp_str_array))
    return (dice_count, dice_side)


def has_conditional_expression(message):
    return ('<' in message or '>' in message or '<=' in message or '>=' in message)


if __name__ == '__main__':
    main()
