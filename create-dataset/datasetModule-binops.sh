#!/bin/bash

set -x

rm -rf binOps_dataset
mkdir binOps_dataset
mkdir binOps_dataset/binOps_complete_train
mkdir binOps_dataset/binOps_complete_test
time node extractFromJS.js binOps --parallel 16 programs_training.txt data/

mv binOps_complete_*.json binOps_dataset/binOps_complete_train/
cat binOps_extra_*.txt > binOps_dataset/binOps_extra_train.txt
rm binOps_extra_*.txt

time node extractFromJS.js binOps --parallel 16 programs_eval.txt data/

mv binOps_complete_*.json binOps_dataset/binOps_complete_test/
cat binOps_extra_*.txt > binOps_dataset/binOps_extra_test.txt
rm binOps_extra_*.txt

python3 UniqueBinOpsAll.py --trainingData binOps_dataset/binOps_complete_train/binOps_complete_*.json --validationData binOps_dataset/binOps_complete_test/binOps_complete_*.json > binOps_dataset/stats.txt

rm data-training-all-binOps.json

mv data-training-binOps.json data-test-binOps.json binOps_dataset

rm -rf binOps_dataset/binOps_complete_train
rm -rf binOps_dataset/binOps_complete_test




