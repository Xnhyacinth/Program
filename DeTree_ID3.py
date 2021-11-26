#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/10/23 13:44
import copy
import json
import os
from math import log
import graphviz
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
import TreePlot
from program.ML import treePlotter
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

os.chdir("D:/桌面/ML/Assignment3")  # 切换工作目录


def load_data(path):  # 读取数据并处理数据
    data = pd.read_csv(path + "data.csv")
    data = data.drop(['group'], axis=1)
    fail_data = pd.read_csv(path + "failureInfo.csv")
    normal_data = pd.read_csv(path + "normalInfo.csv")

    # 对时间标签做处理，分类出label:
    # label = 1: 故障时间区域
    # label = 0: 正常时间区域
    # label = -1:无效数据
    labels = []
    for i in range(len(data)):
        flag = 0
        for j in range(len(fail_data)):
            if fail_data.startTime[j] <= data.iloc[i][0] <= fail_data.endTime[j]:
                labels.append(1)
                flag = 1
                break
        for j in range(len(normal_data)):
            if normal_data.startTime[j] <= data.iloc[i][0] <= normal_data.endTime[j]:
                labels.append(0)
                flag = 1
                break

        if flag == 0:
            labels.append(-1)

    # 删除无效数据
    y = labels
    x = []
    for i in range(len(data)):
        if y[i] == -1:
            x.append(i)
    data = data.drop(x)
    data = data.drop('time', axis=1)

    for i in range(len(y) - 1, -1, -1):
        if y[i] == -1:
            y.pop(i)

    return data, y


