#!/bin/bash

set -x

#Get enclosing function for calls
python3 rawCodeParser-v2.py ../create-dataset/calls_dataset/calls_extra_train.txt ../create-dataset/calls_dataset/calls_extra_test.txt calls enc
#Get surrounding statements for calls
#python3 rawCodeParser-v2.py ../create-dataset/calls_dataset/calls_extra_train.txt ../create-dataset/calls_dataset/calls_extra_test.txt calls surr
#Get enclosing function for wrong binary operands
#python3 rawCodeParser-v2.py ../create-dataset/binOps_dataset/binOps_extra_train.txt ../create-dataset/binOps_dataset/binOps_extra_test.txt binops enc-operand
#Get enclosing function for wrong binary operators
#python3 rawCodeParser-v2.py ../create-dataset/binOps_dataset/binOps_extra_train.txt ../create-dataset/binOps_dataset/binOps_extra_test.txt binops enc-operator
#Get surrounding statements for wrong binary operands
#python3 rawCodeParser-v2.py ../create-dataset/binOps_dataset/binOps_extra_train.txt ../create-dataset/binOps_dataset/binOps_extra_test.txt binops surr-operand
#Get surrounding statements for wrong binary operators
#python3 rawCodeParser-v2.py ../create-dataset/binOps_dataset/binOps_extra_train.txt ../create-dataset/binOps_dataset/binOps_extra_test.txt binops surr-operator

rm -rf ../tensorflow/data
mkdir ../tensorflow/data
mkdir ../tensorflow/data/TestData
mkdir ../tensorflow/data/TrainData
mkdir ../tensorflow/data/DevData

mv ./file_train.txt ../tensorflow/data/TrainData/train.correct
mv ./file_buggy_train.txt ../tensorflow/data/TrainData/train.buggy
mv ./file_dev.txt ../tensorflow/data/DevData/dev.correct
mv ./file_buggy_dev.txt ../tensorflow/data/DevData/dev.buggy
mv ./file_test.txt ../tensorflow/data/TestData/test.correct
mv ./file_buggy_test.txt ../tensorflow/data/TestData/test.buggy


