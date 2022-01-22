#!/bin/bash

set -x

rm -rf '../tensorflow/data/TrainData/'
rm -rf '../tensorflow/data/TestData/'
rm -rf '../tensorflow/data/DevData/'
rm -rf '../tensorflow/data/Vocab'

npm run cleandir

#npm run preProcessData
node --max-old-space-size=4096 preProcessData_data_word_level_synthesized_without_variable_ast_to_data_word_level_synthesized_with_ID_LIT.js

#npm run processdata
#npm run tokenize
node tokenize_esprima.js
#npm run generate_vocab
node generate_vocab_esprima.js
python commonvocab.py 2 30000

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


#rm -rf './Vocab/'
#npm run cleandir

echo "dataset generation - done"
