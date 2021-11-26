#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/10/11 21:44

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def load_data():  # 2，8分进行模型训练
    data = pd.read_csv("C:/Users/Xnhyacinth/Desktop/1.csv")  # 载入数据集
    data_arr = np.array(data.drop(columns=["编号"])).T
    arr1 = data_arr[0:6, :]
    attr = []
    for i in range(6):
        attr.append(list(set(arr1[i])))
    attr.append(["否", "是"])
    arr2 = np.append(arr1, [data_arr[-1]], axis=0)

    # 转换为0，1，2
    for i in range(arr2.shape[0]):
        for j in range(arr2.shape[1]):
            arr2[i][j] = attr[i].index(arr2[i][j])

    arr2 = np.append(arr2, [data_arr[-3], data_arr[-2]], axis=0).astype("float64").T
    # print(arr2)
    arr2 = pd.DataFrame(arr2)
    x_train, x_test, y_train, y_test = \
        train_test_split(arr2.iloc[:, 1:], arr2.iloc[:, 0], test_size=0.25)

    return x_train, x_test, y_train, y_test


def cal_data(x_train, y_train):
    train1 = []
    train2 = []
    train3 = []

    for i in range(0, len(x_train), 1):
        if y_train[i] == 0:
            train1.append(x_train[i].tolist())
        elif y_train[i] == 1:
            train2.append(x_train[i].tolist())
        elif y_train[i] == 2:
            train3.append(x_train[i].tolist())

    # 计算类内均值
    m1 = np.mean(train1, axis=0)
    m2 = np.mean(train2, axis=0)
    m3 = np.mean(train3, axis=0)
    # print(m1,m2,m3)

    # 计算类内离散度矩阵
    s1 = np.zeros((8, 8))
    s2 = np.zeros((8, 8))
    s3 = np.zeros((8, 8))
    for i in range(0, len(train1), 1):
        a = np.array([train1[i] - m1])
        s1 = s1 + a.T @ a
    for i in range(0, len(train2), 1):
        a = np.array([train2[i] - m2])
        s2 = s2 + a.T @ a
    for i in range(0, len(train3), 1):
        a = np.array([train3[i] - m3])
        s3 = s3 + a.T @ a

    # 计算总类内散度矩阵
    s12 = s1 + s2
    s13 = s1 + s3
    s23 = s2 + s3
    # print("'setosa'和'versicolor'的总类内散度矩阵：\n", s12, "\n")
    # print("'setosa'和'virginica'的总类内散度矩阵：\n", s13, "\n")
    # print("'versicolor'和'virginica'的总类内散度矩阵：\n", s23, "\n")

    # 计算Sw的逆
    t12 = np.linalg.inv(s12)
    t13 = np.linalg.inv(s13)
    t23 = np.linalg.inv(s23)

    # 求向量w*
    w12 = (t12 @ np.array([(m1 - m2)]).T).T
    w13 = (t13 @ np.array([(m1 - m3)]).T).T
    w23 = (t23 @ np.array([(m2 - m3)]).T).T

    # 阈值wi
    w1 = 0.5 * w12 @ (m1 + m2)
    w2 = 0.5 * w13 @ (m1 + m3)
    w3 = 0.5 * w23 @ (m2 + m3)

    return w12, w13, w23, w1, w2, w3, train1, train2, train3


def cal_y(w12, w13, w23, w1, w2, w3, x_test, y_test):
    n1 = 0
    n2 = 0
    n3 = 0
    y_predict = []
    for i in range(0, len(x_test), 1):
        x = np.array([x_test[i]])
        m12 = w12 @ x.T - w1
        m13 = w13 @ x.T - w2
        m23 = w23 @ x.T - w3

        if m12 > 0 and m13 > 0:
            y_predict.append(0)
            if y_test[i] == 0:
                n1 = n1 + 1
        elif m12 < 0 and m23 > 0:
            y_predict.append(1)
            if y_test[i] == 1:
                n2 = n2 + 1
        elif m13 < 0 and m23 < 0:
            y_predict.append(2)
            if y_test[i] == 2:
                n3 = n3 + 1
        if len(y_predict) == i:
            y_predict.append('unknown')
    return n1 + n2 + n3, y_predict


def main():
    x_train, x_test, y_train, y_test = load_data()
    y_train = np.array(y_train)
    x_train = np.array(x_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)

    w12, w13, w23, w1, w2, w3, train1, train2, train3 = cal_data(x_train, y_train)
    num, y_predict = cal_y(w12, w13, w23, w1, w2, w3, x_test, y_test)
    print("y_test:\n", y_test)
    print("y_predict:\n", y_predict)
    print("正确率:", num / len(x_test) * 100, "%")


if __name__ == '__main__':
    main()
