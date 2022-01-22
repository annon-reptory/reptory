#!/bin/bash

rm './data/model.output'
rm './data/test.buggy'
rm './data/test.correct'

cp -p './data/TestData/test.buggy' './data/test.buggy'

echo "start inference=$(date -u)"
python -m nmt.nmt \
    --out_dir=./code_model \
    --inference_input_file=./data/test.buggy \
    --inference_output_file=./data/model.output \
    --num_translations_per_input=25 \
    --beam_width=25 \
    --infer_mode=beam_search \
    --coverage_penalty_weight=0.0
echo "end inference=$(date -u)"

cp -p './data/TestData/test.correct' './data/test.correct'
cp -p 'calculate_accuracy_and_rank.py' './data/calculate_accuracy_and_rank.py'