#!/bin/bash

set -x

rm -rf '../tensorflow/data/TrainData/'
rm -rf '../tensorflow/data/TestData/'
rm -rf '../tensorflow/data/DevData/'
rm -rf '../tensorflow/data/RealBugs'
rm -rf '../tensorflow/data/Vocab'
mkdir -p '../tensorflow/data/'

npm run cleandir

cp -p ../create-dataset/real-bugs-dataset/calls/fixed/data-training-calls.json dataset/real-bugs-calls.json

#npm run preProcessData
node --max-old-space-size=4096 calls_ast_preorder.js

#npm run processdata
#npm run tokenize
node tokenize_esprima.js
#npm run generate_vocab
node generate_vocab_esprima.js
python3 commonvocab.py 1 30000

cp -r './Vocab' '../tensorflow/data/Vocab'

#dataDir='./TrainData/' correctDir='TokensTrainCorrect/' buggyDir='TokensTrainBuggy/' astCorrectDir="./ASTsTrainCorrect/"  astBuggyDir="./ASTsTrainBuggy/" node  data_word_level_ast.js
#cp -r './TrainData/' '../tensorflow/data/TrainData'
#
#dataDir='./TestData/' correctDir='TokensTestCorrect/' buggyDir='TokensTestBuggy/' astCorrectDir="./ASTsTestCorrect/"  astBuggyDir="./ASTsTestBuggy/" node data_word_level_ast.js
#cp -r './TestData/' '../tensorflow/data/TestData'
#
#dataDir='./DevData/' correctDir='TokensDevCorrect/' buggyDir='TokensDevBuggy/' astCorrectDir="./ASTsDevCorrect/"  astBuggyDir="./ASTsDevBuggy/" node  data_word_level_ast.js
#cp -r './DevData/' '../tensorflow/data/DevData'

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

echo "dataset generation - done"

echo "embedding generation - started"
./get-embedding-final.sh
echo "embedding generation - done"

cd ../tensorflow
echo "training - started"
./train-final-ast-preorder-save-log.sh
echo "training - done"