def Data_Partition(data, y):  # 划分数据集
    x_train, x_test, y_train, y_test = \
        train_test_split(data, y, test_size=0.3)
    # x_train, x_test, y_train, y_test = \
    #     train_test_split(x_train, y_train, test_size=0.3)
    x_train = np.array(x_train)
    x_test = np.array(x_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    return x_train, x_test, y_train, y_test


def cal_Ent(data):  # 计算信息熵
    num = len(data)
    counts = {}
    for i in data:
        label = i[-1]
        if label not in counts.keys():
            counts[label] = 0
        counts[label] += 1  # 计算每一类样本数量
    ent = 0.0
    for key in counts.keys():
        p = float(counts[key]) / num  # 求p
        ent -= p * log(p, 2)
    return ent


def split_data(data, feat, value):  # 划分数据集，为下一层计算准备
    data_new = []
    for vec in data:
        if vec[feat] == value:
            vec_new = list(vec[:feat])
            vec_new.extend(list(vec[feat + 1:]))  # 除去原样本集的第feat列
            data_new.append(vec_new)
    return data_new


# 划分数据集, axis:按第几个特征划分, value:划分特征的值, LorR: value值左侧（小于）或右侧（大于）的数据集
def splitDataSet_c(data, axis, value, LorR='L'):
    ret_data = []
    if LorR == 'L':
        for featVec in data:
            if float(featVec[axis]) < value:
                ret_data.append(featVec)
    else:
        for featVec in data:
            if float(featVec[axis]) > value:
                ret_data.append(featVec)
    return ret_data


def ChooseBestFeature(data, label_p):
    num = len(data[0]) - 1
    ent_sup = cal_Ent(data)  # 计算父样本信息熵
    # print(ent_sup)
    info_gain_max = 0.0  # 初始信息增益为0
    best_feature = -1
    best_value = None  # 最佳连续划分值
    for i in range(num):
        feat_list = [example[i] for example in data]  # 获取数据集中当前特征下的所有值组成list
        feat = set(feat_list)
        ent = 0.0
        best_value_i = 0.0
        if label_p[i] == 0:  # 离散特征
            for value in feat:
                sub_data = split_data(data, i, value)  # 获得该种特征该种结果的子样本集（去除了这种特征后的）
                p = len(sub_data) / float(len(data))  # 计算|Dv|/|D|,计算子样本集样本数所占父样本数权重
                ent += p * cal_Ent(sub_data)  # 计算各个子样本集的权重*子样本集信息熵并加和
        else:  # 连续特征
            feat_sorted = list(feat)
            feat_sorted.sort()
            ent_min = 999999
            for j in range(len(feat_sorted) - 1):
                label = float(feat_sorted[j] + feat_sorted[j + 1]) / 2
                # 对每个划分点，计算信息熵
                data_left = splitDataSet_c(data, i, label, 'L')
                data_right = splitDataSet_c(data, i, label, 'R')
                p_left = len(data_left) / float(len(data))
                p_right = len(data_right) / float(len(data))
                ent_p = p_right * cal_Ent(data_right) + p_left * cal_Ent(data_left)
                if ent_p < ent_min:
                    ent_min = ent_p
                    best_value_i = label
            ent = ent_min
        info_gain = ent_sup - ent  # 计算信息增益
        # print(i, "信息增益：", info_gain)
        if info_gain > info_gain_max:
            info_gain_max = info_gain
            best_feature = i
            best_value = best_value_i
    return best_feature, best_value


def majorityCnt(class_list):
    '''返回标签列表中最多的标签'''
    count_dict = {}
    for label in class_list:
        if label not in count_dict.keys():
            count_dict[label] = 0
        count_dict[label] += 1
    # print(count_dict)
    return max(zip(count_dict.values(), count_dict.keys()))[1]


def create_tree(data, labels, label_p):
    class_list = [example[-1] for example in data]  # 类别向量
    if class_list.count(class_list[0]) == len(class_list):  # 如果只有一个类别，返回
        return class_list[0]
    if len(data[0]) == 1:  # 所有特征遍历完
        return majorityCnt(class_list)  # 返回出现次数最多的类别
    best_feature, best_value = ChooseBestFeature(data, label_p)
    if best_feature == -1:  # 如果无法选出最优分类特征，返回出现次数最多的类别
        return majorityCnt(class_list)  # 返回出现次数最多的类别
    if label_p[best_feature] == 0:  # 对离散的特征
        best_feat_label = labels[best_feature]
        my_tree = {best_feat_label: {}}
        labels_new = copy.copy(labels)
        label_p_new = copy.copy(label_p)
        del (labels_new[best_feature])  # 已经选择的特征不再参与分类
        del (label_p_new[best_feature])
        feat_values = [example[best_feature] for example in data]
        unique_value = set(feat_values)  # 该特征包含的所有值
        for value in unique_value:  # 对每个特征值，递归构建树
            sub_labels = labels_new[:]
            sub_label_p = label_p_new[:]
            my_tree[best_feat_label][value] = create_tree(
                split_data(data, best_feature, value), sub_labels,
                sub_label_p)
    else:  # 对连续的特征，不删除该特征，分别构建左子树和右子树
        best_feat_label = labels[best_feature] + '<' + str(best_value)
        my_tree = {best_feat_label: {}}
        sub_labels = labels[:]
        sub_label_p = label_p[:]
        # 构建左子树
        value_left = '是'
        my_tree[best_feat_label][value_left] = create_tree(
            splitDataSet_c(data, best_feature, best_value, 'L'), sub_labels,
            sub_label_p)
        # 构建右子树
        value_right = '否'
        my_tree[best_feat_label][value_right] = create_tree(
            splitDataSet_c(data, best_feature, best_value, 'R'), sub_labels,
            sub_label_p)
    return my_tree


# 测试算法
def classify_c(my_tree, labels, label_p, test):
    first_str = list(my_tree.keys())[0]  # 根节点

    first_label = first_str
    less_index = str(first_str).find('<')
    if less_index > -1:  # 如果是连续型的特征
        first_label = str(first_str)[:less_index]
    second_dict = my_tree[first_str]

    feat_index = labels.index(first_label)  # 跟节点对应的特征
    class_label = None
    for key in second_dict.keys():  # 对每个分支循环
        if label_p[feat_index] == 0:  # 离散的特征
            if test[feat_index] == key:  # 测试样本进入某个分支
                if type(second_dict[key]).__name__ == 'dict':  # 该分支不是叶子节点，递归
                    class_label = classify_c(second_dict[key], labels,
                                             label_p, test)
                else:  # 如果是叶子， 返回结果
                    class_label = second_dict[key]
        else:
            part_value = float(str(first_str)[less_index + 1:])
            if test[feat_index] < part_value:  # 进入左子树
                if type(second_dict['是']).__name__ == 'dict':  # 该分支不是叶子节点，递归
                    class_label = classify_c(second_dict['是'], labels,
                                             label_p, test)
                else:  # 如果是叶子， 返回结果
                    class_label = second_dict['是']
            else:
                if type(second_dict['否']).__name__ == 'dict':  # 该分支不是叶子节点，递归
                    class_label = classify_c(second_dict['否'], labels,
                                             label_p, test)
                else:  # 如果是叶子， 返回结果
                    class_label = second_dict['否']

    return class_label


def main():
    data, y = load_data("train/15/")
    data['flag'] = y
    labels = data.columns.values.tolist()
    label_p = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    x_train, x_test, y_train, y_test = Data_Partition(data, y)

    err_my = 0
    my_tree = create_tree(x_train, labels, label_p)
    print(my_tree)
    for i in range(len(x_test)):
        if classify_c(my_tree, labels, label_p, x_test[i]) != y_test[i]:
            err_my += 1
    print("my error rate is:", err_my / len(y_test))
    treePlotter.createPlot(my_tree)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    err_m = 0
    # y_predict = []
    for i in range(len(x_test)):
        # y_predict.append(clf.predict([x_test[i]]))
        if clf.predict([x_test[i]]) != y_test[i]:
            err_m = err_m + 1
    print("err's num is:", err_m)
    print("model's error rate is:", err_m / len(y_test))
    # print(y_test)
    # print(y_predict)
    dot_data = tree.export_graphviz(clf, out_file=None, feature_names=data.columns.values.tolist(),
                                    class_names=["normal", "failure"],
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render("15_predict")

    # a = pd.read_csv("D:/桌面/1.csv")
    # labels = a.columns.values.tolist()
    # a = np.array(a)
    # label_p = [0, 0, 0, 0, 0, 0, 1, 1]  # 属性的类型，0表示离散
    # my_tree = create_tree(a, labels, label_p)
    # print(my_tree.keys())
    #
    #
    # testData = [1, 2, 2, 2, 3, 2, 0.222, 0.112]
    # ffd = classify_c(my_tree, labels, label_p, testData)
    # print(ffd)
    # labels = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感', '密度', '含糖率']
    # best_feature, best_value = ChooseBestFeature(a, label_p)
    # # print(best_value)
    # # print(best_feature)
    # treePlotter.createPlot(my_tree)
    # TreePlot.createPlot(my_tree)


if __name__ == '__main__':
    main()
