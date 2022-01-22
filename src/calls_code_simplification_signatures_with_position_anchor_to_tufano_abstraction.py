#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
import math
import re
import sys
import time

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
        all_calls = json.load(file)

    for call in all_calls:
        single_call = {
            'base': call['base'].strip(),
            'callee': call['callee'].strip(),
            'arg1': call['arg1'].strip(),
            'arg2': call['arg2'].strip()
        }

        if single_call['base'] in frequent:
            frequent[single_call['base']] = frequent[single_call['base']] + 1
        else:
            frequent[single_call['base']] = 1

        if single_call['callee'] in frequent:
            frequent[single_call['callee']] = frequent[single_call['callee']] + 1
        else:
            frequent[single_call['callee']] = 1
        if single_call['arg1'] in frequent:
            frequent[single_call['arg1']] = frequent[single_call['arg1']] + 1
        else:
            frequent[single_call['arg1']] = 1
        if single_call['arg2'] in frequent:
            frequent[single_call['arg2']] = frequent[single_call['arg2']] + 1
        else:
            frequent[single_call['arg2']] = 1

    counter = 0
    for w in sorted(frequent, key=frequent.get, reverse=True):
        if counter < count:
            top_tokens.append(w)
            counter += 1
        else:
            break


def load_keywords(data_path):
    with open(data_path, newline='') as csvfile:
        keywordsReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for keyword in keywordsReader:
            keywords.append(keyword[0])

# https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
def is_not_blank(s):
    return bool(s and not s.isspace())

