export CUDA_VISIBLE_DEVICES=0
python sequenceLabelling.py \
    --model_name_or_path $GEMINI_DATA_IN1/SikuBERT \
    --do_train True \
    --do_eval True \
    --do_test True \
    --max_seq_length 256 \
    --train_file $GEMINI_CODE/corpus/mo1/modern_round1_train_.conll \
    --eval_file $GEMINI_CODE/corpus/mo1/modern_round1_dev_.conll  \
    --test_file $GEMINI_CODE/corpus/mo1/modern_round1_test_.conll  \
    --train_batch_size 128 \
    --eval_batch_size 128 \
    --num_train_epochs 5 \
    --do_lower_case \
    --logging_steps 200 \
    --need_birnn True \
    --rnn_dim 256 \
    --clean True \
    --output_dir $GEMINI_CODE/24history-postag/modern_round1