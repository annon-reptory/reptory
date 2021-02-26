#!/bin/bash

set -x

rm -rf calls_dataset
mkdir calls_dataset
mkdir calls_dataset/calls_complete_train
mkdir calls_dataset/calls_complete_test
time node extractFromJS.js calls --parallel 16 data/js/programs_50_training.txt data/js/programs_50

mv calls_complete_*.json calls_dataset/calls_complete_train/
cat calls_extra_*.txt > calls_dataset/calls_extra_train.txt
rm calls_extra_*.txt

time node extractFromJS.js calls --parallel 16 data/js/programs_50_eval.txt data/js/programs_50

mv calls_complete_*.json calls_dataset/calls_complete_test/
cat calls_extra_*.txt > calls_dataset/calls_extra_test.txt
rm calls_extra_*.txt

python3 UniqueCallsAllWithTypes.py --trainingData calls_dataset/calls_complete_train/calls_complete_*.json --validationData calls_dataset/calls_complete_test/calls_complete_*.json > calls_dataset/stats.txt

rm data-training-all-calls.json

mv data-training-calls.json data-test-calls.json calls_dataset

rm -rf calls_dataset/calls_complete_train
rm -rf calls_dataset/calls_complete_test




