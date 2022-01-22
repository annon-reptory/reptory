#!/bin/bash

set -x

rm -rf '../tensorflow/data/TrainData/'
rm -rf '../tensorflow/data/TestData/'
rm -rf '../tensorflow/data/DevData/'
rm -rf '../tensorflow/data/Vocab'

npm run cleandir

#npm run preProcessData
node --max-old-space-size=4096 preProcessDataSynthesized_without_id_lit.js

#npm run processdata
node tokenize_esprima.js
node generate_vocab_esprima.js
python commonvocab.py 2 30000

cp -r './Vocab' '../tensorflow/data/Vocab'

dataDir='./TrainData/' correctDir='TokensTrainCorrect/' buggyDir='TokensTrainBuggy/' node data_word_level_esprima.js
cp -r './TrainData/' '../tensorflow/data/TrainData'

dataDir='./TestData/' correctDir='TokensTestCorrect/' buggyDir='TokensTestBuggy/' node data_word_level_esprima.js
cp -r './TestData/' '../tensorflow/data/TestData'

dataDir='./DevData/' correctDir='TokensDevCorrect/' buggyDir='TokensDevBuggy/' node data_word_level_esprima.js
cp -r './DevData/' '../tensorflow/data/DevData'

#rm -rf './Vocab/'
#npm run cleandir

echo "dataset generation - done"
