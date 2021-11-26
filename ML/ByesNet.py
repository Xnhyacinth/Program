#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/11/24 17:43

import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

os.chdir("D:/桌面/D/ML/Assignment6")


def load_data(path):
    data = pd.read_csv(path)
    data = data.drop(columns=["编号"])  # 删除编号列
    labels = data.columns.values.tolist()

    # 转换0/1
    for i in range(len(data.columns)):
        feature_list = data[labels[i]].unique().tolist()
        data[labels[i]] = data[labels[i]].apply(lambda feature: feature_list.index(feature))

    return data, labels


def BNet(net):
    n = len(net)  # 节点数

    # 确定父节点
    parents = [list(np.where(net[i, :] == -1)[0] + 1) + list(np.where(net[:, i] == 1)[0] + 1) for i in range(n)]

    # 确定祖结点
    grands = []
    for i in range(n):
        grand = []
        # ---爷爷辈---
        for j in parents[i]:
            for k in parents[j - 1]:
                if k not in grand:
                    grand.append(k)
        # ---曾祖及以上辈---
        loop = True
        while loop:
            loop = False
            for j in grand:
                for k in parents[j - 1]:
                    if k not in grand:
                        grand.append(k)
                        loop = True
        grands.append(grand)

    # 判断环
    circle = [i + 1 for i in range(n) if i + 1 in grands[i]]

    return parents, grands, circle


def draw(net, name=None, title=''):
    # 绘制贝叶斯网络的变量关系图
    # net:array类型，网络结构，右上角元素ij表示各个连接边
    #     取值0表示无边，取值1表示Xi->Xj,取值-1表示Xi<-Xj
    # name:指定各个节点的名称，默认为None，用x1,x2...xN作为名称
    N = net.shape[0]
    Level = np.ones(N, dtype=int)
    # -----确定层级-----
    for i in range(N):
        for j in range(i + 1, N):
            if net[i][j] == 1 and Level[j] <= Level[i]:
                Level[j] += 1
            if net[i][j] == -1 and Level[i] <= Level[j]:
                Level[i] += 1
    # -----确定横向坐标-----
    position = np.zeros(N)
    for i in set(Level):
        num = sum(Level == i)
        position[Level == i] = np.linspace(-(num - 1) / 2, (num - 1) / 2, num)
    # -----画图-----
    plt.figure()
    plt.title(title)
    # 设置出图显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # --先画出各个结点---
    for i in range(N):
        if name == None:
            text = 'x%d' % (i + 1)
        else:
            text = name[i]
        plt.annotate(text, xy=[position[i], Level[i]], bbox={'boxstyle': 'circle', 'fc': '1'}, ha='center')
    # --再画连接线---
    for i in range(N):
        for j in range(i + 1, N):
            if net[i][j] == 1:
                xy = np.array([position[j], Level[j]])
                xytext = np.array([position[i], Level[i]])
            if net[i][j] == -1:
                xy = np.array([position[i], Level[i]])
                xytext = np.array([position[j], Level[j]])
            if net[i][j] != 0:
                L = np.sqrt(sum((xy - xytext) ** 2))
                xy = xy - (xy - xytext) * 0.2 / L
                xytext = xytext + (xy - xytext) * 0.2 / L
                if (xy[0] == xytext[0] and abs(xy[1] - xytext[1]) > 1) or \
                        (xy[1] == xytext[1] and abs(xy[0] - xytext[0]) > 1):
                    arrowprops = dict(arrowstyle='->', connectionstyle='arc3,rad=0.3')
                    # 画弧线，避免遮挡(只考虑了横向和竖向边，暂未考虑斜向边遮挡的情况)
                else:
                    arrowprops = dict(arrowstyle='->')
                plt.annotate('', xy=xy, xytext=xytext, arrowprops=arrowprops, ha='center')
    plt.axis([position.min(), position.max(), Level.min(), Level.max() + 0.5])
    plt.axis('off')
    plt.show()


