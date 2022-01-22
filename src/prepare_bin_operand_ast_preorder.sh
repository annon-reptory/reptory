#!/bin/bash
#binary operand -> Deepbugs Representation (with Types Incomplete without variable value)

set -x

python3 binoperand_ast_preorder.py ../create-dataset/binOps_dataset/data-training-binOps.json train
python3 binoperand_ast_preorder.py ../create-dataset/binOps_dataset/data-test-binOps.json test
python3 binoperand_ast_preorder.py ../create-dataset/real-bugs-dataset/operands/fixed/data-training-binOps.json real

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
