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
    --num_train_steps=20000 \
    --steps_per_stats=100 \
    --num_layers=4 \
    --num_units=512 \
    --dropout=0.2 \
    --metrics=bleu \
    --beam_width=25
echo "end training=$(date -u)"

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "runtime=$elapsed seconds"

# run inference after training
echo "start inference=$(date -u)"
./tuning.infer.beam.sh
echo "end inference=$(date -u)"

# run accuracy calculation after inference
cd data
python calculate_accuracy_and_rank.py test.correct test.buggy model.output

# save data folder in the code_model directory
cd ..
cp -pR data/ code_model/