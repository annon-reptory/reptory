import sys
import re
import math
import json
import esprima

rawCode = {}
rawCode_test = {}

def read_text(filename):
    file = open(filename, mode='rt', encoding='ISO-8859-1')
    text = file.read()
    file.close()
    return text


def to_objects_calls_train(text, info):
    objects = text.strip().split('datapoint_separator')

    split_size = math.floor(len(objects)*0.9);
    counter = 0;

    file_train = open('file_train.txt', 'w')
    file_buggy_train = open('file_buggy_train.txt', 'w')
    file_dev = open('file_dev.txt', 'w')
    file_buggy_dev = open('file_buggy_dev.txt', 'w')

    for one_object in objects:
        single_object = one_object.strip().split('field_separator')
        if len(single_object) != 10:
            continue

        try:

            correctCall = ""
            temp = esprima.tokenize(single_object[3])
            for item in temp:
                correctCall = correctCall + ' ' + item.value;
            correctCall = re.sub(' +', ' ', correctCall.strip().replace('\n', '').strip())

            buggyEncFunc = ""
            temp = esprima.tokenize(single_object[6])
            for item in temp:
                buggyEncFunc = buggyEncFunc + ' ' + item.value;
            buggyEncFunc = re.sub(' +', ' ', buggyEncFunc.strip().replace('\n', '').strip())

            buggySurr = ""
            temp = esprima.tokenize(single_object[8])
            for item in temp:
                buggySurr = buggySurr + ' ' + item.value;
            buggySurr = re.sub(' +', ' ', buggySurr.strip().replace('\n', '').strip())

            if buggySurr == "" or buggyEncFunc == "" or correctCall == "":
                continue
        
        except:
            print("###")
            continue
        
         
        single_rawCode = {
            # 'arg1': single_object[1].strip(),
            # 'arg2': single_object[2].strip(),
            'correct_call': correctCall,
            #'buggy_call': re.sub(' +', ' ', single_object[4].strip().replace('\n', '').strip()),
            #'enclosing_function': re.sub(' +', ' ', single_object[5].strip().replace('\n', '').strip()),
            'buggy_enclosing_function': buggyEncFunc,
            #'surrounding_statement': re.sub(' +', ' ', single_object[7].strip().replace('\n', '').strip()),
            'buggy_surrounding_statement': buggySurr,
            # 'callee': single_object[9].strip()
        }

        if (info == "surr"):
            key = json.dumps(single_rawCode['buggy_surrounding_statement'])
            
            rawCode[key] = 1;
            if counter < split_size:
                file_train.write("%s\n"  % single_rawCode['correct_call'])
                file_buggy_train.write("%s\n" % single_rawCode['buggy_surrounding_statement'])
            else:
                file_dev.write("%s\n"  % single_rawCode['correct_call'])
                file_buggy_dev.write("%s\n" % single_rawCode['buggy_surrounding_statement'])
            counter += 1;

        elif (info == "enc"):
            key = json.dumps(single_rawCode['buggy_enclosing_function'])
            
            rawCode[key] = 1;
            if counter < split_size:
                file_train.write("%s\n"  % single_rawCode['correct_call'])
                file_buggy_train.write("%s\n" % single_rawCode['buggy_enclosing_function'])
            else:
                file_dev.write("%s\n"  % single_rawCode['correct_call'])
                file_buggy_dev.write("%s\n" % single_rawCode['buggy_enclosing_function'])
            counter += 1;

    file_train.close()
    file_buggy_train.close()
    file_dev.close()
    file_buggy_dev.close()

