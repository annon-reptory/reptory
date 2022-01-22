rm -rf ./code_model/

python -m nmt.nmt \
    --src=buggy --tgt=correct \
    --vocab_prefix=./data/Vocab/vocab  \
    --train_prefix=./data/TrainData/train \
    --dev_prefix=./data/DevData/dev  \
    --test_prefix=./data/TestData/test \
    --src_max_len=665 \
    --tgt_max_len=665 \
    --out_dir=./code_model \
    --optimizer=adam \
    --learning_rate=0.001 \
    --decay_scheme=luong5 \
    --max_gradient_norm=4 \
    --batch_size=64 \
    --num_train_steps=50 \
    --steps_per_stats=100 \
    --num_layers=2 \
    --num_units=128 \
    --dropout=0.2 \
    --metrics=bleu
