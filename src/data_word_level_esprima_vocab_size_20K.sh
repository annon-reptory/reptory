#!/bin/bash

set -x

rm -rf '../tensorflow/data/TrainData/'
rm -rf '../tensorflow/data/TestData/'
rm -rf '../tensorflow/data/DevData/'
rm -rf '../tensorflow/data/RealBugs'
rm -rf '../tensorflow/data/Vocab'

mkdir -p '../tensorflow/data/'

npm run cleandir

cp -p ../create-dataset/real-bugs-dataset/calls/fixed/data-training-calls.json data/real-bugs-calls.json

#npm run preProcessData
node --max-old-space-size=4096 preProcessData_just_add_space.js

#npm run processdata
node tokenize_esprima.js
node generate_vocab_esprima.js
python commonvocab.py 2 20000

cp -r './Vocab' '../tensorflow/data/Vocab'

dataDir='./TrainData/' correctDir='TokensTrainCorrect/' buggyDir='TokensTrainBuggy/' node data_word_level_esprima.js
cp -r './TrainData/' '../tensorflow/data/TrainData'

dataDir='./TestData/' correctDir='TokensTestCorrect/' buggyDir='TokensTestBuggy/' node data_word_level_esprima.js
cp -r './TestData/' '../tensorflow/data/TestData'

dataDir='./DevData/' correctDir='TokensDevCorrect/' buggyDir='TokensDevBuggy/' node data_word_level_esprima.js
cp -r './DevData/' '../tensorflow/data/DevData'

dataDir='./RealBugsData/' correctDir='TokensRealBugsCorrect/' buggyDir='TokensRealBugsBuggy/' node data_word_level_esprima.js
cp -r './RealBugsData/' '../tensorflow/data/RealBugs'

#rm -rf './Vocab/'
#npm run cleandir

echo "done"

echo "generate embedding:"
./getEmbeddings-vocab-size-20k.sh

