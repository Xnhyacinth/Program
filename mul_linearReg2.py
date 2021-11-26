#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/10/11 21:43

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
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
        train_test_split(arr2.iloc[:, [0, 1, 2, 3, 4, 5, 7, 8]], arr2.iloc[:, 6], test_size=0.2)

    return x_train, x_test, y_train, y_test


def cal_model(x_train, y_train):
    model = LinearRegression()
    model.fit(x_train, y_train)
    a = model.intercept_  # 截距
    b = model.coef_  # 回归系数
    print("最佳拟合线:截距", a, "\n回归系数：", b)
    return a, b


def cal_reg(x_train, y_train):
    x_train['b'] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    x = np.array(x_train)
    y = np.array(y_train)

    # print(x)
    # print(y)
    xTx = x.T @ x
    if np.linalg.det(xTx) == 0.0:
        print("矩阵为奇异矩阵,不能求逆")
        return
    w = np.linalg.inv(xTx) @ x.T @ y
    return w


def cal_odd(x_test, y_test, w):
    x_test['b'] = [1.0, 1.0, 1.0, 1.0]
    x = np.array(x_test)
    y = np.array(y_test)
    a = []
    m = 0
    for i in range(len(x_test)):
        if w @ x[i].T >= 0 and y[i] == 0:
            m = m + 1
        if w @ x[i].T < 0 and y[i] == 1:
            m = m + 1
        a.append(w @ x[i].T)
    print("对数几率：", a)
    return m


def main():
    x_train, x_test, y_train, y_test = load_data()
    w = cal_reg(x_train, y_train)  # 计算w*矩阵
    print("w*矩阵为：", w)
    err = cal_odd(x_test, y_test, w)  # 计算误差
    print("y_test:", np.array(y_test))
    print("错误率：", err / len(y_test))


if __name__ == '__main__':
    main()
