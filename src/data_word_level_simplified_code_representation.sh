#!/bin/bash

set -x

rm -rf '../tensorflow/data/TrainData/'
rm -rf '../tensorflow/data/TestData/'
rm -rf '../tensorflow/data/DevData/'
rm -rf '../tensorflow/data/Vocab'

npm run cleandir

#npm run preProcessData
node --max-old-space-size=4096 preProcessDataSimplifiedCodeRepresentation.js

#npm run processdata
npm run tokenize
npm run generate_vocab
python commonvocab.py 1 500000

cp -r './Vocab' '../tensorflow/data/Vocab'

dataDir='./TrainData/' correctDir='TokensTrainCorrect/' buggyDir='TokensTrainBuggy/' npm run dataWordLevel
cp -r './TrainData/' '../tensorflow/data/TrainData'

dataDir='./TestData/' correctDir='TokensTestCorrect/' buggyDir='TokensTestBuggy/' npm run dataWordLevel
cp -r './TestData/' '../tensorflow/data/TestData'

dataDir='./DevData/' correctDir='TokensDevCorrect/' buggyDir='TokensDevBuggy/' npm run dataWordLevel
cp -r './DevData/' '../tensorflow/data/DevData'

#rm -rf './Vocab/'
#npm run cleandir

echo "dataset generation - done"
