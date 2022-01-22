#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import join
from os import getcwd
from collections import Counter, namedtuple
import math
import random
import time
import json
import re

binops = []


def stem(input):
    input = re.sub("\s+", ' ', input)
    input = input.rstrip()
    input = input.lstrip()
    return input


def find_datapoints(data_path, mode):

    with open(data_path) as file:
        all_binops = json.load(file)

    for binop in all_binops:

        single_binop = {
            'left': binop['leftOperand'],
            'right': binop['rightOperand'],
            'leftPrefix': binop['original']['left'].strip().split(':'
                    )[0],
            'rightPrefix': binop['original']['right'].strip().split(':'
                    )[0],
            'leftType': binop['original']['leftType'],
            'rightType': binop['original']['rightType'],
            'op': binop['original']['op'],
            }
        binops.append(single_binop)

    if mode == 'train':
        file_train = open('file_train.txt', 'w')
        file_buggy_train = open('file_buggy_train.txt', 'w')
        file_dev = open('file_dev.txt', 'w')
        file_buggy_dev = open('file_buggy_dev.txt', 'w')
        split_size = math.floor(len(binops) * 0.9)
        counter = 0
        all_ops = [
            '*',
            '%',
            '/',
            '+',
            '-',
            '>>',
            '<<',
            '>>>',
            '>',
            '<',
            '>=',
            '<=',
            'in',
            'instanceof',
            '==',
            '!=',
            '===',
            '!==',
            '&',
            '^',
            '|',
            '&&',
            '||',
            ]
        for binop in binops:
            correct = binop['leftPrefix'] + ' ' + binop['leftType'] \
                + ' ' + binop['left'] + ' ' + binop['op'] + ' ' \
                + binop['rightPrefix'] + ' ' + binop['rightType'] + ' ' \
                + binop['right']
            correct = correct.encode('utf-8', 'replace').decode()
            wrong_op = ''
            while True:
                wrong_op = random.choice(all_ops)
                if wrong_op == binop['op']:
                    continue
                else:
                    break

            buggy = binop['leftPrefix'] + ' ' + binop['leftType'] + ' ' \
                + binop['left'] + ' ' + wrong_op + ' ' \
                + binop['rightPrefix'] + ' ' + binop['rightType'] + ' ' \
                + binop['right']
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
        all_ops = [
            '*',
            '%',
            '/',
            '+',
            '-',
            '>>',
            '<<',
            '>>>',
            '>',
            '<',
            '>=',
            '<=',
            'in',
            'instanceof',
            '==',
            '!=',
            '===',
            '!==',
            '&',
            '^',
            '|',
            '&&',
            '||',
            ]
        for binop in binops:
            correct = binop['leftPrefix'] + ' ' + binop['leftType'] \
                + ' ' + binop['left'] + ' ' + binop['op'] + ' ' \
                + binop['rightPrefix'] + ' ' + binop['rightType'] + ' ' \
                + binop['right']
            wrong_op = ''
            while True:
                wrong_op = random.choice(all_ops)
                if wrong_op == binop['op']:
                    continue
                else:
                    break
            buggy = binop['leftPrefix'] + ' ' + binop['leftType'] + ' ' \
                + binop['left'] + ' ' + wrong_op + ' ' \
                + binop['rightPrefix'] + ' ' + binop['rightType'] + ' ' \
                + binop['right']

            buggy = stem(buggy)
            correct = stem(correct)

            file_test.write('%s\n' % correct)
            file_buggy_test.write('%s\n' % buggy)

        file_test.close()
        file_buggy_test.close()
    elif mode == 'real':

        file_real = open('file_real.txt', 'w')
        file_buggy_real = open('file_buggy_real.txt', 'w')
        all_ops = [
            '*',
            '%',
            '/',
            '+',
            '-',
            '>>',
            '<<',
            '>>>',
            '>',
            '<',
            '>=',
            '<=',
            'in',
            'instanceof',
            '==',
            '!=',
            '===',
            '!==',
            '&',
            '^',
            '|',
            '&&',
            '||',
            ]
        for binop in binops:
            correct = binop['leftPrefix'] + ' ' + binop['leftType'] \
                + ' ' + binop['left'] + ' ' + binop['op'] + ' ' \
                + binop['rightPrefix'] + ' ' + binop['rightType'] + ' ' \
                + binop['right']
            wrong_op = ''
            while True:
                wrong_op = random.choice(all_ops)
                if wrong_op == binop['op']:
                    continue
                else:
                    break
            buggy = binop['leftPrefix'] + ' ' + binop['leftType'] + ' ' \
                + binop['left'] + ' ' + wrong_op + ' ' \
                + binop['rightPrefix'] + ' ' + binop['rightType'] + ' ' \
                + binop['right']

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
