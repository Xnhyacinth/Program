#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/3/8 17:23

from matplotlib import pyplot as plt
import cv2
import numpy as np


# 定义高斯噪声函数
def noise_Gaussian(img, mean, var):
    """
    img:原始图像
    mean：均值
    var：方差，值越大噪声越大
    """

    # 创建均值为mean方差为var呈高斯分布的图像矩阵
    noise = np.random.normal(mean, var ** 0.5, img.shape)

    # 将原始图像的像素值进行归一化，除以255使像素值在0-1之间
    img = np.array(img / 255, dtype=float)

    # 噪声和图片合并即加噪后的图像
    out = img + noise

    # 解除归一化，乘以255将加噪后的图像的像素值恢复
    out = np.uint8(out * 255)
    return out


# 高斯滤波器

def gaussian_filter(img, K_size=3, sigma=1.0):
    img = np.asarray(np.uint8(img))
    if len(img.shape) == 3:
        H, W, C = img.shape
    else:
        img = np.expand_dims(img, axis=-1)
        H, W, C = img.shape

    ## Zero padding
    pad = K_size // 2
    out = np.zeros((H + pad * 2, W + pad * 2, C), dtype=np.float64)
    out[pad: pad + H, pad: pad + W] = img.copy().astype(np.float64)

    ## prepare Kernel
    K = np.zeros((K_size, K_size), dtype=np.float64)
    for x in range(-pad, -pad + K_size):
        for y in range(-pad, -pad + K_size):
            K[y + pad, x + pad] = np.exp(-(x ** 2 + y ** 2) / (2 * (sigma ** 2)))
    K /= (2 * np.pi * sigma * sigma)
    K /= K.sum()
    tmp = out.copy()

    # filtering
    for y in range(H):
        for x in range(W):
            for c in range(C):
                out[pad + y, pad + x, c] = np.sum(K * tmp[y: y + K_size, x: x + K_size, c])
    out = np.clip(out, 0, 255)
    out = out[pad: pad + H, pad: pad + W].astype(np.uint8)
    return out


if __name__ == "__main__":
    # 上传图片
    # read the image
    img = cv2.imread("D:/photo/11.jpeg")

    # Print out the type of image data and its dimensions (height, width, and color)
    print('This image is:', type(img),
          ' with dimensions:', img.shape)

    img_copy = np.copy(img)
    # change color to rgb(from bgr)
    img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
    # display
    cv2.imshow("img", img_copy)

    ## 添加高斯噪声
    # 显示添加高斯噪声的结果图像
    out = noise_Gaussian(img_copy, mean=0, var=0.003)
    cv2.imshow("out", out)

    # sigma=0.5 k_size=3
    out_05 = gaussian_filter(img_copy, sigma=0.5)
    cv2.imshow("out_05", out_05)

    # sigma=0.5 k_size=5
    out_05_5 = gaussian_filter(img_copy, K_size=5, sigma=0.5)
    cv2.imshow("out_05_5", out_05_5)

    cv2.waitKey(0)