def find_datapoints(data_path, mode):
    with open(data_path) as file:
        all_calls = json.load(file)

    calls = []
    for call in all_calls:
        base_and_callee = ""
        if "base" in call:
            if is_not_blank(call["base"]):
                base_and_callee = call["base"] + " . " + call["callee"]
            else:
                base_and_callee = call["callee"]

        single_call = {
            'baseAndCallee': base_and_callee,
            'base': call['base'].strip(),
            'callee': call['callee'].strip(),
            'arg1': call['arg1'].strip(),
            'arg2': call['arg2'].strip(),
            'type1': call['synthesizedArgumentTypes'][0].strip(),
            'type2': call['synthesizedArgumentTypes'][1].strip(),
        }
        calls.append(single_call)

    print('Len of calls: ')
    print(len(calls))

    if mode == 'train':
        file_train = open('file_train.txt', 'w')
        file_buggy_train = open('file_buggy_train.txt', 'w')
        file_dev = open('file_dev.txt', 'w')
        file_buggy_dev = open('file_buggy_dev.txt', 'w')
        split_size = math.floor(len(calls) * 0.9)
        counter = 0

        for call in calls:

            methods = []
            variables = []
            numbers = []
            strings = []
            # print ('Counter: ')
            # print (counter)
            callee = ''
            if call['callee'] in top_tokens or call['callee'] in keywords:
                callee = call['callee']
            elif call['callee'] in methods:
                # print("#")
                callee = 'Method_' + str(methods.index(call['callee']) + 1)
            else:
                # print("$")
                methods.append(call['callee'])
                callee = 'Method_' + str(methods.index(call['callee']) + 1)

            base = ''
            if call['base'] != '':
                if call['base'] in top_tokens or call['base'] in keywords:
                    base = call['base']
                elif call['base'] in variables:
                    # print("#")
                    base = 'Var_' + str(variables.index(call['base']) + 1)
                else:
                    # print("$")
                    variables.append(call['base'])
                    base = 'Var_' + str(variables.index(call['base']) + 1)

            # print(callee)
            arg1 = ''
            if call['arg1'] in top_tokens or call['arg1'] in keywords:
                arg1 = call['arg1']
            elif call['type1'] == 'function':
                if call['arg1'] in methods:
                    arg1 = 'Method_' + str(methods.index(call['arg1']) + 1)
                else:
                    methods.append(call['arg1'])
                    arg1 = 'Method_' + str(methods.index(call['arg1']) + 1)
            elif call['type1'] == 'string':
                if call['arg1'] in strings:
                    arg1 = 'String_' + str(strings.index(call['arg1']) + 1)
                else:
                    strings.append(call['arg1'])
                    arg1 = 'String_' + str(strings.index(call['arg1']) + 1)
            elif call['type1'] == 'number':
                if call['arg1'] in numbers:
                    arg1 = 'Number_' + str(numbers.index(call['arg1']) + 1)
                else:
                    numbers.append(call['arg1'])
                    arg1 = 'Number_' + str(numbers.index(call['arg1']) + 1)
            else:
                if call['arg1'] in variables:
                    arg1 = 'Var_' + str(variables.index(call['arg1']) + 1)
                else:
                    variables.append(call['arg1'])
                    arg1 = 'Var_' + str(variables.index(call['arg1']) + 1)

            arg2 = ''
            if call['arg2'] in top_tokens or call['arg2'] in keywords:
                arg2 = call['arg2']
            elif call['type2'] == 'function':
                if call['arg2'] in methods:
                    arg2 = 'Method_' + str(methods.index(call['arg2']) + 1)
                else:
                    methods.append(call['arg2'])
                    arg2 = 'Method_' + str(methods.index(call['arg2']) + 1)
            elif call['type2'] == 'string':
                if call['arg2'] in strings:
                    arg2 = 'String_' + str(strings.index(call['arg2']) + 1)
                else:
                    strings.append(call['arg2'])
                    arg2 = 'String_' + str(strings.index(call['arg2']) + 1)
            elif call['type2'] == 'number':
                if call['arg2'] in numbers:
                    arg2 = 'Number_' + str(numbers.index(call['arg2']) + 1)
                else:
                    numbers.append(call['arg2'])
                    arg2 = 'Number_' + str(numbers.index(call['arg2']) + 1)
            else:
                if call['arg2'] in variables:
                    arg2 = 'Var_' + str(variables.index(call['arg2']) + 1)
                else:
                    variables.append(call['arg2'])
                    arg2 = 'Var_' + str(variables.index(call['arg2']) + 1)

            if base != '':
                correct = base + ' . ' + callee + ' ( ' + arg1 + ' , ' + arg2 + ' )'
                correct = correct.encode('utf-8', 'replace').decode()
                # buggy = base + ' . ' + callee + ' ( ' + arg2 + ' , ' + arg1 + ' )'
                # buggy = buggy.encode('utf-8', 'replace').decode()
            else:
                correct = callee + ' ( ' + arg1 + ' , ' + arg2 + ' )'
                correct = correct.encode('utf-8', 'replace').decode()
                # buggy = callee + ' ( ' + arg2 + ' , ' + arg1 + ' )'
                # buggy = buggy.encode('utf-8', 'replace').decode()

            type1 = call['type1']
            type2 = call['type2']
            base_and_callee = call['baseAndCallee']
            buggy = base_and_callee + ' ( arg0 ' + type2 + ' , arg1 ' + type1 + ' )'
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
        for call in calls:

            methods = []
            variables = []
            numbers = []
            strings = []
            callee = ''
            if call['callee'] in top_tokens or call['callee'] \
                    in keywords:
                callee = call['callee']
            elif call['callee'] in methods:
                # print("#")
                callee = 'Method_' + str(methods.index(call['callee']) + 1)
            else:
                # print("$")
                methods.append(call['callee'])
                callee = 'Method_' + str(methods.index(call['callee']) + 1)
                # print("&")
            # print(callee)
            base = ''
            if call['base'] != '':
                if call['base'] in top_tokens or call['base'] in keywords:
                    base = call['base']
                elif call['base'] in variables:
                    # print("#")
                    base = 'Var_' + str(variables.index(call['base']) + 1)
                else:
                    # print("$")
                    variables.append(call['base'])
                    base = 'Var_' + str(variables.index(call['base']) + 1)
            arg1 = ''
            if call['arg1'] in top_tokens or call['arg1'] in keywords:
                arg1 = call['arg1']
            elif call['type1'] == 'function':
                if call['arg1'] in methods:
                    arg1 = 'Method_' + str(methods.index(call['arg1']) + 1)
                else:
                    methods.append(call['arg1'])
                    arg1 = 'Method_' + str(methods.index(call['arg1']) + 1)
            elif call['type1'] == 'string':
                if call['arg1'] in strings:
                    arg1 = 'String_' + str(strings.index(call['arg1']) + 1)
                else:
                    strings.append(call['arg1'])
                    arg1 = 'String_' + str(strings.index(call['arg1']) + 1)
            elif call['type1'] == 'number':
                if call['arg1'] in numbers:
                    arg1 = 'Number_' + str(numbers.index(call['arg1']) + 1)
                else:
                    numbers.append(call['arg1'])
                    arg1 = 'Number_' + str(numbers.index(call['arg1']) + 1)
            else:
                if call['arg1'] in variables:
                    arg1 = 'Var_' + str(variables.index(call['arg1']) + 1)
                else:
                    variables.append(call['arg1'])
                    arg1 = 'Var_' + str(variables.index(call['arg1']) + 1)

            arg2 = ''
            if call['arg2'] in top_tokens or call['arg2'] in keywords:
                arg2 = call['arg2']
            elif call['type2'] == 'function':
                if call['arg2'] in methods:
                    arg2 = 'Method_' + str(methods.index(call['arg2']) + 1)
                else:
                    methods.append(call['arg2'])
                    arg2 = 'Method_' + str(methods.index(call['arg2']) + 1)
            elif call['type2'] == 'string':
                if call['arg2'] in strings:
                    arg2 = 'String_' + str(strings.index(call['arg2']) + 1)
                else:
                    strings.append(call['arg2'])
                    arg2 = 'String_' + str(strings.index(call['arg2']) + 1)
            elif call['type2'] == 'number':
                if call['arg2'] in numbers:
                    arg2 = 'Number_' + str(numbers.index(call['arg2']) + 1)
                else:
                    numbers.append(call['arg2'])
                    arg2 = 'Number_' + str(numbers.index(call['arg2']) + 1)
            else:
                if call['arg2'] in variables:
                    arg2 = 'Var_' + str(variables.index(call['arg2']) + 1)
                else:
                    variables.append(call['arg2'])
                    arg2 = 'Var_' + str(variables.index(call['arg2']) + 1)

            if base != '':
                correct = base + ' . ' + callee + ' ( ' + arg1 + ' , ' + arg2 + ' )'
                correct = correct.encode('utf-8', 'replace').decode()
                # buggy = base + ' . ' + callee + ' ( ' + arg2 + ' , ' + arg1 + ' )'
                # buggy = buggy.encode('utf-8', 'replace').decode()
            else:
                correct = callee + ' ( ' + arg1 + ' , ' + arg2 + ' )'
                correct = correct.encode('utf-8', 'replace').decode()
                # buggy = callee + ' ( ' + arg2 + ' , ' + arg1 + ' )'
                # buggy = buggy.encode('utf-8', 'replace').decode()

            type1 = call['type1']
            type2 = call['type2']
            base_and_callee = call['baseAndCallee']
            buggy = base_and_callee + ' ( arg0 ' + type2 + ' , arg1 ' + type1 + ' )'
            buggy = buggy.encode('utf-8', 'replace').decode()

            buggy = stem(buggy)
            correct = stem(correct)

            file_test.write('%s\n' % correct)
            file_buggy_test.write('%s\n' % buggy)
        file_test.close()
        file_buggy_test.close()
    elif mode == 'real-bugs':
        file_real = open('file_real.txt', 'w')
        file_buggy_real = open('file_buggy_real.txt', 'w')
        for call in calls:

            methods = []
            variables = []
            numbers = []
            strings = []
            callee = ''
            if call['callee'] in top_tokens or call['callee'] in keywords:
                callee = call['callee']
            elif call['callee'] in methods:
                # print("#")
                callee = 'Method_' + str(methods.index(call['callee']) + 1)
            else:
                # print("$")
                methods.append(call['callee'])
                callee = 'Method_' + str(methods.index(call['callee']) + 1)
                # print("&")
            # print(callee)
            base = ''
            if call['base'] != '':
                if call['base'] in top_tokens or call['base'] in keywords:
                    base = call['base']
                elif call['base'] in variables:
                    # print("#")
                    base = 'Var_' + str(variables.index(call['base']) + 1)
                else:
                    # print("$")
                    variables.append(call['base'])
                    base = 'Var_' + str(variables.index(call['base']) + 1)
            arg1 = ''
            if call['arg1'] in top_tokens or call['arg1'] in keywords:
                arg1 = call['arg1']
            elif call['type1'] == 'function':
                if call['arg1'] in methods:
                    arg1 = 'Method_' + str(methods.index(call['arg1']) + 1)
                else:
                    methods.append(call['arg1'])
                    arg1 = 'Method_' + str(methods.index(call['arg1']) + 1)
            elif call['type1'] == 'string':
                if call['arg1'] in strings:
                    arg1 = 'String_' + str(strings.index(call['arg1']) + 1)
                else:
                    strings.append(call['arg1'])
                    arg1 = 'String_' + str(strings.index(call['arg1']) + 1)
            elif call['type1'] == 'number':
                if call['arg1'] in numbers:
                    arg1 = 'Number_' + str(numbers.index(call['arg1']) + 1)
                else:
                    numbers.append(call['arg1'])
                    arg1 = 'Number_' + str(numbers.index(call['arg1']) + 1)
            else:
                if call['arg1'] in variables:
                    arg1 = 'Var_' + str(variables.index(call['arg1']) + 1)
                else:
                    variables.append(call['arg1'])
                    arg1 = 'Var_' + str(variables.index(call['arg1']) + 1)

            arg2 = ''
            if call['arg2'] in top_tokens or call['arg2'] in keywords:
                arg2 = call['arg2']
            elif call['type2'] == 'function':
                if call['arg2'] in methods:
                    arg2 = 'Method_' + str(methods.index(call['arg2']) + 1)
                else:
                    methods.append(call['arg2'])
                    arg2 = 'Method_' + str(methods.index(call['arg2']) + 1)
            elif call['type2'] == 'string':
                if call['arg2'] in strings:
                    arg2 = 'String_' + str(strings.index(call['arg2']) + 1)
                else:
                    strings.append(call['arg2'])
                    arg2 = 'String_' + str(strings.index(call['arg2']) + 1)
            elif call['type2'] == 'number':
                if call['arg2'] in numbers:
                    arg2 = 'Number_' + str(numbers.index(call['arg2']) + 1)
                else:
                    numbers.append(call['arg2'])
                    arg2 = 'Number_' + str(numbers.index(call['arg2']) + 1)
            else:
                if call['arg2'] in variables:
                    arg2 = 'Var_' + str(variables.index(call['arg2']) + 1)
                else:
                    variables.append(call['arg2'])
                    arg2 = 'Var_' + str(variables.index(call['arg2']) + 1)

            if base != '':
                correct = base + ' . ' + callee + ' ( ' + arg1 + ' , ' + arg2 + ' )'
                correct = correct.encode('utf-8', 'replace').decode()
                # buggy = base + ' . ' + callee + ' ( ' + arg2 + ' , ' + arg1 + ' )'
                # buggy = buggy.encode('utf-8', 'replace').decode()
            else:
                correct = callee + ' ( ' + arg1 + ' , ' + arg2 + ' )'
                correct = correct.encode('utf-8', 'replace').decode()
                # buggy = callee + ' ( ' + arg2 + ' , ' + arg1 + ' )'
                # buggy = buggy.encode('utf-8', 'replace').decode()

            type1 = call['type1']
            type2 = call['type2']
            base_and_callee = call['baseAndCallee']
            buggy = base_and_callee + ' ( arg0 ' + type2 + ' , arg1 ' + type1 + ' )'
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
    print('Load keyword done')
    find_freq(sys.argv[1], sys.argv[5])
    print('Find freq done')

    find_datapoints(sys.argv[1], 'train')
    print('Train ds done')
    find_datapoints(sys.argv[2], 'test')
    print('Test ds done')
    find_datapoints(sys.argv[3], 'real-bugs')
    print('Real ds done')

