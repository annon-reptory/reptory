import sys
import re
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

training_calls = []
test_calls = []
compact_training_calls = []
compact_test_calls = []
compact_training_calls_dict = {}
compact_test_calls_dict = {}
argument_types = {}
unique_keys_train = {}
unique_keys_test = {} 
rawCodeTrain = {}
rawCodeTest = {}


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

def get_types(data_paths):
    
    types = []
    for call in Util.DataReader(data_paths):
        single_call = {
            "callee" : call["callee"]
        }
        types = call["original"];
        types = types["argumentTypes"];
            
        single_call_json_key = json.dumps(single_call)

        if single_call_json_key not in argument_types:
            argument_types[single_call_json_key] = types
        elif single_call_json_key in argument_types and argument_types[single_call_json_key][0] == "unknown" and types[0] != "unknown":
            argument_types[single_call_json_key][0] = types[0]
        elif single_call_json_key in argument_types and argument_types[single_call_json_key][1] == "unknown" and types[1] != "unknown":
            argument_types[single_call_json_key][1] = types[1]
    all_types = ["number", "string", "boolean", "object", "function", "undefined"]
    for types in argument_types:
        if argument_types[types][0] == "unknown":
            argument_types[types][0] = random.choice(all_types)
        if argument_types[types][1] == "unknown":
            argument_types[types][1] = random.choice(all_types)
    single_call_example = {
        "callee" : "setTimeout"
    }    
    single_call_example_json_key = json.dumps(single_call_example)                
    argument_types[single_call_example_json_key][0] = "function";
    argument_types[single_call_example_json_key][1] = "number";



def find_unique_calls(data_paths, type, counter):
    
    types = []
    for call in Util.DataReader(data_paths):
        arg_type = {
            "callee" : call["callee"]
        }
        single_call = {
            "callee" : call["callee"],
            "arg1" : call["arg1"],
            "arg2" : call["arg2"]
        }
            
        single_call_json_key = json.dumps(single_call)
        arg_type_json_key = json.dumps(arg_type)

        call["synthesizedArgumentTypes"][0] = argument_types[arg_type_json_key][0]
        call["synthesizedArgumentTypes"][1] = argument_types[arg_type_json_key][1]

        types = call["original"];
        types = types["argumentTypes"];
    

        hasType = 0;
        if "unknown" not in types:
            hasType = 1;

        if type == 1:
            training_calls.append(call)
            compact_training_calls.append(call)
            compact_training_calls_dict[single_call_json_key] = single_call
            if hasType == 1:
                counter = counter + 1

        if type == 2:
            test_calls.append(call)
            if single_call_json_key not in compact_training_calls_dict and single_call_json_key not in compact_test_calls_dict:
                compact_test_calls.append(call)
                compact_test_calls_dict[single_call_json_key] = single_call
                if hasType == 1:
                    counter = counter + 1
    return counter;

if __name__ == '__main__':

    time_start = time.time()
    training_data_paths, validation_data_paths = parse_data_paths(sys.argv[1:])

    hasType_train = 0;
    hasType_test = 0;

    get_types(training_data_paths);
    get_types(validation_data_paths);

    hasType_train = find_unique_calls(training_data_paths, 1, 0)
    hasType_test = find_unique_calls(validation_data_paths, 2, 0)

    print("training: ",len(training_calls), " eval: ", len(test_calls), " compact_train_calls: ", len(compact_training_calls) ," compact_test_calls: ", len(compact_test_calls))
    print("hasType train: ", hasType_train, " hasType test: ", hasType_test);

    json_object = json.dumps(training_calls[:int(math.floor(len(training_calls)/5))], indent = 2)
    with open('data-training-all-calls.json', 'w') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_calls[int(math.floor(len(training_calls)/5)):int(math.floor(len(training_calls)*2/5))], indent = 2)
    with open('data-training-all-calls.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_calls[int(math.floor(len(training_calls)*2/5)):int(math.floor(len(training_calls)*3/5))], indent = 2)
    with open('data-training-all-calls.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_calls[int(math.floor(len(training_calls)*3/5)):int(math.floor(len(training_calls)*4/5))], indent = 2)
    with open('data-training-all-calls.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(training_calls[int(math.floor(len(training_calls))*4/5):], indent = 2)
    with open('data-training-all-calls.json', 'a') as outfile:
        outfile.write(json_object)

    json_object = json.dumps(compact_test_calls, indent = 2)
    with open('data-test-calls.json', 'w') as outfile:
        outfile.write(json_object)

    file = open('data-training-all-calls.json', mode='rt', encoding='ISO-8859-1')
    text = file.read()
    file.close()
    file = open('data-training-calls.json', mode='wt', encoding='ISO-8859-1')
    text_replaced = text.strip().replace('][', ',').strip()
    file.write("%s" % text_replaced)
    file.close()

    #parse_raw_code('calls_dataset/calls_extra_train.txt', 'train')
    #parse_raw_code('calls_dataset/calls_extra_test.txt', 'test')

    
    
