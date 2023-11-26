'''
Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
Author: Xnhyacinth, Xnhyacinth@qq.com
Date: 2023-11-19 13:24:11
'''
from collections import defaultdict
import math
import time
import random
import os
import sys
import jieba
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import argparse

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

# Feed-forward Neural Network Language Model
class FNN_LM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_hist, dropout):
        super(FNN_LM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.fnn = nn.Sequential(
            nn.Linear(num_hist*embedding_dim, hidden_dim), 
            nn.Tanh(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, vocab_size)
        )

    def forward(self, input):
        # 3D Tensor of size [batch_size x num_hist x emb_size]
        emb = self.embedding(input)
        # 2D Tensor of size [batch_size x (num_hist*emb_size)]
        feat = emb.view(emb.size(0), -1)
        # 2D Tensor of size [batch_size x nwords]
        output = self.fnn(feat)

        return output

parser = argparse.ArgumentParser()
parser.add_argument("--train_data", type=str, default="data/train.txt")
parser.add_argument("--test_data", type=str, default="data/test.txt")
parser.add_argument("--seed", type=int, default=29)
parser.add_argument("--N", type=int, default=2)
parser.add_argument("--embedding_dim", type=int, default=256)
parser.add_argument("--hidden_dim", type=int, default=512)
parser.add_argument("--dropout", type=float, default=0.1)
args = parser.parse_args()

# seed the random number generators
seed = int(args.seed)
torch.manual_seed(seed)
USE_CUDA = torch.cuda.is_available()
if USE_CUDA:
    torch.cuda.manual_seed(seed)
np.random.seed(seed)

N = args.N  # The length of the n-gram
embedding_dim  = args.embedding_dim   # The size of the embedding
hidden_dim  = args.hidden_dim  # The size of the hidden layer

# Functions to read in the corpus
#       unknown words, etc.
w2i = defaultdict(lambda: len(w2i))
S = w2i["<s>"]
UNK = w2i["<unk>"]

def tokenize(text):
    return list(jieba.cut(text))

def read_dataset(filename):
    with open(filename, "r") as f:
        for line in f:
          words = tokenize(line.strip())
          yield [w2i[x] for x in words]

# Read in the data
train = list(read_dataset("./data/train.txt"))
w2i = defaultdict(lambda: UNK, w2i)
i2w = {v: k for k, v in w2i.items()}
vocab_size = len(w2i)
print(vocab_size)
dev = list(read_dataset("./data/test.txt"))
# Initialize the model and the optimizer
model = FNN_LM(vocab_size=vocab_size, embedding_dim=embedding_dim,
               hidden_dim=hidden_dim, num_hist=N, dropout=args.dropout)
if USE_CUDA:
    model = model.cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)
print(f'Model size: {count_parameters(model) / 10 ** 6}M parameters')
# convert a (nested) list of int into a pytorch Variable

# def convert_to_variable(words):
#     var = Variable(torch.LongTensor(words))
#     if USE_CUDA:
#         var = var.cuda()

#     return var

# # A function to calculate scores for one value

# def calc_score_of_histories(words):
#     # This will change from a list of histories, to a pytorch Variable whose data type is LongTensor
#     words_var = convert_to_variable(words)
#     logits = model(words_var)
#     return logits

# # Calculate the loss value for the entire sentence

# def calc_sent_loss(sent):
#     # The initial history is equal to end of sentence symbols
#     hist = [S] * N
#     # Step through the sentence, including the end of sentence token
#     all_histories = []
#     all_targets = []
#     for next_word in sent + [S]:
#         all_histories.append(list(hist))
#         all_targets.append(next_word)
#         hist = hist[1:] + [next_word]

#     logits = calc_score_of_histories(all_histories)
#     loss = nn.functional.cross_entropy(
#         logits, convert_to_variable(all_targets), size_average=False)

#     return loss

# MAX_LEN = 100
# # Generate a sentence

# def generate_sent():
#     hist = [S] * N
#     sent = []
#     while True:
#         logits = calc_score_of_histories([hist])
#         prob = nn.functional.softmax(logits)
#         next_word = torch.multinomial(prob, num_samples=1).squeeze(1)
#         if next_word == S or len(sent) == MAX_LEN:
#             break
#         sent.append(next_word)
#         hist = hist[1:] + [next_word]
#     return sent


# last_dev = 1e20
# best_dev = 1e20

# for ITER in range(20):
#     # Perform training
#     random.shuffle(train)
#     # set the model to training mode
#     model.train()
#     train_words, train_loss = 0, 0.0
#     start = time.time()
#     for sent_id, sent in enumerate(train):
#         my_loss = calc_sent_loss(sent)
#         train_loss += my_loss.item()
#         train_words += len(sent)
#         optimizer.zero_grad()
#         my_loss.backward()
#         torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
#         optimizer.step()
#         if (sent_id+1) % 5000 == 0:
#             print("--finished %r sentences (word/sec=%.2f)" %
#                   (sent_id+1, train_words/(time.time()-start)))
#     print("iter %r: train loss/word=%.4f, ppl=%.4f (word/sec=%.2f)" % (ITER, train_loss /
#           train_words, math.exp(train_loss/train_words), train_words/(time.time()-start)))

#     # Evaluate on dev set
#     # set the model to evaluation mode
#     model.eval()
#     dev_words, dev_loss = 0, 0.0
#     start = time.time()
#     for sent_id, sent in enumerate(dev):
#         my_loss = calc_sent_loss(sent)
#         dev_loss += my_loss.item()
#         dev_words += len(sent)

#     # Keep track of the development accuracy and reduce the learning rate if it got worse
#     if last_dev < dev_loss:
#         optimizer.param_groups[0]['lr'] /= 2
#     last_dev = dev_loss

#     # Keep track of the best development accuracy, and save the model only if it's the best one
#     if best_dev > dev_loss:
#         torch.save(model, "models/fnn.pt")
#         best_dev = dev_loss

#     # Save the model
#     print("iter %r: dev loss/word=%.4f, ppl=%.4f (word/sec=%.2f)" % (ITER, dev_loss /
#           dev_words, math.exp(dev_loss/dev_words), dev_words/(time.time()-start)))

#     # Generate a few sentences
#     for _ in range(5):
#         sent = generate_sent()
#         print(" ".join([i2w[x.item()] for x in sent]))
