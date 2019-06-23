import re
import sys
import random


def main():
    test_messages = [
        # testcase format
        # dice?
        # dice count
        # dice side
        # dice result min
        # dice result max
        # has condition ?
        # has option ?

        # d
        ['1d6+1', True, 1, 6, 1, 16, False, False],
        ['1d6+1 < 5', True, 1, 6, 1, 16, True, False],
        ['1d6+1 < 5 [RoR2]', True, 1, 6, 1, 16, True, True],

        # D
        ['1D6+1', True, 1, 6, 1, 16, False, False],
        ['1D6+1 < 5', True, 1, 6, 1, 16, True, False],
        ['1D6+1 < 5 [RoR2]', True, 1, 6, 1, 16, True, True],

        # dice count = 0
        ['0D6+1 < 5', True, 0, 6, 0, 0, True, False],

        # dice side = 0
        ['10D0+1 < 5', True, 10, 0, 0, 0, True, False],

        # minus
        ['1d6-1', True, 1, 6, 1, 6, False, False],
        ['1d6-1 < 5', True, 1, 6, 1, 6, True, False],
        ['1d6-1 < 5 [RoR2]', True, 1, 6, 1, 6, True, True],

        # mul
        ['1d6*1', True, 1, 6, 1, 6, False, False],
        ['1d6*1 < 5', True, 1, 6, 1, 6, True, False],
        ['1d6*1 < 5 [RoR2]', True, 1, 6, 1, 6, True, True],

        # div
        ['1d6/1', True, 1, 6, 1, 6, False, False],
        ['1d6/1 < 5', True, 1, 6, 1, 6, True, False],
        ['1d6/1 < 5 [RoR2]', True, 1, 6, 1, 6, True, True],

        ['1d100 - 10 < 50 [sleep]', True, 1, 100, 1, 100, True, True],
    ]
    for n in test_messages:
        print("")
        print(n[0])
        d = is_dice_roll(n[0])
        if d != n[1]:
            print("Test Failed:IsDiceRoll is wrong")
            continue
        if not d:
            continue

        dice_info = parse_dice(n[0])
        parsed_dice = parse_dice_info(dice_info[0])
        if parsed_dice[0] != n[2]:
            print("Test Failed:DiceCount in ParseDiceInfo is wrong"
                  f"expected {n[2]} but result was {parsed_dice[0]}")
            continue

        if parsed_dice[1] != n[3]:
            print("Test Failed:DiceSide in ParseDiceInfo is wrong"
                  f"expected {n[3]} but result was {parsed_dice[1]}")
            continue
        # if dice_info[0] != n[2]:
        # if dice_info[1] != n[3]:
        #     print("Test Failed:DiceSide in ParseDice is wrong")
        #     continue
        # dice_result = execute_dice_roll(dice_info[0], dice_info[1])
        # if not (dice_result >= n[4] and dice_result <= n[5]):
        #     print(f"Test Failed:ExecuteDice is wrong "
        #           f"expected range is {n[4]} ~ {n[5]}"
        #           f"but result was {dice_result}")
        #     print("")
        #     continue
        # result = execute(n[0], dice_result)
        # if n[6] and type(result) != bool:
        #     print("Test Failed:Execute is wrong")
        #     continue

        # if n[7] != has_option(n[0]):
        #     print("Test Failed:Option is wrong")
        #     continue
        # print(create_result_message(n[0], dice_result, result))


def is_dice_roll(message):
    return re.match(r'\d+d\d', message.lower()) is not None


def has_operation(message):
    return '+' in message or '-' in message or '*' in message or '/' in message


def has_conditional_expression(message):
    return ('<' in message or
            '>' in message or
            '<=' in message or
            '>=' in message)


def has_option(message):
    return '[' in message and ']' in message


def parse_dice(message):
    message = message.replace(" ", "")
    if not is_dice_roll(message):
        return []

    ret = []
    dice_match = re.search(r'\d+d\d+', message, re.IGNORECASE)
    ret += [dice_match.group()]

    message = message[dice_match.end():]

    operator = has_operation(message)
    condition = has_conditional_expression(message)
    option = has_option(message)

    if operator:
        operator_match = re.search(r'[+|\-|*|/]\d+', message)
        ret += [operator_match.group()]
    else:
        ret += [""]

    if condition:
        condition_match = re.search(r'[<|>|<=|>=]\d+', message)
        ret += [condition_match.group()]
    else:
        ret += [""]

    if option:
        opt_match = re.search(r'\[\S+\]', message)
        ret += [opt_match.group().replace('[', '').replace(']', '')]
    else:
        ret += [""]
    return ret


def parse_dice_info(dice_info):
    dice_count_match = re.match(r'\d+', dice_info)
    dice_count = int(dice_count_match.group())

    dice_info = dice_info[dice_count_match.end() + 1:]
    dice_side_match = re.match(r'\d+', dice_info)
    dice_side = int(dice_side_match.group())

    return (dice_count, dice_side)


def execute_dice_roll(parsed_dice_info):
    pass


if __name__ == '__main__':
    main()
