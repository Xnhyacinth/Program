#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/5/19 9:05
import calendar
import datetime
import json
import os
import re
import time
from torch.utils.data import DataLoader
from werkzeug.utils import secure_filename
from dataset import *
from data import *
from evaluate import *
import torch
from flask import Flask, request, render_template_string, redirect, abort, url_for, send_file
from flask_cors import CORS
from pathlib import Path

UPLOAD_DIR: Path = Path(__file__).parent / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app = Flask(__name__)
CORS(app, supports_credentials=True)
if not os.path.isdir("uploads"):
    os.mkdir("uploads")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    filepath = "uploads/"
    for root, dirs, files in os.walk(filepath):
        filepath = filepath + files[-1]
    # load model
    model = torch.load('model')
    model.to(device)
    # load data
    user_id, user_area, user_court, x, y = getPredictData(filepath)
    print(user_id, user_area, user_court, x, y)

    dataset = FraudDataset(x, y)
    valid_loader = DataLoader(dataset=dataset, batch_size=100, shuffle=False)

    # 计算预测概率
    logits, y_eval, _ = get_logits_and_trues_and_loss(model, valid_loader, loss_fn=None, device=device)
    p = logits.argmax(1)
    probs = torch.softmax(torch.tensor(logits), dim=1).numpy()
    fraud_prob = probs[:, 1]
    print(y_eval)
    print(p)

    # 将预测结果保存到文件
    json_predict = []
    for i in range(len(fraud_prob)):
        jd = {"user_id": user_id[i], "user_area": user_area[i], "user_court": user_court[i],
              "date": datetime.datetime.now().strftime("%Y.%m.%d"),
              "result": "{}".format("窃电" if p[i] > 0.5 else "正常")}
        json_predict.append(jd)
    print(json_predict)
    return {
        'code': 200,
        'result': json_predict
    }


def uploadFile2IPFS(file_path):
    """ 上传文件到IPFS """
    # ipfs = IPFS()
    # ipfs.add(get_file_content(file_path))
    # return ipfs.get_hash()
    cmd = 'ipfs add ' + file_path
    result = os.popen(cmd)
    res = result.read()
    return res


def getLog(filepath):
    train_result = {}
    for root, dirs, files in os.walk(filepath):
        for file in files:
            pattern = r"(?<=_).*?(?=\.)"
            name = re.search(pattern, file).group()
            train_result[name] = {}
            with open(os.path.join(root, file), 'r') as f:
                if re.match(r'^client', name):
                    lines = f.readlines()
                    for line in lines[:-1]:
                        dic = json.loads(line)
                        if 'comm{}'.format(dic['communicate_index']) not in train_result[name]:
                            train_result[name]['comm{}'.format(dic['communicate_index'])] = {'train': {}, 'valid': {}}
                            train_result[name]['comm{}'.format(dic['communicate_index'])]['train'][
                                'epoch{}'.format(dic['epoch'])] = dic['train_loss']
                        elif 'epoch' in dic.keys():
                            train_result[name]['comm{}'.format(dic['communicate_index'])][
                                'epoch{}'.format(dic['epoch'])] = \
                                dic['train_loss']
                        else:
                            train_result[name]['comm{}'.format(dic['communicate_index'])]['valid'] = {
                                'valid_loss': dic['valid_loss'],
                                'tn': dic['tn'],
                                'fp': dic['fp'],
                                'fn': dic['fn'],
                                'tp': dic['tp'],
                                'precision': dic['precision'],
                                'recall': dic['recall'],
                                'f1Score': dic['f1Score'],
                                'accuracy': dic['accuracy'],
                                'AUC': dic['AUC'],
                                'MAP@100': dic['MAP@100'],
                                'MAP@200': dic['MAP@200'],
                            }
                        modelHash = uploadFile2IPFS('model/{}/local_model_{}'.format(name, dic['communicate_index']))
                        train_result[name]['comm{}'.format(dic['communicate_index'])]['modelHash'] = modelHash
                    l = json.loads(lines[-1])
                    train_result[name]['contribution'] = l['contribution']
                else:
                    lines = f.readlines()
                    for line in lines:
                        dic = json.loads(line)
                        modelHash = uploadFile2IPFS('model/{}/global_model_{}'.format(name, dic['communicate_index']))
                        train_result[name]['comm{}'.format(dic['communicate_index'])] = {
                            'valid_loss': dic['valid_loss'],
                            'tn': dic['tn'],
                            'fp': dic['fp'],
                            'fn': dic['fn'],
                            'tp': dic['tp'],
                            'precision': dic['precision'],
                            'recall': dic['recall'],
                            'f1Score': dic['f1Score'],
                            'accuracy': dic['accuracy'],
                            'AUC': dic['AUC'],
                            'MAP@100': dic['MAP@100'],
                            'MAP@200': dic['MAP@200'],
                            'modelHash': modelHash
                        }
                f.close()
    return train_result


