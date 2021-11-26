#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/10/30 16:02
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os

from numpy import shape, zeros, mat, exp
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

os.chdir("D:/桌面/ML/Assignment4")
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


class SVM:
    def __init__(self, max_iter=100, kernel=("linear", 0)):
        self.max_iter = max_iter
        self._kernel = kernel

    def init_args(self, features, labels):
        self.m, self.n = features.shape
        self.X = features
        self.Y = labels
        self.b = 0.0

        # 将Ei保存在一个列表里
        self.alpha = np.ones(self.m)
        self.E = [self._E(i) for i in range(self.m)]
        # 松弛变量
        self.C = 1.0

    def cal_k(self, a):  # x:数据特征  a: 某行数据   k_p：svm类别
        k = mat(zeros((self.m, 1)))
        if self._kernel[0] == "linear":  # 线性
            k = self.X @ a.T
        elif self._kernel[0] == 'rbf':  # 高斯
            for j in range(self.m):
                delta = self.X[j, :] - a
                k[j] = delta @ delta.T
            k = exp(-k / (2 * self._kernel[1] ** 2))
        else:
            print("error")
            return
        return k

    # 核函数
    def kernel(self, x1, x2):
        if self._kernel[0] == "linear":  # 线性核函数
            return sum([x1[k] * x2[k] for k in range(self.n)])
            # return x1 @ x2.T
        elif self._kernel[0] == "rbf":  # 高斯核函数
            # return (sum([x1[k] * x2[k] for k in range(self.n)]) + 1) ** 2
            delta = x1 - x2
            return exp(-(delta @ delta.T) / (2 * self._kernel[1] ** 2))

        return 0

    # g(x)为预测，输入xi(X[i])
    def _g(self, i):
        r = self.b
        for j in range(self.m):
            r += self.alpha[j] * self.Y[j] * self.kernel(self.X[i], self.X[j])
        return r

    # KKT条件
    def _KKT(self, i):
        y_g = self._g(i) * self.Y[i]
        if self.alpha[i] == 0:
            return y_g >= 1
        elif 0 < self.alpha[i] < self.C:
            return y_g == 1
        else:
            return y_g <= 1

    # E(x)为g(x)对输入x的预测值和真实输出y的差
    def _E(self, i):
        return self._g(i) - self.Y[i]

    def _init_alpha(self):
        # 外层循环首先遍历所有满足0<a<C的样本点，检验是否满足KKT
        index_list = [i for i in range(self.m) if 0 < self.alpha[i] < self.C]
        # 否则遍历整个训练集
        # 选择出不满足KKT点的样本
        non_satisfy_list = [i for i in range(self.m) if i not in index_list]
        index_list.extend(non_satisfy_list)

        for i in index_list:
            if self._KKT(i):
                continue
            E1 = self.E[i]
            # 如果E1是+，选择最小的；如果E2是负的，选择最大的
            if E1 >= 0:
                j = min(range(self.m), key=lambda x: self.E[x])
            else:
                j = max(range(self.m), key=lambda x: self.E[x])
            return i, j

    def _compare(self, _alpha, L, H):
        if _alpha > H:
            return H
        elif _alpha < L:
            return L
        else:
            return _alpha

    def smo(self, features, labels):
        self.init_args(features, labels)

        for t in range(self.max_iter):
            i1, i2 = self._init_alpha()

            if self.Y[i1] == self.Y[i2]:
                L = max(0, self.alpha[i1] + self.alpha[i2] - self.C)
                H = min(self.C, self.alpha[i1] + self.alpha[i2])
            else:
                L = max(0, self.alpha[i2] - self.alpha[i1])
                H = min(self.C, self.C + self.alpha[i2] - self.alpha[i1])
            E1 = self.E[i1]
            E2 = self.E[i2]

            # eta=K11+K22-2K12
            eta = self.kernel(self.X[i1], self.X[i1]) + self.kernel(self.X[i2], self.X[i2]) - 2 * self.kernel(
                self.X[i1], self.X[i2])
            if eta <= 0:
                continue
            alpha2_new_unc = self.alpha[i2] + self.Y[i2] * (E1 - E2) / eta
            alpha2_new = self._compare(alpha2_new_unc, L, H)
            alpha1_new = self.alpha[i1] + self.Y[i1] * self.Y[i2] * (self.alpha[i2] - alpha2_new)

            b1_new = - E1 - self.Y[i1] * self.kernel(self.X[i1], self.X[i1]) * (
                    alpha1_new - self.alpha[i1]) - self.Y[i2] * self.kernel(self.X[i2], self.X[i1]) * (
                             alpha2_new - self.alpha[i2]) + self.b

            b2_new = - E2 - self.Y[i1] * self.kernel(self.X[i1], self.X[i2]) * (
                    alpha1_new - self.alpha[i1]) - self.Y[i2] * self.kernel(self.X[i2], self.X[i2]) * (
                             alpha2_new - self.alpha[i2]) + self.b

            if 0 < alpha1_new < self.C:
                b_new = b1_new
            elif 0 < alpha2_new < self.C:
                b_new = b2_new
            else:
                # 选择中点
                b_new = (b1_new + b2_new) / 2

                # 更新参数
            self.alpha[i1] = alpha1_new
            self.alpha[i2] = alpha2_new
            self.b = b_new

            self.E[i1] = self._E(i1)
            self.E[i2] = self._E(i2)
            return "train done!"

    def predict(self, data):
        r = self.b
        for i in range(self.m):
            r += self.alpha[i] * self.Y[i] * self.kernel(data, self.X[i])

        return 1 if r > 0 else -1

    def score(self, X_test, y_test):
        right_count = 0
        for i in range(len(X_test)):
            result = self.predict(X_test[i])
            if result == y_test[i]:
                right_count += 1
        return right_count / len(X_test)

    def _weight(self):
        # linear model
        yx = self.Y.reshape(-1, 1) * self.X
        self.w = np.dot(yx.T, self.alpha)
        return self.w


