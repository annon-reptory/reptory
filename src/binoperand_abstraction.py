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
import csv

top_tokens = []
keywords = []


def stem(input):
    input = re.sub("\s+", ' ', input)
    input = input.rstrip()
    input = input.lstrip()
    return input


def find_freq(data_path, count):
    count = int(count)
    frequent = {}
    with open(data_path) as file:
        all_binops = json.load(file)

    for binop in all_binops:

        single_binop = {'left': binop['leftOperand'].strip(),
                        'right': binop['rightOperand'].strip()}

        if single_binop['left'] in frequent:
            frequent[single_binop['left']] = \
                frequent[single_binop['left']] + 1
        else:
            frequent[single_binop['left']] = 1
        if single_binop['right'] in frequent:
            frequent[single_binop['right']] = \
                frequent[single_binop['right']] + 1
        else:
            frequent[single_binop['right']] = 1

    counter = 0
    for w in sorted(frequent, key=frequent.get, reverse=True):
        if counter < count:
            top_tokens.append(w)
            counter += 1
        else:
            break


def load_keywords(data_path):
    with open(data_path, newline='') as csvfile:
        keywordsReader = csv.reader(csvfile, delimiter=',',
                                    quotechar='|')
        for keyword in keywordsReader:
            keywords.append(keyword[0])


