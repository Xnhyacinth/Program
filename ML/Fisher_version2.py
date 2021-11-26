#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/10/10 20:31

import numpy as np
from sklearn.datasets import load_iris  # 导入数据集
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def load_data():  # 共150条数据，训练120，测试30，2，8分进行模型训练
    iris = load_iris()  # 载入数据集
    x_train, x_test, y_train, y_test = \
        train_test_split(iris.data, iris.target, test_size=0.2)
    return x_train, x_test, y_train, y_test


def cal_data(x_train, y_train):
    iris1_train = []
    iris2_train = []
    iris3_train = []
    for i in range(0, len(x_train), 1):
        if y_train[i] == 0:
            iris1_train.append(x_train[i].tolist())
        elif y_train[i] == 1:
            iris2_train.append(x_train[i].tolist())
        elif y_train[i] == 2:
            iris3_train.append(x_train[i].tolist())

    # 计算类内均值
    m1 = np.mean(iris1_train, axis=0)
    m2 = np.mean(iris2_train, axis=0)
    m3 = np.mean(iris3_train, axis=0)

    # 计算类内离散度矩阵
    s1 = np.zeros((4, 4))
    s2 = np.zeros((4, 4))
    s3 = np.zeros((4, 4))
    for i in range(0, len(iris1_train), 1):
        a = np.array([iris1_train[i] - m1])
        s1 = s1 + a.T @ a
    for i in range(0, len(iris2_train), 1):
        a = np.array([iris2_train[i] - m2])
        s2 = s2 + a.T @ a
    for i in range(0, len(iris3_train), 1):
        a = np.array([iris3_train[i] - m3])
        s3 = s3 + a.T @ a

    # 计算总类内散度矩阵
    s12 = s1 + s2
    s13 = s1 + s3
    s23 = s2 + s3
    print("'setosa'和'versicolor'的总类内散度矩阵：\n", s12, "\n")
    print("'setosa'和'virginica'的总类内散度矩阵：\n", s13, "\n")
    print("'versicolor'和'virginica'的总类内散度矩阵：\n", s23, "\n")

    # 计算Sw的逆
    t12 = np.linalg.inv(s12)
    t13 = np.linalg.inv(s13)
    t23 = np.linalg.inv(s23)
    print(t12)

    # 求向量w*
    w12 = (t12 @ np.array([(m1 - m2)]).T).T
    w13 = (t13 @ np.array([(m1 - m3)]).T).T
    w23 = (t23 @ np.array([(m2 - m3)]).T).T

    # 阈值wi
    w1 = 0.5 * w12 @ (m1 + m2)
    w2 = 0.5 * w13 @ (m1 + m3)
    w3 = 0.5 * w23 @ (m2 + m3)

    return w12, w13, w23, w1, w2, w3, iris1_train, iris2_train, iris3_train


def cal_y(w12, w13, w23, w1, w2, w3, x_test, y_test):
    n1 = 0
    n2 = 0
    n3 = 0
    for i in range(0, len(x_test), 1):
        x = np.array([x_test[i]])
        m12 = w12 @ x.T - w1
        m13 = w13 @ x.T - w2
        m23 = w23 @ x.T - w3
        if m12 > 0 and m13 > 0:
            if y_test[i] == 0:
                n1 = n1 + 1
        elif m12 < 0 and m23 > 0:
            if y_test[i] == 1:
                n2 = n2 + 1
        elif m13 < 0 and m23 < 0:
            if y_test[i] == 2:
                n3 = n3 + 1
    return n1 + n2 + n3


def show_figure(iris1_train, iris2_train, iris3_train):  # 可视化
    # 花瓣与花萼的长度散点图
    plt.scatter(np.array(iris1_train)[:, 2], np.array(iris1_train)[:, 0], color='red', marker='o', label='setosa')
    plt.scatter(np.array(iris2_train)[:, 2], np.array(iris2_train)[:, 0], color='blue', marker='x', label='versicolor')
    plt.scatter(np.array(iris3_train)[:, 2], np.array(iris3_train)[:, 0], color='green', label='virginica')
    plt.xlabel('petal length')
    plt.ylabel('sepal length')
    plt.title("花瓣与花萼长度的散点图")
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend(loc='upper left')
    plt.show()

    # 花瓣与花萼的宽度度散点图
    plt.scatter(np.array(iris1_train)[:, 3], np.array(iris1_train)[:, 1], color='red', marker='o', label='setosa')
    plt.scatter(np.array(iris2_train)[:, 3], np.array(iris2_train)[:, 1], color='blue', marker='x', label='versicolor')
    plt.scatter(np.array(iris3_train)[:, 3], np.array(iris3_train)[:, 1], color='green', label='virginica')
    plt.xlabel('petal width')
    plt.ylabel('sepal width')
    plt.title("花瓣与花萼宽度的散点图")
    plt.legend(loc='upper left')
    plt.show()


def main():
    x_train, x_test, y_train, y_test = load_data()
    w12, w13, w23, w1, w2, w3, iris1_train, iris2_train, iris3_train = cal_data(x_train, y_train)
    num = cal_y(w12, w13, w23, w1, w2, w3, x_test, y_test)
    print("正确率:", num / len(x_test) * 100, "%")
    show_figure(iris1_train, iris2_train, iris3_train)


if __name__ == '__main__':
    main()
