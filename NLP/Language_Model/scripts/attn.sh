###
 # Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
 # @Author: Xnhyacinth, Xnhyacinth@qq.com
 # @Date: 2023-11-20 07:32:45
### 
batch_size=32
# CUDA_VISIBLE_DEVICES=6 nohup python -u LM.py --batch_size ${batch_size} --epoch 10 --model attn > logs/attn_bs${batch_size}.log 2>&1 &

# batch_size=32
# CUDA_VISIBLE_DEVICES=7 nohup python -u RNN_LM1.py --batch_size ${batch_size} --epoch 10 > logs/rnn_bs${batch_size}.log 2>&1 &

# attn

for model in rnn attn lstm
    do
        for layers in 1 2 4
            do
                CUDA_VISIBLE_DEVICES=8 python -u LM.py --batch_size ${batch_size} --epoch 20 --model ${model} --nlayers ${layers}
            done
    done


# for model in rnn attn lstm
#     do
#         CUDA_VISIBLE_DEVICES=8 python -u LM.py --batch_size ${batch_size} --epoch 30 --model ${model} --nlayers 1
#     done