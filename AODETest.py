#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/11/25 14:26

import os

import numpy as np
import pandas as pd

os.chdir("D:/桌面/D/ML/Assignment6/2")


def AODE(x, X, Y, laplace=True, mmin=3):
    # 平均独依赖贝叶斯分类器
    # x 待预测样本
    # X 训练样本特征值
    # Y 训练样本标记
    # laplace 是否采用“拉普拉斯修正”，默认为真
    # mmin 作为父属性最少需要的样本数

    C = list(set(Y))  # 所有可能标记
    N = [len(set(x[i] for x in X)) for i in range(len(x))]  # 各个属性的可能取值数
    p = []  # 存储概率值

    # AODE
    for c in C:
        #  获取类先验概率p(c)
        Xc = [X[i] for i in range(len(Y)) if Y[i] == c]  # c类样本子集
        pc = (len(Xc) + laplace) / (len(X) + laplace * len(C))  # 类先验概率
        # --------求取父属性概率P(c,xi)--------
        p_cxi = np.zeros(len(x))  # 将计算结果存储在一维向量p_cxi中
        for i in range(len(x)):
            if type(x[i]) != type(X[0][i]):
                print('样本数据第%d个特征的数据类型与训练样本数据类型不符,无法预测!' % (i + 1))
                return None
            if type(x[i]) == str:
                # 若为字符型特征，按离散取值处理
                Xci = [1 for xc in Xc if xc[i] == x[i]]  # c类子集中第i个特征与待预测样本一样的子集
                p_cxi[i] = (len(Xci) + laplace) / (len(X) + laplace * len(C) * N[i])
            elif type(x[i]) == np.int64:
                Xci = [1 for xc in Xc if xc[i] == x[i]]  # c类子集中第i个特征与待预测样本一样的子集
                p_cxi[i] = (len(Xci) + laplace) / (len(X) + laplace * len(C) * N[i])
            elif type(x[i]) == np.float64:
                # 若为浮点型特征，按高斯分布处理
                Xci = [xc[i] for xc in Xc]
                u = np.mean(Xci)
                sigma = np.std(Xci, ddof=1)
                p_cxi[i] = pc / np.sqrt(2 * np.pi) / \
                           sigma * np.exp(-(x[i] - u) ** 2 / 2 / sigma ** 2)
            else:
                print('目前只能处理字符型,整数和浮点型数据，对于其他类型有待扩展相应功能。')
                return None
        print(''.join(['p(c=%d,xi)=' % c] + ['%.3f' % p_cxi[i] + (lambda i: ';' if i == len(x) - 1 else ',')(i) for i in
                                             range(len(x))]))

        # --------求取父属性条件依赖概率P(xj|c,xi)--------
        p_cxixj = np.eye(len(x))  # 将计算结果存储在二维向量p_cxixj中
        for i in range(len(x)):
            for j in range(len(x)):
                if i == j:
                    continue
                # ------根据xi和xj是离散还是连续属性分为多种情况-----
                if type(x[i]) == str and type(x[j]) == str:
                    Xci = [xc for xc in Xc if xc[i] == x[i]]
                    Xcij = [1 for xci in Xci if xci[j] == x[j]]
                    p_cxixj[i, j] = (len(Xcij) + laplace) / (len(Xci) + laplace * N[j])
                if type(x[i]) == str and type(x[j]) == float:
                    Xci = [xc for xc in Xc if xc[i] == x[i]]
                    Xcij = [xci[j] for xci in Xci]
                    # 若子集Dc,xi数目少于2个，则无法用于估计正态分布参数，
                    # 则将其设为标准正态分布
                    if len(Xci) == 0:
                        u = 0
                    else:
                        u = np.mean(Xcij)
                    if len(Xci) < 2:
                        sigma = 1
                    else:
                        sigma = np.std(Xcij, ddof=1)
                    p_cxixj[i, j] = 1 / np.sqrt(2 * np.pi) / \
                                    sigma * np.exp(-(x[j] - u) ** 2 / 2 / sigma ** 2)
                if type(x[i]) == float and type(x[j]) == str:
                    Xcj = [xc for xc in Xc if xc[j] == x[j]]
                    Xcji = [xcj[i] for xcj in Xcj]
                    if len(Xcj) == 0:
                        u = 0
                    else:
                        u = np.mean(Xcji)
                    if len(Xcj) < 2:
                        sigma = 1
                    else:
                        sigma = np.std(Xcji, ddof=1)
                    p_cxixj[i, j] = 1 / np.sqrt(2 * np.pi) / sigma * np.exp(-(x[i] - u) ** 2 / 2 / sigma ** 2) * p_cxi[
                        j] / p_cxi[i]
                if type(x[i]) == float and type(x[j]) == float:
                    Xcij = np.array([[xc[i], xc[j]] for xc in Xc])
                    u = Xcij.mean(axis=0).reshape(1, -1)
                    sigma2 = (Xcij - u).T.dot(Xcij - u) / (Xcij.shape[0] - 1)
                    p_cxixj[i, j] = 1 / 2 * np.pi / np.sqrt(np.linalg.det(sigma2)) \
                                    * np.exp(-0.5 * ([x[i], x[j]] - u).
                                             dot(np.linalg.inv(sigma2)).
                                             dot(([x[i], x[j]] - u).T)) * pc / p_cxi[i]
        print(''.join([(lambda j: 'p(xj|c=%d,x%d)=' % (c, i + 1) if j == 0 else '')(j)
                       + '%.3f' % p_cxixj[i][j]
                       + (lambda i: ';\n' if i == len(x) - 1 else ',')(j)
                       for i in range(len(x)) for j in range(len(x))]))
        # --------求计算总的概率∑iP(c,xi)*∏jP(xj|c,xi)--------
        sump = 0
        for i in range(len(x)):
            if len([1 for xi in X if xi[1] == x[1]]) >= mmin:
                sump += p_cxi[i] * p_cxixj[i, :].prod()
        print('P(c=%d,x) ∝ %.3E\n' % (c, sump))
        p.append(sump)
        # --------做预测--------
    predict = C[p.index(max(p))]
    print('===============预测结果：%s类===============' % predict)
    return predict


def main():
    test_data = pd.read_csv('./data_format1/test_format1.csv')
    train_data = pd.read_csv('./data_format1/train_format1.csv')

    user_info = np.array(pd.read_csv('./data_format1/user_info_format1.csv'))
    user_log = np.array(pd.read_csv('./data_format1/user_log_format1.csv'))
    # print(train_data.info)
    # print(test_data.info)

    labels = train_data['label']
    train_data = train_data.drop(['label'],axis=1)
    train_data = np.array(train_data)
    test_data = np.array(test_data)
    AODE(train_data[2], train_data, labels)
    print(labels[2])


if __name__ == '__main__':
    main()
