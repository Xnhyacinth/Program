#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/11/16 16:07
import os
from sklearn import metrics
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, auc
import matplotlib.pyplot as plt

os.chdir("D:/桌面/D/ML/Assignment5")
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.close('all')


def load_data(path):
    data = pd.read_csv(path)
    data = data.drop(columns=["编号"])  # 删除编号列
    labels = data.columns.values.tolist()

    # 转换0/1
    for i in range(len(data.columns)):
        feature_list = data[labels[i]].unique().tolist()
        data[labels[i]] = data[labels[i]].apply(lambda feature: feature_list.index(feature))
    return data


def Data_Partition(data):  # 划分数据集
    labels = data.columns.values.tolist()
    y = data[labels[-1]].values
    data = data.drop(columns=labels[-1])
    x_train, x_test, y_train, y_test = \
        train_test_split(data, y, test_size=0.2)
    # x_train, x_test, y_train, y_test = \
    #     train_test_split(x_train, y_train, test_size=0.3)
    x_train = np.array(x_train)
    x_test = np.array(x_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    return x_train, x_test, y_train, y_test


def main():
    data = load_data("watermelon_3a.csv")
    x_train, x_test, y_train, y_test = Data_Partition(data)

    # AdaBoost Algorithm
    clf = AdaBoostClassifier()
    clf.fit(x_train, y_train)
    print("Adaboost Algorithm:")
    print("y:", y_test)
    print("y_predict:", clf.predict(x_test))
    y_probs = clf.predict_proba(x_test).T[1]  # 模型的预测得分

    # RF
    clf_rf = RandomForestClassifier()
    clf_rf.fit(x_train, y_train)
    print("RF Algorithm:")
    print("y:", y_test)
    print("y_predict:", clf_rf.predict(x_test))
    y_probs1 = clf.predict_proba(x_test).T[1]  # 模型的预测得分

    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_probs)
    fpr1, tpr1, thresholds = metrics.roc_curve(y_test, y_probs1)
    roc_auc = auc(fpr, tpr)  # auc为Roc曲线下的面积
    roc_auc1 = auc(fpr1, tpr1)  # auc为Roc曲线下的面积
    # 开始画ROC曲线
    plt.plot(fpr, tpr, 'b', label='AUC_Ada = %0.2f' % roc_auc)
    plt.plot([0, 1], [0, 1], 'r--')
    plt.plot(fpr1, tpr1, 'g', label='AUC_RF = %0.2f' % roc_auc1)
    plt.legend(loc='lower right')
    plt.xlim([-0.1, 1.1])
    plt.ylim([-0.1, 1.1])
    plt.xlabel('False Positive Rate')  # 横坐标是fpr
    plt.ylabel('True Positive Rate')  # 纵坐标是tpr
    plt.title('ROC')
    plt.show()


if __name__ == '__main__':
    main()
