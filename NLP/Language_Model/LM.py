'''
Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
Author: Xnhyacinth, Xnhyacinth@qq.com
Date: 2023-11-19 13:46:13
'''
import argparse
import torch
import numpy as np
import torch.nn as nn
from collections import defaultdict
import jieba
import math
import time
import utils
import data
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
from torch.nn import TransformerEncoder, TransformerEncoderLayer
from torch import nn, Tensor


class RNN_LM(nn.Module):

    def __init__(self,
                 vocab_size,
                 embedding_dim,
                 hidden_dim,
                 dropout,
                 num_layers=2):
        super(RNN_LM, self).__init__()
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.RNN(embedding_dim,
                          hidden_dim,
                          num_layers,
                          batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, input):
        embedded = self.embedding(input)
        output, _ = self.rnn(embedded)
        logits = self.fc(self.dropout(output))
        return logits.view(-1, self.vocab_size)


class LSTM_LM(nn.Module):

    def __init__(self,
                 vocab_size,
                 embedding_dim,
                 hidden_dim,
                 dropout,
                 num_layers=2):
        super(LSTM_LM, self).__init__()
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim,
                            hidden_dim,
                            num_layers,
                            batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, input):
        embedded = self.embedding(input)
        output, _ = self.lstm(embedded)
        logits = self.fc(self.dropout(output))
        return logits.view(-1, self.vocab_size)


