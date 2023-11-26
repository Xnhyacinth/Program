###
 # Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
 # @Author: Xnhyacinth, Xnhyacinth@qq.com
 # @Date: 2023-11-20 07:32:45
### 
CUDA_VISIBLE_DEVICES=8 nohup python -u FFN_LM.py --N 2 > logs_ffn/ffn_2_lr8e-5.log 2>&1 &