def find_datapoints(data_path, mode):
    with open(data_path) as file:
        all_binops = json.load(file)

    binops = []
    for binop in all_binops:
        single_binop = {
            'left': binop['leftOperand'].strip(),
            'right': binop['rightOperand'].strip(),
            'op': binop['original']['op'].strip(),
            'leftType': binop['original']['leftType'].strip(),
            'rightType': binop['original']['rightType'].strip(),
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

            methods = []
            variables = []
            numbers = []
            strings = []

            left = ''
            if binop['left'] in top_tokens or binop['left'] in keywords:
                left = binop['left']
            elif binop['leftType'] == 'function':
                if binop['left'] in methods:
                    left = 'Method_' + str(methods.index(binop['left'])
                            + 1)
                else:
                    methods.append(binop['left'])
                    left = 'Method_' + str(methods.index(binop['left'])
                            + 1)
            elif binop['leftType'] == 'string':
                if binop['left'] in strings:
                    left = 'String_' + str(strings.index(binop['left'])
                            + 1)
                else:
                    strings.append(binop['left'])
                    left = 'String_' + str(strings.index(binop['left'])
                            + 1)
            elif binop['leftType'] == 'number':
                if binop['left'] in numbers:
                    left = 'Number_' + str(numbers.index(binop['left'])
                            + 1)
                else:
                    numbers.append(binop['left'])
                    left = 'Number_' + str(numbers.index(binop['left'])
                            + 1)
            else:
                if binop['left'] in variables:
                    left = 'Var_' + str(variables.index(binop['left'])
                            + 1)
                else:
                    variables.append(binop['left'])
                    left = 'Var_' + str(variables.index(binop['left'])
                            + 1)

            right = ''
            if binop['right'] in top_tokens or binop['right'] \
                in keywords:
                right = binop['right']
            elif binop['rightType'] == 'function':
                if binop['right'] in methods:
                    right = 'Method_' + str(methods.index(binop['right'
                            ]) + 1)
                else:
                    methods.append(binop['right'])
                    right = 'Method_' + str(methods.index(binop['right'
                            ]) + 1)
            elif binop['rightType'] == 'string':
                if binop['right'] in strings:
                    right = 'String_' + str(strings.index(binop['right'
                            ]) + 1)
                else:
                    strings.append(binop['right'])
                    right = 'String_' + str(strings.index(binop['right'
                            ]) + 1)
            elif binop['rightType'] == 'number':
                if binop['right'] in numbers:
                    right = 'Number_' + str(numbers.index(binop['right'
                            ]) + 1)
                else:
                    numbers.append(binop['right'])
                    right = 'Number_' + str(numbers.index(binop['right'
                            ]) + 1)
            else:
                if binop['right'] in variables:
                    right = 'Var_' + str(variables.index(binop['right'
                            ]) + 1)
                else:
                    variables.append(binop['right'])
                    right = 'Var_' + str(variables.index(binop['right'
                            ]) + 1)

            correct = left + ' ' + binop['op'] + ' ' + right
            correct = correct.encode('utf-8', 'replace').decode()
            buggy = right + ' ' + binop['op'] + ' ' + left
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

            methods = []
            variables = []
            numbers = []
            strings = []

            left = ''
            if binop['left'] in top_tokens or binop['left'] in keywords:
                left = binop['left']
            elif binop['leftType'] == 'function':
                if binop['left'] in methods:
                    left = 'Method_' + str(methods.index(binop['left'])
                            + 1)
                else:
                    methods.append(binop['left'])
                    left = 'Method_' + str(methods.index(binop['left'])
                            + 1)
            elif binop['leftType'] == 'string':
                if binop['left'] in strings:
                    left = 'String_' + str(strings.index(binop['left'])
                            + 1)
                else:
                    strings.append(binop['left'])
                    left = 'String_' + str(strings.index(binop['left'])
                            + 1)
            elif binop['leftType'] == 'number':
                if binop['left'] in numbers:
                    left = 'Number_' + str(numbers.index(binop['left'])
                            + 1)
                else:
                    numbers.append(binop['left'])
                    left = 'Number_' + str(numbers.index(binop['left'])
                            + 1)
            else:
                if binop['left'] in variables:
                    left = 'Var_' + str(variables.index(binop['left'])
                            + 1)
                else:
                    variables.append(binop['left'])
                    left = 'Var_' + str(variables.index(binop['left'])
                            + 1)

            right = ''
            if binop['right'] in top_tokens or binop['right'] \
                in keywords:
                right = binop['right']
            elif binop['rightType'] == 'function':
                if binop['right'] in methods:
                    right = 'Method_' + str(methods.index(binop['right'
                            ]) + 1)
                else:
                    methods.append(binop['right'])
                    right = 'Method_' + str(methods.index(binop['right'
                            ]) + 1)
            elif binop['rightType'] == 'string':
                if binop['right'] in strings:
                    right = 'String_' + str(strings.index(binop['right'
                            ]) + 1)
                else:
                    strings.append(binop['right'])
                    right = 'String_' + str(strings.index(binop['right'
                            ]) + 1)
            elif binop['rightType'] == 'number':
                if binop['right'] in numbers:
                    right = 'Number_' + str(numbers.index(binop['right'
                            ]) + 1)
                else:
                    numbers.append(binop['right'])
                    right = 'Number_' + str(numbers.index(binop['right'
                            ]) + 1)
            else:
                if binop['right'] in variables:
                    right = 'Var_' + str(variables.index(binop['right'
                            ]) + 1)
                else:
                    variables.append(binop['right'])
                    right = 'Var_' + str(variables.index(binop['right'
                            ]) + 1)

            correct = left + ' ' + binop['op'] + ' ' + right
            correct = correct.encode('utf-8', 'replace').decode()
            buggy = right + ' ' + binop['op'] + ' ' + left
            buggy = buggy.encode('utf-8', 'replace').decode()

            buggy = stem(buggy)
            correct = stem(correct)

            file_test.write('%s\n' % correct)
            file_buggy_test.write('%s\n' % buggy)
        file_test.close()
        file_buggy_test.close()
    elif mode == 'real':

        methods = []
        variables = []
        numbers = []
        strings = []

        file_real = open('file_real.txt', 'w')
        file_buggy_real = open('file_buggy_real.txt', 'w')
        for binop in binops:

            left = ''
            if binop['left'] in top_tokens or binop['left'] in keywords:
                left = binop['left']
            elif binop['leftType'] == 'function':
                if binop['left'] in methods:
                    left = 'Method_' + str(methods.index(binop['left'])
                            + 1)
                else:
                    methods.append(binop['left'])
                    left = 'Method_' + str(methods.index(binop['left'])
                            + 1)
            elif binop['leftType'] == 'string':
                if binop['left'] in strings:
                    left = 'String_' + str(strings.index(binop['left'])
                            + 1)
                else:
                    strings.append(binop['left'])
                    left = 'String_' + str(strings.index(binop['left'])
                            + 1)
            elif binop['leftType'] == 'number':
                if binop['left'] in numbers:
                    left = 'Number_' + str(numbers.index(binop['left'])
                            + 1)
                else:
                    numbers.append(binop['left'])
                    left = 'Number_' + str(numbers.index(binop['left'])
                            + 1)
            else:
                if binop['left'] in variables:
                    left = 'Var_' + str(variables.index(binop['left'])
                            + 1)
                else:
                    variables.append(binop['left'])
                    left = 'Var_' + str(variables.index(binop['left'])
                            + 1)

            right = ''
            if binop['right'] in top_tokens or binop['right'] \
                in keywords:
                right = binop['right']
            elif binop['rightType'] == 'function':
                if binop['right'] in methods:
                    right = 'Method_' + str(methods.index(binop['right'
                            ]) + 1)
                else:
                    methods.append(binop['right'])
                    right = 'Method_' + str(methods.index(binop['right'
                            ]) + 1)
            elif binop['rightType'] == 'string':
                if binop['right'] in strings:
                    right = 'String_' + str(strings.index(binop['right'
                            ]) + 1)
                else:
                    strings.append(binop['right'])
                    right = 'String_' + str(strings.index(binop['right'
                            ]) + 1)
            elif binop['rightType'] == 'number':
                if binop['right'] in numbers:
                    right = 'Number_' + str(numbers.index(binop['right'
                            ]) + 1)
                else:
                    numbers.append(binop['right'])
                    right = 'Number_' + str(numbers.index(binop['right'
                            ]) + 1)
            else:
                if binop['right'] in variables:
                    right = 'Var_' + str(variables.index(binop['right'
                            ]) + 1)
                else:
                    variables.append(binop['right'])
                    right = 'Var_' + str(variables.index(binop['right'
                            ]) + 1)

            correct = left + ' ' + binop['op'] + ' ' + right
            correct = correct.encode('utf-8', 'replace').decode()
            buggy = right + ' ' + binop['op'] + ' ' + left
            buggy = buggy.encode('utf-8', 'replace').decode()

            buggy = stem(buggy)
            correct = stem(correct)

            file_real.write('%s\n' % correct)
            file_buggy_real.write('%s\n' % buggy)
        file_real.close()
        file_buggy_real.close()


if __name__ == '__main__':

    time_start = time.time()
    load_keywords(sys.argv[4])
    find_freq(sys.argv[1], sys.argv[5])
    find_datapoints(sys.argv[1], 'train')
    find_datapoints(sys.argv[2], 'test')
    find_datapoints(sys.argv[3], 'real')