def to_objects_calls_test(text, info):
    objects = text.strip().split('datapoint_separator')

    file_test = open('file_test.txt', 'w')
    file_buggy_test = open('file_buggy_test.txt', 'w')

    for one_object in objects:
        single_object = one_object.strip().split('field_separator')
        if len(single_object) != 10:
            continue

        try:

            correctCall = ""
            temp = esprima.tokenize(single_object[3])
            for item in temp:
                correctCall = correctCall + ' ' + item.value;
            correctCall = re.sub(' +', ' ', correctCall.strip().replace('\n', '').strip())

            buggyEncFunc = ""
            temp = esprima.tokenize(single_object[6])
            for item in temp:
                buggyEncFunc = buggyEncFunc + ' ' + item.value;
            buggyEncFunc = re.sub(' +', ' ', buggyEncFunc.strip().replace('\n', '').strip())

            buggySurr = ""
            temp = esprima.tokenize(single_object[8])
            for item in temp:
                buggySurr = buggySurr + ' ' + item.value;
            buggySurr = re.sub(' +', ' ', buggySurr.strip().replace('\n', '').strip())

            if buggySurr == "" or buggyEncFunc == "" or correctCall == "":
                continue
        
        except:
            print("@@@")
            continue
        

        single_rawCode = {
            # 'arg1': single_object[1].strip(),
            # 'arg2': single_object[2].strip(),
            'correct_call': correctCall,
            # 'buggy_call': re.sub(' +', ' ', single_object[4].strip().replace('\n', '').strip()),
            #'enclosing_function': re.sub(' +', ' ', single_object[5].strip().replace('\n', '').strip()),
            'buggy_enclosing_function': buggyEncFunc,
            #'surrounding_statement': re.sub(' +', ' ', single_object[7].strip().replace('\n', '').strip()),
            'buggy_surrounding_statement': buggySurr,
            # 'callee': single_object[9].strip()
        }

        if (info == "surr"):
            key = json.dumps(single_rawCode['buggy_surrounding_statement'])
        elif (info == "enc"):
            key = json.dumps(single_rawCode['buggy_enclosing_function'])

        if key not in rawCode_test and key not in rawCode:
            rawCode_test[key] = single_rawCode;
        
    for key in rawCode_test:
        if (info == "surr"):
            file_test.write("%s\n"  % rawCode_test[key]['correct_call'])
            file_buggy_test.write("%s\n" % rawCode_test[key]['buggy_surrounding_statement'])
        elif (info == "enc"):
            file_test.write("%s\n"  % rawCode_test[key]['correct_call'])
            file_buggy_test.write("%s\n" % rawCode_test[key]['buggy_enclosing_function'])

    file_test.close()
    file_buggy_test.close()

def to_objects_binops_test(text, info):
    objects = text.strip().split('datapoint_separator')

    file_test = open('file_test.txt', 'w')
    file_buggy_test = open('file_buggy_test.txt', 'w')

    for one_object in objects:
        single_object = one_object.strip().split('field_separator')
        if len(single_object) != 12:
            continue

        try:

            correctOp = ""
            temp = esprima.tokenize(single_object[1])
            for item in temp:
                correctOp = correctOp + ' ' + item.value;
            correctOp = correctOp.strip();

            enclosingFunction = ""
            temp = esprima.tokenize(single_object[6])
            for item in temp:
                enclosingFunction = enclosingFunction + ' ' + item.value;
            enclosingFunction = enclosingFunction.strip();

            buggyEnclosingFunctionOperand = ""
            temp = esprima.tokenize(single_object[7])
            for item in temp:
                buggyEnclosingFunctionOperand = buggyEnclosingFunctionOperand + ' ' + item.value;
            buggyEnclosingFunctionOperand = buggyEnclosingFunctionOperand.strip();

            buggyEnclosingFunctionOperator = ""
            temp = esprima.tokenize(single_object[8])
            for item in temp:
                buggyEnclosingFunctionOperator = buggyEnclosingFunctionOperator + ' ' + item.value;
            buggyEnclosingFunctionOperator = buggyEnclosingFunctionOperator.strip();

            surroundingStatement = ""
            temp = esprima.tokenize(single_object[9])
            for item in temp:
                surroundingStatement = surroundingStatement + ' ' + item.value;
            surroundingStatement = surroundingStatement.strip();

            buggySurroundingStatementOperand = ""
            temp = esprima.tokenize(single_object[10])
            for item in temp:
                buggySurroundingStatementOperand = buggySurroundingStatementOperand + ' ' + item.value;
            buggySurroundingStatementOperand = buggySurroundingStatementOperand.strip();

            buggySurroundingStatementOperator = ""
            temp = esprima.tokenize(single_object[11])
            for item in temp:
                buggySurroundingStatementOperator = buggySurroundingStatementOperator + ' ' + item.value;
            buggySurroundingStatementOperator = buggySurroundingStatementOperator.strip();

            if correctOp == "" or enclosingFunction == "" or buggyEnclosingFunctionOperand == "" or buggyEnclosingFunctionOperator == "" or surroundingStatement == "" or buggySurroundingStatementOperator == "" or buggySurroundingStatementOperand == "":
                continue
        
        except:
            print("~~~")
            continue
    

        single_rawCode = {
            'correctOp': correctOp,
            'buggyOperand': single_object[2].strip(),
            'buggyOperator': single_object[3].strip(),
            'leftOperand': single_object[4].strip(),
            'rightOperand': single_object[5].strip(),
            'enclosingFunction': enclosingFunction,
            'buggyEnclosingFunctionOperand': buggyEnclosingFunctionOperand,
            'buggyEnclosingFunctionOperator': buggyEnclosingFunctionOperator,
            'surroundingStatement': surroundingStatement,
            'buggySurroundingStatementOperand': buggySurroundingStatementOperand,
            'buggySurroundingStatementOperator': buggySurroundingStatementOperator,
        }

        if (info == "surr-operand" or info == "surr-operator"):
            key = json.dumps(single_rawCode['surroundingStatement'])
        if (info == "enc-operand" or info == "enc-operator"):
            key = json.dumps(single_rawCode['enclosingFunction'])

        if key not in rawCode_test and key not in rawCode:
            rawCode_test[key] = single_rawCode;
        
    for key in rawCode_test:
        if (info == "surr-operand"):
            file_test.write("%s\n"  % rawCode_test[key]['correctOp'])
            file_buggy_test.write("%s\n" % rawCode_test[key]['buggySurroundingStatementOperand'])
        elif(info == "surr-operator"):
            file_test.write("%s\n"  % rawCode_test[key]['correctOp'])
            file_buggy_test.write("%s\n" % rawCode_test[key]['buggySurroundingStatementOperator'])
        elif(info == "enc-operator"):
            file_test.write("%s\n"  % rawCode_test[key]['correctOp'])
            file_buggy_test.write("%s\n" % rawCode_test[key]['buggyEnclosingFunctionOperator'])
        elif(info == "enc-operand"):
            file_test.write("%s\n"  % rawCode_test[key]['correctOp'])
            file_buggy_test.write("%s\n" % rawCode_test[key]['buggyEnclosingFunctionOperand'])

    file_test.close()
    file_buggy_test.close()


