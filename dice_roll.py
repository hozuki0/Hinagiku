import re
import sys
import random


def main():
    test_messages = [
        # testcase , dice? , dice_count , dice_side , dice result min ,dice result max, has condition,has option

        # d
        ['1d6+10', True, 1, 6, 1, 16, False, False],
        ['1d6+10 < 5', True, 1, 6, 1, 16, True, False],
        ['1d6+10 < 5 [RoR2]', True, 1, 6, 1, 16, True, True],

        # D
        ['1D6+10', True, 1, 6, 1, 16, False, False],
        ['1D6+10 < 5', True, 1, 6, 1, 16, True, False],
        ['1D6+10 < 5 [RoR2]', True, 1, 6, 1, 16, True, True],

        # dice count = 0
        ['0D6+10 < 5', True, 0, 6, 0, 0, True, False],

        # dice side = 0
        ['10D0+10 < 5', True, 10, 0, 0, 0, True, False],

        # minus
        ['1d6-10', True, 1, 6, 1, 6, False, False],
        ['1d6-10 < 5', True, 1, 6, 1, 6, True, False],
        ['1d6-10 < 5 [RoR2]', True, 1, 6, 1, 6, True, True],

    ]
    for n in test_messages:
        print(n[0])
        d = is_dice_roll(n[0])
        if d != n[1]:
            print("Test Failed:IsDiceRoll is wrong")
            continue
        if not d:
            continue

        dice_info = parse_dice(n[0])
        if dice_info[0] != n[2]:
            print("Test Failed:DiceCount in ParseDice is wrong")
            continue
        if dice_info[1] != n[3]:
            print("Test Failed:DiceSide in ParseDice is wrong")
            continue
        dice_result = execute_dice_roll(dice_info[0], dice_info[1])
        if not (dice_result >= n[4] and dice_result <= n[5]):
            print(f"Test Failed:ExecuteDice is wrong "
                  "expected range is {n[4]} ~ {n[5]} but result was {dice_result}")
            print("")
            continue
        result = execute(n[0], dice_result)
        if n[6] and type(result) != bool:
            print("Test Failed:Execute is wrong")
            continue

        if n[7] != has_option(n[0]):
            print("Test Failed:Option is wrong")
            continue
        print(create_result_message(n[0], dice_result, result))
        print("")


def is_dice_roll(message):
    return re.match('\d+d\d', message.lower()) != None


def has_operation(message):
    return '+' in message or '-' in message or '*' in message or '/' in message


def parse_dice(message):
    lower_message = message.lower()
    first_d_pos = lower_message.find('d')
    temp_str_array = []
    for n in range(first_d_pos):
        temp_str_array += [lower_message[n]]
    dice_count = int(''.join(temp_str_array))
    lower_message = lower_message[first_d_pos +
                                  1:len(lower_message)]

    non_num_pos = find_non_num_pos(lower_message)
    temp_str_array = []
    for n in range(non_num_pos):
        temp_str_array += [lower_message[n]]
    dice_side = int(''.join(temp_str_array))

    return (dice_count, dice_side)


def find_non_num_pos(message):
    pos = 0
    for n in message:
        if n != ' ' and not n.isnumeric():
            return pos
        pos += 1
    return pos


def has_conditional_expression(message):
    return ('<' in message or
            '>' in message or
            '<=' in message or
            '>=' in message)


def execute_dice_roll(count, side_count):
    sum = 0
    if side_count == 0 or count == 0:
        return sum
    for n in range(count):
        sum += random.randint(1, side_count)
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


def find_operation(message):
    conditions = ['+', '-', '*', '/']
    for condition in conditions:
        p = message.find(condition)
        if p != -1:
            return p
    return None


def execute(message, dice_result):
    m = re.match('\d+d\d+', message.lower())
    message = message[m.end():]
    below = extract_below_comp_operator(message)
    return eval(str(dice_result) + below + extract_comp_expression(message))


def extract_comp_expression(message):
    if not has_conditional_expression(message):
        return ''
    first_cond_pos = find_condition(message)
    if has_option(message):
        return message[first_cond_pos:message.find('[')]
    return message[first_cond_pos:]


def extract_above_comp_operator(message):
    if has_operation(message):
        return message[:find_operation(message)]
    return ''


def extract_below_comp_operator(message):
    if has_operation(message):
        ope = find_operation(message)
        cond = find_condition(message)
        if cond:
            return message[ope:len(message)]
        else:
            return message[ope:cond]
    return ''


def create_result_message(message, dice_result, evaluate_result):
    if has_conditional_expression(message):
        ev = 'Error'
        if evaluate_result:
            ev = 'Success!'
        else:
            ev = 'Failed...'
        opt = extract_option(message)
        if opt != '':
            opt += ' '

        return opt + str(dice_result) + ' ' + \
            extract_conditions(message) + ' -> ' + ev
    return str(dice_result)


def extract_option(message):
    if not has_option(message):
        return ''
    return message[message.find('['): len(message)]


if __name__ == '__main__':
    main()
