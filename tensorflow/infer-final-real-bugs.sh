#!/bin/bash

rm './data/realbugs.model.output'
rm './data/realbugs.buggy'
rm './data/realbugs.correct'

cp -p './data/RealBugs/realbugs.buggy' './data/realbugs.buggy'

echo "start inference=$(date -u)"
python -m nmt.nmt \
    --out_dir=./code_model \
    --inference_input_file=./data/realbugs.buggy \
    --inference_output_file=./data/realbugs.model.output \
    --num_translations_per_input=25 \
    --beam_width=25 \
    --infer_mode=beam_search \
    --coverage_penalty_weight=0.0
echo "end inference=$(date -u)"

cp -p './data/RealBugs/realbugs.correct' './data/realbugs.correct'
cp -p 'calculate_accuracy_and_rank.py' './data/calculate_accuracy_and_rank.py'