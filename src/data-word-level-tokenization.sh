#!/bin/bash

set -x

rm -rf '../tensorflow/data/TrainData/'
rm -rf '../tensorflow/data/TestData/'
rm -rf '../tensorflow/data/DevData/'
rm -rf '../tensorflow/data/Vocab'

npm run cleandir

npm run preProcessData

npm run tokenize

npm run generate_vocab

python commonvocab.py 5 10000

cp -r './Vocab' '../tensorflow/data/Vocab'

dataDir='./TrainData/' correctDir='TokensTrainCorrect/' buggyDir='TokensTrainBuggy/' npm run data
cp -r './TrainData/' '../tensorflow/data/TrainData'

dataDir='./TestData/' correctDir='TokensTestCorrect/' buggyDir='TokensTestBuggy/' npm run data
cp -r './TestData/' '../tensorflow/data/TestData'

dataDir='./DevData/' correctDir='TokensDevCorrect/' buggyDir='TokensDevBuggy/' npm run data
cp -r './DevData/' '../tensorflow/data/DevData'

#rm -rf './Vocab/'
#npm run cleandir

echo "done"