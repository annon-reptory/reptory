#!/bin/bash
#binary operand -> Deepbugs Representation (with Types Incomplete without variable value)

set -x

python3 binoperand-2.py ../create-dataset/binOps_dataset/data-training-binOps.json train
python3 binoperand-2.py ../create-dataset/binOps_dataset/data-test-binOps.json test

rm -rf ../tensorflow/data
mkdir ../tensorflow/data
mkdir ../tensorflow/data/TestData
mkdir ../tensorflow/data/TrainData
mkdir ../tensorflow/data/DevData

mv ./file_buggy_train.txt ../tensorflow/data/TrainData/train.buggy
mv ./file_buggy_dev.txt ../tensorflow/data/DevData/dev.buggy
mv ./file_buggy_test.txt ../tensorflow/data/TestData/test.buggy
rm ./file_test.txt
rm ./file_dev.txt
rm ./file_train.txt

python3 binoperand-4.py ../create-dataset/binOps_dataset/data-training-binOps.json train
python3 binoperand-4.py ../create-dataset/binOps_dataset/data-test-binOps.json test

mv ./file_train.txt ../tensorflow/data/TrainData/train.correct
mv ./file_dev.txt ../tensorflow/data/DevData/dev.correct
mv ./file_test.txt ../tensorflow/data/TestData/test.correct
rm ./file_buggy_train.txt
rm ./file_buggy_dev.txt
rm ./file_buggy_test.txt

sh getEmbeddings.sh
rm -rf ../tensorflow/data/Embedding