@app.route('/start', methods=['GET', 'POST'])
def start():
    json_receive = request.get_json()
    lr = json_receive['lr']
    num_comm = json_receive['num_comm']
    isDP = json_receive['isDP']
    print(lr, num_comm, isDP)
    aggregation = json_receive['aggregation']
    optimizer = json_receive['optimizer']
    e = json_receive['e']
    if isDP:
        cmd = "python Server_Single.py" + " --lr " + str(lr) + " --num_comm " + str(num_comm) + " --aggregation " + str(
            aggregation) + " --optimizer " + str(optimizer) + " --e " + str(e)
        os.system(cmd)
    else:
        cmd = "python Server_Single.py" + " --learning_rate " + str(lr) + " --num_comm " + str(num_comm) \
              + " --aggregation " + str(aggregation) + " --optimizer " + str(optimizer)
        os.system(cmd)
    train_result = getLog('log')
    return {
        'code': 200,
        'train_result': train_result,
    }


def get_file_content(file_path):
    """ 读取图片 """
    with open(file_path, 'rb') as fp:
        return fp.read()


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    # print(request.headers)
    print(request.files)
    file = request.files.get('file')
    if file is None:
        # 表示没有发送文件
        return {
            'message': "文件上传失败"
        }
    file_name = file.filename  # print(file.filename)
    # 获取前缀（文件名称）print(os.path.splitext(file_name)[0])
    # 获取后缀（文件类型）print(os.path.splitext(file_name)[-1])
    suffix = os.path.splitext(file_name)[-1]  # 获取文件后缀（扩展名）
    basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
    nowTime = calendar.timegm(time.gmtime())  # 获取当前时间戳改文件名print(nowTime)
    upload_path = os.path.join(basePath, 'uploads',
                               str(nowTime))  # 改到upload目录下# 注意：没有的文件夹一定要先创建，不然会提示没有该路径print(upload_path)
    upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
    file.save(upload_path + str(nowTime) + suffix)  # 保存文件
    # http 路径
    url = 'http://localhost:3000/#/home/1' + str(nowTime) + str(nowTime) + suffix
    return {
        'code': 200,
        'messsge': "文件上传成功",
        'fileNameOld': file_name,
        'fileNameSave': str(nowTime) + str(nowTime) + suffix,
        'url': url
    }


@app.route('/download', methods=['POST', 'GET'])
def download():
    hash = request.args.get('hash')
    # cmd = "ipfs get " + hash
    # os.system(cmd)
    return send_file('predict.py', as_attachment=True)


