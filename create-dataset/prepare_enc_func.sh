#!/bin/bash

set -x

python3 rawCodeParser.py calls_dataset/calls_extra_train.txt calls train
python3 rawCodeParser.py calls_dataset/calls_extra_test.txt calls test

rm -rf ../context-ml/tensorflow/data
mkdir ../context-ml/tensorflow/data
mkdir ../context-ml/tensorflow/data/TestData
mkdir ../context-ml/tensorflow/data/TrainData
mkdir ../context-ml/tensorflow/data/DevData

mv ./enc_f_file_train.txt ../context-ml/tensorflow/data/TrainData/train.correct
mv ./enc_f_file_buggy_train.txt ../context-ml/tensorflow/data/TrainData/train.buggy
mv ./enc_f_file_dev.txt ../context-ml/tensorflow/data/DevData/dev.correct
mv ./enc_f_file_buggy_dev.txt ../context-ml/tensorflow/data/DevData/dev.buggy
mv ./enc_f_file_test.txt ../context-ml/tensorflow/data/TestData/test.correct
mv ./enc_f_file_buggy_test.txt ../context-ml/tensorflow/data/TestData/test.buggy


