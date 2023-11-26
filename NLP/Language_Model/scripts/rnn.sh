###
 # Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
 # @Author: Xnhyacinth, Xnhyacinth@qq.com
 # @Date: 2023-11-20 07:32:45
### 
batch_size=32
model='rnn'
CUDA_VISIBLE_DEVICES=6 nohup python -u LM.py --batch_size ${batch_size} --epoch 10 --model ${model} > logs/${model}_bs${batch_size}.log 2>&1 &

# batch_size=32
# CUDA_VISIBLE_DEVICES=7 nohup python -u RNN_LM1.py --batch_size ${batch_size} --epoch 10 > logs/rnn_bs${batch_size}.log 2>&1 &