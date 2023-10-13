#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/4/24 17:42
import datetime
import json
from torch.utils.data import DataLoader
from evaluate import evaluate_fn, get_logits_and_trues_and_loss
from data import *
from dataset import FraudDataset


def main():
    if not os.path.isdir("./result"):
        os.mkdir("./result")
    # load model
    #model = HybridAttentionModel()
    #model.load_state_dict(torch.load('local_model'))
    model = torch.load('local_model')
    model.to('cuda')

    # load data
    x, y = GetDataSet('data/eval.csv')

    dataset = FraudDataset(x, y)
    valid_loader = DataLoader(dataset=dataset, batch_size=100, shuffle=True)

    logits, y_eval, _ = get_logits_and_trues_and_loss(model, valid_loader, loss_fn=None, device='cuda')
    probs = torch.softmax(torch.tensor(logits), dim=1).numpy()
    fraud_prob = probs[:, 1]

    # 将预测结果保存到文件
    json_predict = {}
    for i in range(len(fraud_prob)):
        json_predict["id"] = i+1
        json_predict["fraud"] = "{}".format("是" if fraud_prob[i] > 0.5 else "否")
        json_predict["date"] = "{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        jd = json.dumps(json_predict, ensure_ascii=False)
        with open('result/predict.json', 'a', encoding='utf-8') as f:
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
