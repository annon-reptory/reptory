#!/bin/bash

set -x

rm -rf ./code_model/
mkdir ./code_model/

./train-final-ast-preorder.sh  2>&1 | tee ./code_model/all-training-inference-stats.log
