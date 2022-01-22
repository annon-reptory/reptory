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

#training_binops = ""
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

def find_unique_binops(data_paths, type):

    training_binops = ""

    for binop in Util.DataReader(data_paths):

        binop_correct = binop["correct_op"];
        binop_operand_buggy = binop["buggy_operand"];
        #binop_operator_buggy = binop["buggy_operator"];

        if type == 1 or type == 3:
            training_binops = training_binops + binop_correct + '\n'
        if type == 2 or type == 4:
            training_binops = training_binops +  binop_operand_buggy + '\n'
        #compact_test_binops2.append(binop_operator_buggy)
    return training_binops

    

if __name__ == '__main__':

    time_start = time.time()
    training_data_paths, validation_data_paths = parse_data_paths(sys.argv[1:])

    type = 1;

    training_binops = find_unique_binops(training_data_paths, type)
    #hasType_test = find_unique_binops(validation_data_paths, type)


    if type == 1:
        filename = "train.correct";
        lastfilename = "dev.correct"

    if type == 2:
        filename = "train.buggy";
        lastfilename = "dev.buggy"

    if type == 3:
        filename = "test.correct";
        lastfilename = "test.correct"

    if type == 4:
        filename = "test.buggy";
        lastfilename = "test.buggy"

   
    with open(filename, 'w') as outfile:
        outfile.write(training_binops[:math.floor(len(training_binops)/10)])

    with open(filename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)/10):math.floor(len(training_binops)*2/10)])

    with open(filename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)*2/10):math.floor(len(training_binops)*3/10)])

    with open(filename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)*3/10):math.floor(len(training_binops)*4/10)])

    with open(filename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)*4/10):math.floor(len(training_binops)*5/10)])

    with open(filename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)*5/10):math.floor(len(training_binops)*6/10)])

    with open(filename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)*6/10):math.floor(len(training_binops)*7/10)])

    with open(filename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)*7/10):math.floor(len(training_binops)*8/10)])

    with open(filename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)*8/10):math.floor(len(training_binops)*9/10)])

    with open(lastfilename, 'a') as outfile:
        outfile.write(training_binops[math.floor(len(training_binops)*9/10):])

    
    