def to_objects_binops_train(text, info):
    objects = text.strip().split('datapoint_separator')

    split_size = math.floor(len(objects)*0.9);
    counter = 0;

    file_train = open('file_train.txt', 'w')
    file_buggy_train = open('file_buggy_train.txt', 'w')
    file_dev = open('file_dev.txt', 'w')
    file_buggy_dev = open('file_buggy_dev.txt', 'w')

    for one_object in objects:
        single_object = one_object.strip().split('field_separator')
        if len(single_object) != 12:
            continue

        try:

            correctOp = ""
            temp = esprima.tokenize(single_object[1])
            for item in temp:
                correctOp = correctOp + ' ' + item.value;
            correctOp = correctOp.strip();

            enclosingFunction = ""
            temp = esprima.tokenize(single_object[6])
            for item in temp:
                enclosingFunction = enclosingFunction + ' ' + item.value;
            enclosingFunction = enclosingFunction.strip();

            buggyEnclosingFunctionOperand = ""
            temp = esprima.tokenize(single_object[7])
            for item in temp:
                buggyEnclosingFunctionOperand = buggyEnclosingFunctionOperand + ' ' + item.value;
            buggyEnclosingFunctionOperand = buggyEnclosingFunctionOperand.strip();

            buggyEnclosingFunctionOperator = ""
            temp = esprima.tokenize(single_object[8])
            for item in temp:
                buggyEnclosingFunctionOperator = buggyEnclosingFunctionOperator + ' ' + item.value;
            buggyEnclosingFunctionOperator = buggyEnclosingFunctionOperator.strip();

            surroundingStatement = ""
            temp = esprima.tokenize(single_object[9])
            for item in temp:
                surroundingStatement = surroundingStatement + ' ' + item.value;
            surroundingStatement = surroundingStatement.strip();

            buggySurroundingStatementOperand = ""
            temp = esprima.tokenize(single_object[10])
            for item in temp:
                buggySurroundingStatementOperand = buggySurroundingStatementOperand + ' ' + item.value;
            buggySurroundingStatementOperand = buggySurroundingStatementOperand.strip();

            buggySurroundingStatementOperator = ""
            temp = esprima.tokenize(single_object[11])
            for item in temp:
                buggySurroundingStatementOperator = buggySurroundingStatementOperator + ' ' + item.value;
            buggySurroundingStatementOperator = buggySurroundingStatementOperator.strip();

            if correctOp == "" or enclosingFunction == "" or buggyEnclosingFunctionOperand == "" or buggyEnclosingFunctionOperator == "" or surroundingStatement == "" or buggySurroundingStatementOperator == "" or buggySurroundingStatementOperand == "":
                continue

        except:
            print("&&&")
            continue

        single_rawCode = {
            'correctOp': re.sub(' +', ' ', single_object[1].strip().replace('\n', '').strip()),
            'buggyOperand': single_object[2].strip(),
            'buggyOperator': single_object[3].strip(),
            'leftOperand': single_object[4].strip(),
            'rightOperand': single_object[5].strip(),
            'enclosingFunction': re.sub(' +', ' ', single_object[6].strip().replace('\n', '').strip()),
            'buggyEnclosingFunctionOperand': re.sub(' +', ' ', single_object[7].strip().replace('\n', '').strip()),
            'buggyEnclosingFunctionOperator': re.sub(' +', ' ', single_object[8].strip().replace('\n', '').strip()),
            'surroundingStatement': re.sub(' +', ' ', single_object[9].strip().replace('\n', '').strip()),
            'buggySurroundingStatementOperand': re.sub(' +', ' ', single_object[10].strip().replace('\n', '').strip()),
            'buggySurroundingStatementOperator': re.sub(' +', ' ', single_object[11].strip().replace('\n', '').strip()),
        }

        if (info == "surr-operand"):
            key = json.dumps(single_rawCode['surroundingStatement'])
            
            rawCode[key] = 1;
            if counter < split_size:
                file_train.write("%s\n"  % single_rawCode['correctOp'])
                file_buggy_train.write("%s\n" % single_rawCode['buggySurroundingStatementOperand'])
            else:
                file_dev.write("%s\n"  % single_rawCode['correctOp'])
                file_buggy_dev.write("%s\n" % single_rawCode['buggySurroundingStatementOperand'])
            counter += 1;
        elif(info == "surr-operator"):
            key = json.dumps(single_rawCode['surroundingStatement'])
            
            rawCode[key] = 1;
            if counter < split_size:
                file_train.write("%s\n"  % single_rawCode['correctOp'])
                file_buggy_train.write("%s\n" % single_rawCode['buggySurroundingStatementOperator'])
            else:
                file_dev.write("%s\n"  % single_rawCode['correctOp'])
                file_buggy_dev.write("%s\n" % single_rawCode['buggySurroundingStatementOperator'])
            counter += 1;
        elif(info == "enc-operator"):
            key = json.dumps(single_rawCode['enclosingFunction'])
            
            rawCode[key] = 1;
            if counter < split_size:
                file_train.write("%s\n"  % single_rawCode['correctOp'])
                file_buggy_train.write("%s\n" % single_rawCode['buggyEnclosingFunctionOperator'])
            else:
                file_dev.write("%s\n"  % single_rawCode['correctOp'])
                file_buggy_dev.write("%s\n" % single_rawCode['buggyEnclosingFunctionOperator'])
            counter += 1;
        elif(info == "enc-operand"):
            key = json.dumps(single_rawCode['enclosingFunction'])
            
            rawCode[key] = 1;
            if counter < split_size:
                file_train.write("%s\n"  % single_rawCode['correctOp'])
                file_buggy_train.write("%s\n" % single_rawCode['buggyEnclosingFunctionOperand'])
            else:
                file_dev.write("%s\n"  % single_rawCode['correctOp'])
                file_buggy_dev.write("%s\n" % single_rawCode['buggyEnclosingFunctionOperand'])
            counter += 1;

    file_train.close()
    file_buggy_train.close()
    file_dev.close()
    file_buggy_dev.close()



if __name__ == '__main__':

    filename_train = sys.argv[1]
    filename_test = sys.argv[2]
    mode = sys.argv[3]
    info = sys.argv[4]
    data_train = read_text(filename_train)
    #data_test = read_text(filename_test)
    if mode == "calls":
        to_objects_calls_train(data_train, info)
        data_train = ""
        data_test = read_text(filename_test)
        to_objects_calls_test(data_test, info)
    elif mode == "binops":
        to_objects_binops_train(data_train, info)
        to_objects_binops_test(data_test, info)
