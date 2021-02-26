#!/bin/bash

set -x

rm -rf ./dataset ./vocab.txt ./vectors.txt ./vectors.bin ./cooccurrence.bin ./cooccurrence.shuf.bin

rm -rf ../tensorflow/data/Vocab

mkdir ../tensorflow/data/Vocab

rm -rf ../tensorflow/data/Embedding

mkdir ../tensorflow/data/Embedding


cat ../tensorflow/data/DevData/*.correct ../tensorflow/data/TrainData/*.correct > ./dataset
./getGlove.sh
python3 vocab_parser.py
mv ./vocab_parsed.txt ../tensorflow/data/Vocab/vocab.correct
mv ./vectors_parsed.txt ../tensorflow/data/Embedding/embedding.correct


rm -rf ./dataset ./vocab.txt ./vectors.txt ./vectors.bin ./cooccurrence.bin ./cooccurrence.shuf.bin
cat ../tensorflow/data/DevData/*.buggy ../tensorflow/data/TrainData/*.buggy > ./dataset
./getGlove.sh
python3 vocab_parser.py
mv ./vocab_parsed.txt ../tensorflow/data/Vocab/vocab.buggy
mv ./vectors_parsed.txt ../tensorflow/data/Embedding/embedding.buggy





