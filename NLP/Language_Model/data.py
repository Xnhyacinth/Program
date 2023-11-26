'''
Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
Author: Xnhyacinth, Xnhyacinth@qq.com
Date: 2023-11-20 15:47:51
'''

import collections
import os
import sys
import utils
import numpy as np

from collections import defaultdict
import jieba
import torch
# EOS = "</eos>"


def tokenize(text):
    return list(jieba.cut(text))


def build_vocab(train_data, test_data):
    """
    构建词典,用于存储所有的词汇
    :param train_data:
    :param test_data:
    :return:
    """
    w2i = defaultdict(lambda: len(w2i))
    S = w2i["<s>"]
    UNK = w2i["<unk>"]

    def read_dataset(filename):
        with open(filename, "r") as f:
            for line in f:
                words = tokenize(line.strip())
                yield [w2i[x] for x in words]

    # Read in the data
    train = list(read_dataset(train_data))
    w2i = defaultdict(lambda: UNK, w2i)
    vocab_size = len(w2i)
    test = list(read_dataset(test_data))
    i2w = {v: k for k, v in w2i.items()}

    return w2i, i2w, vocab_size


def file_to_ids(src_file, src_vocab):
    """
    将文章单词序列转化成词典id序列
    :param src_file:
    :param src_vocab:
    :return:
    """
    src_data = []
    with open(src_file, "r") as f_src:
        for line in f_src.readlines():
            words = tokenize(line.strip())
            ids = [src_vocab[w] for w in words if w in src_vocab]
            src_data += ids + [0]
    return src_data


def load_data(file_name, vocab_dict):
    """
    读取文件,返回 id 形式的大数组
    :param file_name:
    :param vocab_dict:
    :return:
    """
    file_ids = file_to_ids(file_name, vocab_dict)
    return file_ids


def get_data_iter(raw_data, batch_size, num_steps):
    """
    获取训练数据,对于语言模型来说,通常是读取n个词,然后预测下一个可能出现的词,
    因为RNN网路的结构能够记住以往的信息,所以可以简化为每读取一个词,预测下一个词
    :param raw_data: 原始数据,一个大数组
    :param batch_size: batch的数量
    :param num_steps: 每次读取多少个固定数量的词,这里相当于控制RNN处理的序列长度,也即是每个样本有多少次预测
    :return:
    """
    data_len = len(raw_data)
    raw_data = np.asarray(raw_data, dtype="int64")

    batch_len = data_len // batch_size

    # 将原有的大数组变成二维数组,第一维是batch的数量,第二维是每个bathc里数据的长度
    data = raw_data[0:batch_size * batch_len].reshape((batch_size, batch_len))

    epoch_size = (batch_len - 1) // num_steps   # 保证最后一个词可以作为标签被预测
    
    return batch_len, get_iter(epoch_size, data, num_steps, batch_size)


def get_iter(epoch_size, data, num_steps, batch_size):
    for i in range(epoch_size):
        x = np.copy(data[:, i * num_steps:(i + 1) * num_steps])
        y = np.copy(data[:, i * num_steps + 1:(i + 1) * num_steps + 1])
        # 此时x,y的大小是 [batch_size, num_steps]

        x = x.reshape((num_steps, batch_size))
        y = y.reshape((-1, 1)).squeeze()
        yield (torch.tensor(x), torch.tensor(y))


# def getadd(x):
#     for i in range(x):
#         yield i
        

# for j in range(3):
#     a = getadd(5)
#     for i in a:
#         print(i)