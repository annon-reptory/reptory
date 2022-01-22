#!/bin/bash

set -x

cp -p ../create-dataset/real-bugs-dataset/calls/fixed/data-training-calls.json dataset/real-bugs-calls.json
python3 calls_code_simplification_signatures_with_position_anchor_to_tufano_abstraction.py ./dataset/data-training-calls.json ./dataset/data-test-calls.json ./dataset/real-bugs-calls.json ../create-dataset/keywords.csv 300

rm -rf ../tensorflow/data
mkdir ../tensorflow/data
mkdir ../tensorflow/data/TestData
mkdir ../tensorflow/data/TrainData
mkdir ../tensorflow/data/DevData
mkdir ../tensorflow/data/RealBugs

mv ./file_train.txt ../tensorflow/data/TrainData/train.correct
mv ./file_buggy_train.txt ../tensorflow/data/TrainData/train.buggy
mv ./file_dev.txt ../tensorflow/data/DevData/dev.correct
mv ./file_buggy_dev.txt ../tensorflow/data/DevData/dev.buggy
mv ./file_test.txt ../tensorflow/data/TestData/test.correct
mv ./file_buggy_test.txt ../tensorflow/data/TestData/test.buggy
mv ./file_real.txt ../tensorflow/data/RealBugs/realbugs.correct
mv ./file_buggy_real.txt ../tensorflow/data/RealBugs/realbugs.buggy

sh get-embedding-final.sh

cd ../tensorflow
echo "training - started"
./train-final-save-log.sh
echo "training - done"