@app.route('/111', methods=['POST', 'GET'])
def aaa():
    j = {"docType": "globalmodelObj", "TaskID": "Task1",
         "TaskDescription": {"Round": 20, "AggAlgorithm": "FedAvg", "OptimAlgorithm": "RAdam", "Lr": 0.001, "IfDP": "否",
                             "Epsilon": 0, "SimpleDescription": "基于多头注意力机制的窃电行为检测模型"}, "FinalLoss": 0.018,
         "FinalAccuracy": 0.9576, "FinalRecall": 0.905, "FinalF1": 0.932, "FinalConfusionMatrix": [3825, 51, 171, 191],
         "Participants": [{"CourtsID": "Courts1", "Contribution": 50.65}, {"CourtsID": "Courts2", "Contribution": 50},
                          {"CourtsID": "Courts3", "Contribution": 48.72}], "ModelInfo": [
            {"RoundNum": 1, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 2, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 3, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 4, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 5, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 6, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 7, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 8, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 9, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 10, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 11, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 12, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 13, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 14, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 15, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 16, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 17, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 18, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 19, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"},
            {"RoundNum": 20, "Loss": 0.284, "AUC": 0.905, "MAP100": 0.765, "MAP200": 0.658,
             "ConfusionMatrix": [3825, 51, 171, 191], "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"}]}
    return j


@app.route('/Courts2', methods=['POST', 'GET'])
def a():
    a = {"docType": "courtstrainingObj", "CourtsID": "C001", "district": "北京昌平区", "State": "在线",
         "Address": "北京市昌平区xx路xx号", "ConsumerCount": 5726, "Reputation": 50, "TrainingHistory": [
            {"TaskID": "Task1", "Contribution": 40.24, "LocalModel": [
                {"RoundNum": 1, "TrainLoss": 0.381, "ValidLoss": 0.302, "AUC": 0.703, "MAP100": 0.51, "MAP200": 0.56,
                 "ConfusionMatrix": [3875, 1, 361, 0], "IPFSHash": "ABC76F4ER78S946"},
                {"RoundNum": 2, "TrainLoss": 0.289, "ValidLoss": 0.298, "AUC": 0.7, "MAP100": 0.638, "MAP200": 0.657,
                 "ConfusionMatrix": [3875, 1, 361, 0], "IPFSHash": "ABC76F4ER78S946"}]}]}

    return a


@app.route('/Courts1', methods=['POST', 'GET'])
def b():
    b = {"docType": "courtstrainingObj", "CourtsID": "C001", "district": "北京昌平区", "State": "在线",
         "Address": "北京市昌平区xx路xx号", "ConsumerCount": 5726, "Reputation": 50, "TrainingHistory": [
            {"TaskID": "Task1", "Contribution": 40.24, "LocalModel": [
                {"RoundNum": 1, "TrainLoss": 0.381, "ValidLoss": 0.302, "AUC": 0.703, "MAP100": 0.51, "MAP200": 0.56,
                 "ConfusionMatrix": [3875, 1, 361, 0], "IPFSHash": "ABC76F4ER78S946"},
                {"RoundNum": 2, "TrainLoss": 0.289, "ValidLoss": 0.298, "AUC": 0.7, "MAP100": 0.638, "MAP200": 0.657,
                 "ConfusionMatrix": [3875, 1, 361, 0], "IPFSHash": "ABC76F4ER78S946"}]}]}
    return b


@app.route('/Courts3', methods=['POST', 'GET'])
def c():
    c = {"docType": "courtstrainingObj", "CourtsID": "C001", "district": "北京昌平区", "State": "在线",
         "Address": "北京市昌平区xx路xx号", "ConsumerCount": 5726, "Reputation": 50, "TrainingHistory": [
            {"TaskID": "Task1", "Contribution": 40.24, "LocalModel": [
                {"RoundNum": 1, "TrainLoss": 0.381, "ValidLoss": 0.302, "AUC": 0.703, "MAP100": 0.51, "MAP200": 0.56,
                 "ConfusionMatrix": [3875, 1, 361, 0], "IPFSHash": "ABC76F4ER78S946"},
                {"RoundNum": 2, "TrainLoss": 0.289, "ValidLoss": 0.298, "AUC": 0.7, "MAP100": 0.638, "MAP200": 0.657,
                 "ConfusionMatrix": [3875, 1, 361, 0], "IPFSHash": "ABC76F4ER78S946"}]}]}
    return c


if __name__ == "__main__":
    app.run(debug=True)
