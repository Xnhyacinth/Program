#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/4/24 17:42
import json

import torch
from torch import nn
from torch.utils.data import DataLoader
from evaluate import evaluate_fn, get_logits_and_trues_and_loss
from metrics import metrics_report
from Hybrid_Attn import HybridAttentionModel
from radam import RAdam
from data import *
from dataset import FraudDataset


def main():
    if not os.path.isdir("./result"):
        os.mkdir("./result")
    # load model
    model = torch.load('global_model_0')

    # load data
    x, y = GetDataSet('data/eval.csv')

    dataset = FraudDataset(x, y)
    valid_loader = DataLoader(dataset=dataset, batch_size=100, shuffle=True)
    # 定义损失函数
    loss_func = nn.CrossEntropyLoss()

    # 定义优化函数
    opti = RAdam(model.parameters(), 0.001)
    # test
    valid_loss, tn, fp, fn, tp, precision, recall, f1Score = evaluate_fn(model, valid_loader,
                                                                         loss_func,
                                                                         'cpu', verbose=True)
    logits, y_eval, _ = get_logits_and_trues_and_loss(model, valid_loader, loss_fn=None, device='cpu')
    probs = torch.softmax(torch.tensor(logits), dim=1).numpy()
    fraud_prob = probs[:, 1]

    jd = {}
    jd['valid_loss'] = "{:.3}".format(valid_loss)
    jd['tn'] = "{}".format(tn)
    jd['fp'] = "{}".format(fp)
    jd['fn'] = "{}".format(fn)
    jd['tp'] = "{}".format(tp)
    jd['accuracy'] = "{:.3}".format(float((tn + tp) / (tn + tp + fn + fp)))
    jd['precision'] = "{:.3}".format(precision)
    jd['recall'] = "{:.3}".format(recall)
    jd['f1Score'] = "{:.3}".format(f1Score)
    jd = json.dumps(jd, ensure_ascii=False)

    with open(os.path.join("./", 'result/log_{}.json'.format("predict")), 'a') as f:
        f.write(jd + '\n')
        f.close()

    # 将预测结果保存到文件
    json_predict = {}
    for i in range(len(fraud_prob)):
        json_predict["{}".format(i)] = "是否窃电：{}".format("是" if fraud_prob[i] > 0.5 else "否")

    jd = json.dumps(json_predict, ensure_ascii=False)
    with open('result/predict.json', 'w', encoding='utf-8') as f:
        f.write(jd)
        f.close()

    # with open("log_test_model.txt", 'a', encoding='utf-8') as f:
    #     f.write(
    #         'ep: V: {:.3} -- F1: {:.3}  --TN:{:.3}   --FP:{:.3}   --FN:{:.3}   --TP:{:.3}   --P:{:.3}   --R:{:.3}'
    #         .format(valid_loss, f1Score, tn, fp, fn, tp, precision, recall) + '\n')
    # metrics_report(model, valid_loader, name="test_model", device='cpu')
    pass


if __name__ == '__main__':
    main()
