import sys
import json
from os.path import join
from os import getcwd
from collections import Counter, namedtuple
import math
import random
import time
import numpy as np
import Util
import json

training_binops = []
test_binops = []
compact_training_binops = []
compact_test_binops = []
compact_training_binops_dict = {}
compact_test_binops_dict = {}

def parse_data_paths(args):
    training_data_paths = []
    eval_data_paths = []
    mode = None
    for arg in args:
        if arg == "--trainingData":
            assert mode == None
            mode = "trainingData"
        elif arg == "--validationData":
            assert mode == "trainingData"
            mode = "validationData"
        else:
            path = join(getcwd(), arg)
            if mode == "trainingData":
                training_data_paths.append(path)
            elif mode == "validationData":
                eval_data_paths.append(path)
            else:
                print("Incorrect arguments")
                sys.exit(0)
    return [training_data_paths, eval_data_paths]

def find_unique_binops(data_paths, type, counter):
    
    leftType = ""
    rightType = ""
    for binop in Util.DataReader(data_paths):

        single_binop = {
            "left" : binop["leftOperand"],
            "right": binop["rightOperand"],
            "op": binop["original"]["op"]
        }

        types = binop["original"];
        leftType = types["leftType"];
        rightType = types["rightType"];

        hasType = 0;
        if leftType != "unknown" and rightType != "unknown":
            hasType = 1;
            
        single_binop_json_key = json.dumps(single_binop)

        if type == 1:
            training_binops.append(binop)
            compact_training_binops.append(binop)
            compact_training_binops_dict[single_binop_json_key] = single_binop
            if hasType == 1:
                counter = counter + 1

        if type == 2:
            test_binops.append(binop)
            if single_binop_json_key not in compact_training_binops_dict and single_binop_json_key not in compact_test_binops_dict:
                compact_test_binops.append(binop)
                compact_test_binops_dict[single_binop_json_key] = single_binop
                if hasType == 1:
                    counter = counter + 1
    return counter;
    

if __name__ == '__main__':

    time_start = time.time()
    training_data_paths, validation_data_paths = parse_data_paths(sys.argv[1:])

    hasType_train = 0;
    hasType_test = 0;

    hasType_train = find_unique_binops(training_data_paths, 1, 0)
    hasType_test = find_unique_binops(validation_data_paths, 2, 0)

    print("training: ",len(training_binops), " eval: ", len(test_binops), " compact_train_binops: ", len(compact_training_binops) ," compact_test_binops: ", len(compact_test_binops))
    print("hasType train: ", hasType_train, " hasType test: ", hasType_test);

    json_object = json.dumps(training_binops[:math.floor(len(training_binops)/10)], indent = 2)
    with open('data-training-all-binOps.json', 'w') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)/10):math.floor(len(training_binops)*2/10)], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)*2/10):math.floor(len(training_binops)*3/10)], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)*3/10):math.floor(len(training_binops)*4/10)], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)*4/10):math.floor(len(training_binops)*5/10)], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)*5/10):math.floor(len(training_binops)*6/10)], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)*6/10):math.floor(len(training_binops)*7/10)], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)*7/10):math.floor(len(training_binops)*8/10)], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)*8/10):math.floor(len(training_binops)*9/10)], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_binops[math.floor(len(training_binops)*9/10):], indent = 2)
    with open('data-training-all-binOps.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(compact_test_binops, indent = 2)
    with open('data-test-binOps.json', 'w') as outfile:
        outfile.write(json_object)


    file = open('data-training-all-binOps.json', mode='rt', encoding='ISO-8859-1')
    text = file.read()
    file.close()
    file = open('data-training-binOps.json', mode='wt', encoding='ISO-8859-1')
    text_replaced = text.strip().replace('][', ',').strip()
    file.write("%s" % text_replaced)
    file.close()
    
    
