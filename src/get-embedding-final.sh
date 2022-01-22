#!/bin/bash

set -x

start_time="$(date -u +%s)"

rm -rf ./embedding
mkdir ./embedding

cat ../tensorflow/data/DevData/*.correct ../tensorflow/data/TrainData/*.correct > ./embedding/corpus.correct
cat ../tensorflow/data/DevData/*.buggy ../tensorflow/data/TrainData/*.buggy > ./embedding/corpus.buggy

python word2vec.py ./embedding/corpus.correct ./embedding/vocab.correct ./embedding/embedding.correct 512
python word2vec.py ./embedding/corpus.buggy ./embedding/vocab.buggy ./embedding/embedding.buggy 512

rm -rf ../tensorflow/data/Vocab
mkdir ../tensorflow/data/Vocab

rm -rf ../tensorflow/data/Embedding
mkdir ../tensorflow/data/Embedding

cp ./embedding/vocab.correct ../tensorflow/data/Vocab
cp ./embedding/embedding.correct ../tensorflow/data/Embedding
cp ./embedding/vocab.buggy ../tensorflow/data/Vocab
cp ./embedding/embedding.buggy ../tensorflow/data/Embedding

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "training time for embedding=$elapsed seconds"