'''
Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
Author: Xnhyacinth, Xnhyacinth@qq.com
Date: 2023-11-20 15:48:40
'''
import os
import sys
import logging

lm_logger = None


def init_log_config(args):
    """
    初始化日志相关配置
    :return:
    """
    global lm_logger
    lm_logger = logging.getLogger()
    lm_logger.setLevel(logging.INFO)
    log_path = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_name = os.path.join(log_path, f'{args.model}_layers{args.nlayers}_train_{args.batch_size}.log')
    sh = logging.StreamHandler()
    fh = logging.FileHandler(log_name, mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - [%(process)d] [line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    lm_logger.addHandler(sh)
    lm_logger.addHandler(fh)
    return lm_logger
    

def check_cuda(use_cuda, err="You can not set use_cuda = True in the model because you are using paddlepaddle-cpu.\n \
    Please: 1. Install paddlepaddle-gpu to run your models on GPU or 2. Set use_cuda = False to run models on CPU."
               ):
    """
    检查当前 paddle 是否支持 GPU
    :param use_cuda:
    :param err:
    :return:
    """
    try:
        if use_cuda == True:
            lm_logger.error(err)
            sys.exit(1)
    except Exception as e:
        lm_logger.error("Exception {}".format(e))


# init_log_config()
