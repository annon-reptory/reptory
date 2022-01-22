#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import math
import re
import sys
import time

binops = []


def camel_case_split(identifier):
    matches = \
        re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)'
                    , identifier)
    sub_words = [m.group(0) for m in matches]
    return ' <CAMEL> '.join([sub_word for sub_word in sub_words])


def snake_case_split(identifier):
    words = identifier.split('_')
    return ' '.join([sub_word for sub_word in words])


def stem(input_string):
    result = camel_case_split(input_string)
    result = snake_case_split(result)
    result = ' '.join([sub_word for sub_word in re.split('(\d+)', result)])
    result = re.sub("\s+", ' ', result)
    result = camel_case_split(result)
    result = result.rstrip()
    result = result.lstrip()
    return result

def get_value(input_arg, input_type):
    numbers = [0, 1]
    numbers_str = ["0", "1"]
    strings = ["0", "1"]
    result = input_arg

    # print("get_value({}, {}), types=({},{})".format(input_arg, input_type,
    #                                                 type(input_arg), type(input_type)))

    # if input['type1'] == 'string':
    #     if input['arg1'] in strings:
    #         arg1 = str(input['arg1'])
    #     else:
    #         arg1 = 'String'
    # elif input['type1'] == 'number':
    #     if input['arg1'] in numbers:
    #         arg1 = str(input['arg1'])
    #     else:
    #         arg1 = 'Number'

    # print('started matching:')
    # print('searching for:{}', input_type)
    if input_type == 'string':
        #print('match string')
        if input_arg in strings:
            result = str(input_arg)
        else:
            result = 'String'
    elif input_type == 'number':
        #print('match number')
        if input_arg in numbers or input_arg in numbers_str:
            result = str(input_arg)
        else:
            result = 'Number'
    # print('end matching:')

    return result


def find_datapoints(data_path, mode):
    with open(data_path) as file:
        all_binops = json.load(file)

    for binop in all_binops:
        single_binop = {'left': binop['leftOperand'],
                        'right': binop['rightOperand'],
                        'op': binop['original']['op'],
                        'leftType': binop['original']['leftType'].strip(),
                        'rightType': binop['original']['rightType'].strip()
                        }
        binops.append(single_binop)

    if mode == 'train':
        file_train = open('file_train.txt', 'w')
        file_buggy_train = open('file_buggy_train.txt', 'w')
        file_dev = open('file_dev.txt', 'w')
        file_buggy_dev = open('file_buggy_dev.txt', 'w')
        split_size = math.floor(len(binops) * 0.9)
        counter = 0

        for binop in binops:
            correct = get_value(binop['left'], binop['leftType']) + ' ' + binop['op'] + ' ' + get_value(binop['right'], binop['rightType'])
            correct = correct.encode('utf-8', 'replace').decode()

            buggy = get_value(binop['right'], binop['rightType']) + ' ' + binop['op'] + ' ' + get_value(binop['left'], binop['leftType'])
            buggy = buggy.encode('utf-8', 'replace').decode()

            buggy = stem(buggy)
            correct = stem(correct)

            if counter < split_size:
                file_train.write('%s\n' % correct)
                file_buggy_train.write('%s\n' % buggy)
            else:
                file_dev.write('%s\n' % correct)
                file_buggy_dev.write('%s\n' % buggy)
            counter += 1

        file_train.close()
        file_buggy_train.close()
        file_dev.close()
        file_buggy_dev.close()
    elif mode == 'test':
        file_test = open('file_test.txt', 'w')
        file_buggy_test = open('file_buggy_test.txt', 'w')
        for binop in binops:
            correct = get_value(binop['left'], binop['leftType']) + ' ' + binop['op'] + ' ' + get_value(binop['right'], binop['rightType'])
            buggy = get_value(binop['right'], binop['rightType']) + ' ' + binop['op'] + ' ' + get_value(binop['left'], binop['leftType'])

            buggy = stem(buggy)
            correct = stem(correct)

            file_test.write('%s\n' % correct)
            file_buggy_test.write('%s\n' % buggy)
        file_test.close()
        file_buggy_test.close()
    elif mode == 'real':
        file_real = open('file_real.txt', 'w')
        file_buggy_real = open('file_buggy_real.txt', 'w')
        for binop in binops:
            print(binop)
            correct = get_value(binop['left'], binop['leftType']) + ' ' + binop['op'] + ' ' + get_value(binop['right'], binop['rightType'])
            buggy = get_value(binop['right'], binop['rightType']) + ' ' + binop['op'] + ' ' + get_value(binop['left'], binop['leftType'])

            buggy = stem(buggy)
            correct = stem(correct)

            file_real.write('%s\n' % correct)
            file_buggy_real.write('%s\n' % buggy)
        file_real.close()
        file_buggy_real.close()


if __name__ == '__main__':
    time_start = time.time()
    mode = sys.argv[2]

    find_datapoints(sys.argv[1], mode)
