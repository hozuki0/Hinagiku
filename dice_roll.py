import re
import sys
import random


def main():
    test_message = [
        '1d6+10',
        '1d6+10 < 5',
        '1d6+10 < 5 [RoR2]',

        '10d6+10',
        '100d6+10 < 5',
        '1000d6+10 < 5 [RoR2]',

        '1D6+10',
        '1D6+10 < 5',
        '1D6+10 < 5 [RoR2]',

        'Yukitterの真似して',
        'sita',
        '上下UD',
        '酒!',
    ]
    for n in test_message:
        print(n)
        d = is_dice_roll(n)
        print(f"DiceRoll:{d}")
        if not d:
            print("")
            continue
        dice_info = parse_dice(n)
        print(f"DiceCount:{dice_info[0]} & DiceSideCount:{dice_info[1]}")
        dice_result = execute_dice_roll(dice_info[0], dice_info[1])
        print(dice_result)
        print(f"HasCondition:{has_conditional_expression(n)}")
        print(extract_conditions(n))
        print(f"HasOption:{has_option(n)}")
        result = execute(n, dice_result)
        print(create_result_message(n, dice_result, result))
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
                                  1:len(lower_message)]
    first_plus_pos = lower_message.find('+')

    temp_str_array = []
    for n in range(first_plus_pos):
        temp_str_array += [lower_message[n]]
    dice_side = int(''.join(temp_str_array))
    return (dice_count, dice_side)


def has_conditional_expression(message):
    return ('<' in message or '>' in message or '<=' in message or '>=' in message)


def execute_dice_roll(count, side_count):
    sum = 0
    for n in range(count):
        sum += random.randint(0, side_count)
    return sum


def extract_conditions(message):
    # messageから < , > , <= , >= と数字を抽出する
    condition_pos = find_condition(message)
    if not condition_pos:
        return ''

    if has_option(message):
        return message[condition_pos:message.find('[') - 1]
    else:
        return message[condition_pos:len(message)]


def has_option(message):
    return '[' in message and ']' in message


def find_condition(message):
    conditions = ['<', '>', '<=', '>=']
    for condition in conditions:
        p = message.find(condition)
        if p != -1:
            return p
    return None


def execute(message, dice_result):
    return eval(str(dice_result) + extract_other_than_dice_exp(message))


def extract_other_than_dice_exp(message):
    first_plus_pos = message.find('+')
    if has_option(message):
        return message[first_plus_pos:message.find('[')]
    else:
        return message[first_plus_pos:len(message)]


def create_result_message(message, dice_result, evaluate_result):
    ev = 'Success!' if evaluate_result else 'Failed...'
    opt = extract_option(message)
    if opt != '':
        opt += ' '
    return (opt + str(dice_result + eval(extract_other_than_dice_exp(message))) + ' ' + extract_conditions(message) + ' -> ' + ev)


def extract_option(message):
    if not has_option(message):
        return ''
    return message[message.find('['): len(message)]


if __name__ == '__main__':
    main()
