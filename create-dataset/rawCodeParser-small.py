import sys
import re
import math
import json

rawCode = {}
rawCode_test = {}

def read_text(filename):
    file = open(filename, mode='rt', encoding='ISO-8859-1')
    text = file.read()
    file.close()
    return text


def to_objects_calls_train(text):
    objects = text.strip().split('datapoint_separator')

    split_size = math.floor(len(objects)*0.9);
    counter = 0;

    enc_f_file_train = open('enc_f_file_train.txt', 'w')
    enc_f_file_buggy_train = open('enc_f_file_buggy_train.txt', 'w')
    enc_f_file_dev = open('enc_f_file_dev.txt', 'w')
    enc_f_file_buggy_dev = open('enc_f_file_buggy_dev.txt', 'w')

    for one_object in objects:
        single_object = one_object.strip().split('field_separator')
        if len(single_object) != 10:
            continue
        single_rawCode = {
            # 'arg1': single_object[1].strip(),
            # 'arg2': single_object[2].strip(),
            # 'correct_call': re.sub(' +', ' ', single_object[3].strip().replace('\n', '').strip()),
            # 'buggy_call': re.sub(' +', ' ', single_object[4].strip().replace('\n', '').strip()),
            'enclosing_function': re.sub(' +', ' ', single_object[5].strip().replace('\n', '').strip()),
            'buggy_enclosing_function': re.sub(' +', ' ', single_object[6].strip().replace('\n', '').strip()),
            # 'surrounding_statement': re.sub(' +', ' ', single_object[7].strip().replace('\n', '').strip()),
            # 'buggy_surrounding_statement': re.sub(' +', ' ', single_object[8].strip().replace('\n', '').strip()),
            # 'callee': single_object[9].strip()
        }

        key = json.dumps(single_rawCode['enclosing_function'])
        
        rawCode[key] = 1;
        if counter < split_size:
            enc_f_file_train.write("%s\n"  % single_rawCode['enclosing_function'])
            enc_f_file_buggy_train.write("%s\n" % single_rawCode['buggy_enclosing_function'])
        else:
            enc_f_file_dev.write("%s\n"  % single_rawCode['enclosing_function'])
            enc_f_file_buggy_dev.write("%s\n" % single_rawCode['buggy_enclosing_function'])
        counter += 1;

    enc_f_file_train.close()
    enc_f_file_buggy_train.close()
    enc_f_file_dev.close()
    enc_f_file_buggy_dev.close()

def to_objects_calls_test(text):
    objects = text.strip().split('datapoint_separator')

    enc_f_file_test = open('enc_f_file_test.txt', 'w')
    enc_f_file_buggy_test = open('enc_f_file_buggy_test.txt', 'w')

    for one_object in objects:
        single_object = one_object.strip().split('field_separator')
        if len(single_object) != 10:
            continue
        single_rawCode = {
            # 'arg1': single_object[1].strip(),
            # 'arg2': single_object[2].strip(),
            # 'correct_call': re.sub(' +', ' ', single_object[3].strip().replace('\n', '').strip()),
            # 'buggy_call': re.sub(' +', ' ', single_object[4].strip().replace('\n', '').strip()),
            'enclosing_function': re.sub(' +', ' ', single_object[5].strip().replace('\n', '').strip()),
            'buggy_enclosing_function': re.sub(' +', ' ', single_object[6].strip().replace('\n', '').strip()),
            # 'surrounding_statement': re.sub(' +', ' ', single_object[7].strip().replace('\n', '').strip()),
            # 'buggy_surrounding_statement': re.sub(' +', ' ', single_object[8].strip().replace('\n', '').strip()),
            # 'callee': single_object[9].strip()
        }

        key = json.dumps(single_rawCode['enclosing_function'])

        if key not in rawCode_test and key not in rawCode:
            rawCode_test[key] = single_rawCode;
        
    for key in rawCode_test:
        enc_f_file_test.write("%s\n"  % rawCode_test[key]['enclosing_function'])
        enc_f_file_buggy_test.write("%s\n" % rawCode_test[key]['buggy_enclosing_function'])

    enc_f_file_test.close()
    enc_f_file_buggy_test.close()

def to_objects_binops(text):
    single_object = text.strip().split('field_separator')
    rawCode = {
        'correct': single_object[0].strip(),
        'buggy_operand': single_object[1].strip(),
        'buggy_operator': single_object[2].strip(),
        'enclosing_function': single_object[3].strip(),

    }
    return rawCode


if __name__ == '__main__':

    filename = sys.argv[1]
    mode = sys.argv[2]
    train_or_test = sys.argv[3]
    data = read_text(filename)
    if mode == "calls":
        if train_or_test == "train":
            to_objects_calls_train(data)
        elif train_or_test == "test":
            to_objects_calls_test(data)
    elif mode == "binops":
        to_objects_binops(data)

