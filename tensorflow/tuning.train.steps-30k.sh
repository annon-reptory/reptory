#!/bin/bash

set -x

rm -rf ./code_model/
start_time="$(date -u +%s)"

echo "start training=$(date -u)"
python -m nmt.nmt \
    --attention=scaled_luong \
    --src=buggy --tgt=correct \
    --vocab_prefix=./data/Vocab/vocab  \
    --train_prefix=./data/TrainData/train \
    --dev_prefix=./data/DevData/dev  \
    --test_prefix=./data/TestData/test \
    --embed_prefix=./data/Embedding/embedding \
    --src_max_len=665 \
    --tgt_max_len=665 \
    --out_dir=./code_model \
    --optimizer=adam \
    --learning_rate=0.001 \
    --decay_scheme=luong5 \
    --max_gradient_norm=4 \
    --batch_size=16 \
    --num_train_steps=30000 \
    --steps_per_stats=100 \
    --num_layers=2 \
    --num_units=512 \
    --dropout=0.1 \
    --metrics=bleu \
    --beam_width=25
echo "end training=$(date -u)"

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "training runtime=$elapsed seconds"

# run inference - test data
start_time="$(date -u +%s)"
echo "start inference on test data=$(date -u)"
./infer-final.sh
echo "end inference=$(date -u)"

end_time="$(date -u +%s)"
echo "inference runtime on test data=$elapsed seconds"

cd data
python calculate_accuracy_and_rank.py test.correct test.buggy model.output

# run inference - real bugs
cd ..
start_time="$(date -u +%s)"
echo "start inference on real bugs=$(date -u)"
./infer-final-real-bugs.sh
echo "end inference=$(date -u)"

end_time="$(date -u +%s)"
echo "inference runtime on real bugs=$elapsed seconds"

cd data
python calculate_accuracy_and_rank.py realbugs.correct realbugs.buggy realbugs.model.output

# save data folder in the code_model directory
cd ..
cp -pR data/ code_model/

