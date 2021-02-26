#!/bin/bash

rm 'data/code_infer.correct'

python -m nmt.nmt \
    --out_dir=./code_model \
    --inference_input_file=./data/code_infer.buggy \
    --inference_output_file=./data/code_infer.correct