def AIC_score(net, D, consider=None):
    # 计算评分函数
    # 输入：
    #     net:贝叶斯网络
    #     D:数据集
    # 输出：
    #    [struct,emp]:评分函数的结构项和经验项

    # -----从数据集D中提取一些信息-----
    m, N = D.shape  # 样本数和特征数
    values = [np.unique(D[:, i]) for i in range(len(D[0]))]  # 各个离散属性的可能取值
    # -----父节点-----
    parents = [list(np.where(net[i, :] == -1)[0] + 1) +
               list(np.where(net[:, i] == 1)[0] + 1)
               for i in range(N)]
    # -----计算AIC评分-----
    struct, emp = 0, 0  # AIC评分的结构项和经验项
    if consider == None:
        consider = range(N)
    for i in consider:
        r = len(values[i])  # Xi结点的取值数
        pa = parents[i]  # Xi的父节点编号
        nums = [len(values[p - 1]) for p in pa]  # 父节点取值数
        q = np.prod(nums)  # 父节点取值组合数
        struct += q * (r - 1)  # 对结构项的贡献
        # -----如果父节点数目为零，亦即没有父节点
        if len(pa) == 0:
            for value_k in values[i]:
                Dk = D[D[:, i] == value_k]  # D中Xi取值v_k的子集
                mk = len(Dk)  # Dk子集大小
                if mk > 0:
                    emp -= mk * np.log(mk / m)  # 对经验项的贡献
            continue
        # -----有父节点时，通过编码方式，遍历所有父节点取值组合
        for code in range(q):
            # 解码：比如，父节点有2×3种组合，
            # 将0~5解码为[0,0]~[1,2]
            code0 = code

            decode = []
            for step in range(len(pa) - 1):
                wight = np.prod(nums[step + 1:])
                decode.append(code0 // wight)
                code0 = code0 % wight
            decode.append(code0)

            # 父节点取某一组合时的子集
            index = range(m)  # 子集索引号，初始为全集D
            for j in range(len(pa)):
                indexj = np.where(D[:, pa[j] - 1] == values[pa[j] - 1][decode[j]])[0]
                index = np.intersect1d(index, indexj)
            Dij = D[index, :]  # 子集
            mij = len(Dij)  # 子集大小
            if mij > 0:  # 仅当子集非空时才计算该种情况
                for value_k in values[i]:
                    Dijk = Dij[Dij[:, i] == value_k]  # Dij中Xi取值v_k的子集
                    mijk = len(Dijk)  # Dijk子集大小
                    if mijk > 0:
                        emp -= mijk * np.log(mijk / mij)  # 对经验项的贡献
    return np.array([struct, emp])


def main():
    data, labels = load_data("watermelon_3a.csv")
    data = np.array(data)
    m, n = data.shape
    net = np.zeros((n, n))

    # 取值0表示无边，取值1表示Xi->Xj,取值-1表示Xi<-Xj
    flag = True  # 若存在环，则重新生成
    while flag:
        for i in range(n - 1):
            net[i, i + 1:] = np.random.randint(-1, 2, n - i - 1)
        flag = len(BNet(net)[2]) != 0

    # 画初始图
    draw(net, labels, '初始结构图')

    score0 = AIC_score(net, data)
    score = [score0]
    print('===========训练贝叶斯网============')
    print('初始AIC评分:%.3f(结构%.3f,经验%.3f)' % (sum(score0), score0[0], score0[1]))

    eta, tao = 0.1, 50  # 允许eta的概率调整到BIC评分增大的网络
    # 阈值随迭代次数指数下降
    for loop in range(10000):
        # 随机指定需要调整的连接边的两个节点：Xi和Xj
        i, j = np.random.randint(0, n, 2)
        while i == j:
            i, j = np.random.randint(0, n, 2)
        i, j = (i, j) if i < j else (j, i)
        # 确定需要调整的结果
        value0 = net[i, j]
        change = np.random.randint(2) * 2 - 1  # 结果为+1或-1
        value1 = (value0 + 1 + change) % 3 - 1  # 调整后的取值
        net1 = net.copy()
        net1[i, j] = value1
        if value1 != 0 and len(BNet(net1)[2]) != 0:
            # 如果value1取值非零，说明为转向或者增边
            # 若引入环，则放弃该调整
            continue
        delta_score = AIC_score(net1, data, [i, j]) - AIC_score(net, data, [i, j])
        if sum(delta_score) < 0 or np.random.rand() < eta * np.exp(-loop / tao):
            score0 = score0 + delta_score
            score.append(score0)
            print('调整后AIC评分:%.3f(结构%.3f,经验%.3f)'
                  % (sum(score0), score0[0], score0[1]))
            net = net1
        else:
            continue

    draw(net, labels, '最终网络结构')

    score = np.array(score)
    x = np.arange(len(score))
    plt.title('AIC贝叶斯网络结构搜索过程')
    plt.xlabel('更新次数')
    plt.ylabel('分值')
    plt.plot(x, score[:, 0], '.r-')
    plt.plot(x, score[:, 1], '.b-')
    plt.plot(x, score.sum(axis=1), '.k-')
    plt.legend(['struct', 'emp', 'AIC(struct+emp)'])
    plt.show()


if __name__ == '__main__':
    main()
