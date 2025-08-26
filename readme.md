# BERT-BiLSTM-CRF模型

### 输入数据格式请处理成BIO格式，如下：
```
父	B-n
言	B-nr
忠	I-nr
，	B-w
貌	B-n
魁	B-a
梧	I-a
，	B-w
事	B-v
母	B-n
以	B-p
孝	B-n
聞	B-v
，	B-w
補	B-v
萬	B-ns
年	I-ns
主	B-nx
簿	I-nx
。	B-w

```

### 运行的环境
```
python == 3.7.4
pytorch == 1.3.1 
pytorch-crf == 0.7.2  
pytorch-transformers == 1.2.0               
```

### 使用方法
```
BERT_BASE_DIR=bert-base-chinese
DATA_DIR=/raid/ypj/openSource/cluener_public/
OUTPUT_DIR=./model/clue_bilstm
export CUDA_VISIBLE_DEVICES=0

python sequenceLabelling.py \
    --model_name_or_path F:\pretrain models\SikuBERT \
    --do_train True \
    --do_eval True \
    --do_test True \
    --max_seq_length 256 \
    --train_file ./corpus/ancient_round1/ancient_round1_train_.conll \
    --eval_file ./corpus/ancient_round1/ancient_round1_dev_.conll  \
    --test_file ./corpus/ancient_round1/ancient_round1_test_.conll  \
    --train_batch_size 32 \
    --eval_batch_size 32 \
    --num_train_epochs 5 \
    --do_lower_case \
    --logging_steps 200 \
    --need_birnn True \
    --rnn_dim 256 \
    --clean True \
    --output_dir $OUTPUT_DIR
```
