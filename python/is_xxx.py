import re
import random


def main():
    test_case = [
        ['IsRoR2()', True, 'RoR2'],
    ]
    for test in test_case:
        print(f'Test Case is {test[0]}')
        if is_isXXX_format(test[0]) != test[1]:
            print('Failed to Check isXXX format')
            continue
        if not is_isXXX_format(test[0]):
            continue

        fn_name = parse_function_name(test[0])
        if fn_name != test[2]:
            print(f'Failed to Parse FnName .'
                  f'expected {test[2]} but result was {fn_name}')
            continue
        print("collect!")
        print("")


def is_isXXX_format(message):
    return 'is' in message.lower() \
        and '(' in message.lower() \
        and ')' in message.lower()


def parse_function_name(message):
    lm = message.lower()
    prefix = re.match('is', lm)
    return message[prefix.end():lm.find('(')]


def create_reply(message):
    result = "return true;" if random.randint(0, 1) == 1 else "return false;"
    return result


if __name__ == '__main__':
    main()
