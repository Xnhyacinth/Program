#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2021/10/5 20:49
import numpy as np
from sklearn.datasets import load_iris  # 导入数据集
import matplotlib.pyplot as plt

iris = load_iris()  # 载入数据集
# print(iris)

iris1 = iris.data[0:50, 0:4]
iris2 = iris.data[50:100, 0:4]
iris3 = iris.data[100:150, 0:4]

iris1_train = iris1[0:30, 0:4]
iris2_train = iris2[0:30, 0:4]
iris3_train = iris3[0:30, 0:4]
print(iris1)
# 计算类内均值
m1 = np.mean(iris1_train, axis=0)
m2 = np.mean(iris2_train, axis=0)
m3 = np.mean(iris3_train, axis=0)

# 计算类内离散度矩阵
s1 = np.zeros((4, 4))
s2 = np.zeros((4, 4))
s3 = np.zeros((4, 4))

for i in range(0, 30, 1):
    a = np.array([iris1[i] - m1])
    s1 = s1 + a.T @ a
for i in range(0, 30, 1):
    a = np.array([iris2[i] - m2])
    s2 = s2 + a.T @ a
for i in range(0, 30, 1):
    a = np.array([iris3[i] - m3])
    s3 = s3 + a.T @ a

# 计算总类内散度矩阵
s12 = s1 + s2
s13 = s1 + s3
s23 = s2 + s3

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

n1 = n2 = n3 = 0  # 各类别正确个数
iris1_new = iris2_new = iris3_new = []

# 测试
for i in range(30, 49, 1):
    x = np.array([iris1[i]])
    m12 = w12 @ x.T - w1
    m13 = w13 @ x.T - w2
    m23 = w23 @ x.T - w3
    print(x)
    if m12 > 0 and m13 > 0:
        iris1_new.extend(x)
        n1 = n1 + 1
    elif m12 < 0 and m23 > 0:
        iris2_new.extend(x)
    elif m13 < 0 and m23 < 0:
        iris3_new.extend(x)

for i in range(30, 49, 1):
    x = np.array([iris2[i]])
    m12 = w12 @ x.T - w1
    m13 = w13 @ x.T - w2
    m23 = w23 @ x.T - w3
    if m12 > 0 and m13 > 0:
        iris1_new.extend(x)
    elif m12 < 0 and m23 > 0:
        iris2_new.extend(x)
        n2 = n2 + 1
    elif m13 < 0 and m23 < 0:
        iris3_new.extend(x)

for i in range(30, 49, 1):
    x = np.array([iris3[i]])
    m12 = w12 @ x.T - w1
    m13 = w13 @ x.T - w2
    m23 = w23 @ x.T - w3
    if m12 > 0 and m13 > 0:
        iris1_new.extend(x)
    elif m12 < 0 and m23 > 0:
        iris2_new.extend(x)
    elif m13 < 0 and m23 < 0:
        iris3_new.extend(x)
        n3 = n3 + 1

print((n1 + n2 + n3) / 60)

# 花瓣与花萼的长度散点图
plt.scatter(iris1[:, 2], iris1[:, 0], color='red', marker='o', label='setosa')
plt.scatter(iris2[:, 2], iris2[:, 0], color='blue', marker='x', label='versicolor')
plt.scatter(iris3[:, 2], iris3[:, 0], color='green', label='virginica')
# line_x1 = np.arange(min(np.min(iris1[:, 2]), np.min(iris2[:, 2])),
#                     max(np.max(iris1[:, 2]), np.max(iris2[:, 2])),
#                     step=1)
# line_x2 = np.arange(min(np.min(iris1[:, 2]), np.min(iris3[:, 2])),
#                     max(np.max(iris1[:, 2]), np.max(iris3[:, 2])),
#                     step=1)
# line_x3 = np.arange(min(np.min(iris2[:, 2]), np.min(iris3[:, 2])),
#                     max(np.max(iris2[:, 2]), np.max(iris3[:, 2])),
#                     step=1)
# line_y1 = - (w12[0][2] / w12[0][0]) * line_x1
# line_y2 = - (w13[0][2] / w13[0][0]) * line_x2
# line_y3 = - (w23[0][2] / w23[0][0]) * line_x3
# plt.plot(line_x1, line_y1)
# plt.plot(line_x2, line_y2)
# plt.plot(line_x3, line_y3)
plt.xlabel('petal length')
plt.ylabel('sepal length')
plt.title("花瓣与花萼长度的散点图")
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False
plt.legend(loc='upper left')
plt.show()

# 花瓣与花萼的宽度度散点图
plt.scatter(iris1[:, 3], iris1[:, 1], color='red', marker='o', label='setosa')
plt.scatter(iris2[:, 3], iris2[:, 1], color='blue', marker='x', label='versicolor')
plt.scatter(iris3[:, 3], iris3[:, 1], color='green', label='virginica')
plt.xlabel('petal width')
plt.ylabel('sepal width')
plt.title("花瓣与花萼宽度的散点图")
plt.legend(loc='upper left')
plt.show()

print(iris1)