# 数据特征可视化
# def visual(data, class_method):
#     colormap = dict(zip(data['好瓜'].value_counts().index.tolist(), ['blue', 'green']))  # 坏瓜好瓜颜色
#     die = data.groupby('好瓜')
#     plt.figure()
#     for species, klass in die:
#         plt.scatter(klass['密度'], klass['含糖率'],
#                     color=colormap[species],
#                     label=species
#                     )
#     for name, model in class_method.items():
#         sv = model.support_vectors_
#         plt.plot(sv[:, 0], sv[:, 1], label=str(name) + '_supported_vector')
#     plt.legend(frameon=True, title='好瓜', loc="upper left")
#     plt.title('SVC')
#     plt.show()


def main():
    data = load_data("watermelon_3a.csv")
    x_train, x_test, y_train, y_test = Data_Partition(data)

    s = SVM(max_iter=200)
    s.smo(x_train, y_train)
    print('线性核的准确率为：{}'.format(s.score(x_test, y_test)))

    s2 = SVM(max_iter=200, kernel=('rbf', 3))
    s2.smo(x_train, y_train)
    print('高斯核的准确率为：{}'.format(s2.score(x_test, y_test)))

    # 线性核处理
    linear_svm = svm.LinearSVC(C=0.5, class_weight='balanced')
    linear_svm.fit(x_train, y_train)
    y_pred = linear_svm.predict(x_test)
    print('线性核_model的准确率为：{}'.format(accuracy_score(y_pred=y_pred, y_true=y_test)))

    # 高斯核处理
    gauss_svm = svm.SVC(C=0.5, kernel='rbf', class_weight='balanced')
    gauss_svm.fit(x_train, y_train)
    y_pred2 = gauss_svm.predict(x_test)
    print('高斯核_model的准确率: %s' % (accuracy_score(y_pred=y_pred2, y_true=y_test)))


if __name__ == '__main__':
    main()
