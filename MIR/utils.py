'''
Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
Author: Xnhyacinth, Xnhyacinth@qq.com
Date: 2023-12-28 06:14:09
'''
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer
from tqdm import tqdm
from utils import *
import subprocess
import pandas as pd


def load_eval_dataset(query_path, label_path):
    with open(query_path, 'r') as f:
        data = f.readlines()
    # format: {qid, query}
    queries = {}
    for d in data:
        qid, query = d.split('\t')
        queries[qid] = query
    
    with open(label_path, 'r') as f:
        data = f.readlines()
    labels = {}
    for d in data:
        qid , _, pid , rank, score, sys_id = d.split(' ')
        labels[(qid, pid)] = int(rank)
    return queries, labels

def load_tsv(path):
    tsv_file = pd.read_csv(path, sep='\t', header=None)
    data = np.array(tsv_file)
    return data


def load_source(path):
    source = load_tsv(path)
    pairs = dict(zip(source[:, 0], source[:, 1]))
    return pairs


class Metric:
    def __init__(self):
        pass

    def get_ndcg(self, preds, pids, is_test=False):

        dtype = [('qid', int), ('pid', int), ('score', float)]
        preds = np.array(preds, dtype=dtype)
        preds = preds[np.argsort(preds, order=['qid', 'score'])]

        outputs = []
        current_qid = 0
        rank = 0
        for line in preds:  # 生成rank
            if current_qid != line[0]:
                rank = 1
                current_qid = line[0]
            outputs.append((line[0], line[1], rank, -line[2]))
            rank += 1

        # 调用trec_eval程序， 用subprocess读取cmd输出，提取其中的necg@10分数
        if not is_test:  # dev
            with open('dev_result.txt', 'w') as f:
                for line in outputs:
                    f.write(
                        f"{line[0]} 0 {pids[line[1]]} {line[2]} {line[3]} CIPZHAO\n")
                f.close()
            p = subprocess.Popen('./trec_eval -m ndcg_cut ./sample/val_2021.qrels.pass.final.txt ./dev_result.txt',
                                 shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:          # test
            with open('test_result.txt', 'w') as f:
                for line in outputs:
                    f.write(
                        f"{line[0]} 0 {pids[line[1]]} {line[2]} {line[3]} CIPZHAO\n")
                f.close()
            p = subprocess.Popen('./trec_eval -m ndcg_cut ./sample/test_2022.qrels.pass.withDupes.txt ./test_result.txt',
                                 shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        outputs = []
        # 读取cmd的输出
        for line in p.stdout.readlines():
            outputs.append(line.decode())
        # 进行一些字符串处理
        return float(outputs[1].strip().replace('ndcg_cut_10           \tall\t', ''))