class PositionalEncoding(nn.Module):

    def __init__(self,
                 d_model: int,
                 dropout: float = 0.1,
                 max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x: Tensor, shape [seq_len, batch_size, embedding_dim]
        """
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)


class Transformer_LM(nn.Module):

    def __init__(self,
                 ntoken: int,
                 d_model: int,
                 d_hid: int,
                 dropout: float = 0.5,
                 nhead: int = 2,
                 nlayers: int = 2):
        super().__init__()
        self.model_type = 'Transformer'
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = TransformerEncoderLayer(d_model, nhead, d_hid,
                                                 dropout)
        self.transformer_encoder = TransformerEncoder(encoder_layers, nlayers)
        self.encoder = nn.Embedding(ntoken, d_model)
        self.d_model = d_model
        self.decoder = nn.Linear(d_model, ntoken)
        self.n_token = ntoken

        self.init_weights()

    def init_weights(self) -> None:
        initrange = 0.1
        self.encoder.weight.data.uniform_(-initrange, initrange)
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, src: Tensor, src_mask: Tensor) -> Tensor:
        """
        Args:
            src: Tensor, shape [seq_len, batch_size]
            src_mask: Tensor, shape [seq_len, seq_len]

        Returns:
            output Tensor of shape [seq_len, batch_size, ntoken]
        """
        src = self.encoder(src) * math.sqrt(self.d_model)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src, src_mask)
        output = self.decoder(output)
        return output.view(-1, self.n_token)


def generate_square_subsequent_mask(sz: int) -> Tensor:
    """生成一个负无穷大的上三角矩阵，对角线上元素为 0。"""
    return torch.triu(torch.ones(sz, sz) * float('-inf'), diagonal=1)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def main():
    """ 
    Main func.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="rnn")
    parser.add_argument("--train_data", type=str, default="data/train.txt")
    parser.add_argument("--test_data", type=str, default="data/test.txt")
    parser.add_argument("--seed", type=int, default=29)
    parser.add_argument("--epoch", type=int, default=5)
    parser.add_argument("--num_steps", type=int, default=128)
    parser.add_argument("--nhead", type=int, default=2)
    parser.add_argument("--nlayers", type=int, default=2)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--embedding_dim", type=int, default=256)
    parser.add_argument("--hidden_dim", type=int, default=512)
    parser.add_argument("--dropout", type=float, default=0.1)
    args = parser.parse_args()

    # seed the random number generators
    seed = int(args.seed)
    logger = utils.init_log_config(args)
    torch.manual_seed(seed)
    USE_CUDA = torch.cuda.is_available()
    if USE_CUDA:
        torch.cuda.manual_seed(seed)
    np.random.seed(seed)

    logger.info("begin to load data")
    w2i, i2w, vocab_size = data.build_vocab(args.train_data, args.test_data)
    logger.info("vocab word num {}".format(vocab_size))
    # 把词典保存下来
    with open('vocab.txt', 'w') as f:
        for (k, v) in w2i.items():
            f.write("{}\t{}\n".format(k, v))
    train_data = data.load_data(args.train_data, w2i)
    test_data = data.load_data(args.test_data, w2i)
    logger.info("finished load data")

    data_iter_size = args.batch_size

    if args.model == 'rnn':
        model = RNN_LM(vocab_size, args.embedding_dim,
                       args.hidden_dim, args.dropout, args.nlayers)
    elif args.model == 'lstm':
        model = LSTM_LM(vocab_size, args.embedding_dim,
                        args.hidden_dim, args.dropout, args.nlayers)
    elif args.model == 'attn':
        model = Transformer_LM(vocab_size, args.embedding_dim,
                               args.hidden_dim, args.dropout, args.nhead, args.nlayers)
    if USE_CUDA:
        model = model.cuda()
    # 打印模型大小
    logger.info(f'Model size: {count_parameters(model) / 10 ** 6}M parameters')
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    # Train
    logger.info("start training")
    total_time = 0.0
    src_mask = generate_square_subsequent_mask(args.num_steps).cuda()
    best_score = 100.0
    for epoch in range(args.epoch):
        batch_len, train_batches = data.get_data_iter(train_data,
                                                      data_iter_size,
                                                      args.num_steps)
        total_loss = 0.0
        epoch_start_time = time.time()
        l = 0
        model.train()
        for batch in tqdm(train_batches, desc='Length'):
            l += 1
            x, y = batch
            x = x.cuda()
            y = y.cuda()
            batch_size = x.size(0)
            if batch_size != args.num_steps:  # 仅在最后一批进行
                src_mask = src_mask[:batch_size, :batch_size]
            optimizer.zero_grad()
            if args.model == 'attn':
                output = model(x, src_mask)
            else:
                output = model(x)
            loss = criterion(output, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
            optimizer.step()
            total_loss += loss.item()

        epoch_time = time.time() - epoch_start_time
        total_time += epoch_time
        avg_loss = total_loss / l
        logger.info(
            "Train epoch:%2d | epoch Time: %4.2f | ppl: %6.4f | avg_loss: %6.4f"
            % (epoch + 1, epoch_time, math.exp(avg_loss), avg_loss))

        # eval
        test_loss = 0.0
        batch_len, test_batches = data.get_data_iter(test_data, data_iter_size,
                                                        args.num_steps)
        # 计算困惑度
        l = 0
        src_mask = generate_square_subsequent_mask(args.num_steps).cuda()
        model.eval()
        with torch.no_grad():
            for batch in tqdm(test_batches):
                l += 1
                x, y = batch
                x = x.cuda()
                y = y.cuda()
                batch_size = x.size(0)
                if batch_size != args.num_steps:  # 仅在最后一批进行
                    src_mask = src_mask[:batch_size, :batch_size]
                if args.model == 'attn':
                    output = model(x, src_mask)
                else:
                    output = model(x)
                # test_loss += batch_size * criterion(output, y).item()
                test_loss += criterion(output, y).item()
        test_loss /= l
        logger.info(
            f"Test epoch: {epoch + 1:2d} |  test loss: {test_loss:6.4f}  |  test ppl: {math.exp(test_loss):6.4f}")
        
        if test_loss < best_score:
            best_score = test_loss
            torch.save(model.state_dict(), f'models/{args.model}_{args.nlayers}.pt')
            logger.info("save model")


if __name__ == '__main__':
    main()
