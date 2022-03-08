#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/3/8 17:38
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Read in the image
image = cv2.imread('img/1.jpg')

# Print out the type of image data and its dimensions (height, width, and color)
print('This image is:', type(image),
      ' with dimensions:', image.shape)


'''RGB'''
# RGB
# Make a copy of the image
image_copy = np.copy(image)

# OpenCV 会读取 BGR 格式（而不是 RGB 格式）的图像，因为一开始开发 OpenCV 的时候，BGR 颜色格式对相机制造商和图像软件提供商来说很受欢迎。
# 红色通道被认为是最不重要的颜色通道，因此列在最后面。但是，现在标准改变了，很多图像软件和相机都使用 RGB 格式

# Change color to RGB (from BGR)
image_copy_rgb = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)

# Display the image copy
plt.imshow(image_copy_rgb)

# 定义颜色阈值
lower_blue = np.array([0, 0, 250])
upper_blue = np.array([250, 250, 255])

# 创建遮罩
mask = cv2.inRange(image_copy_rgb, lower_blue, upper_blue)

# Vizualize the mask
plt.imshow(mask, cmap='gray')

masked_image_rgb = np.copy(image_copy_rgb)

masked_image_rgb[mask != 0] = [0, 0, 0]

# Display it!
plt.imshow(masked_image_rgb)
# Load in a background image, and convert it to RGB
background_image = cv2.imread('img/10.jpeg')
# print(background_image.shape)
background_image_rgb = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)

# Crop it to the right size (1482x988)
crop_background = background_image_rgb[0:1482, 0:988]

crop_background[mask == 0] = [0, 0, 0]

# Display the background
plt.imshow(crop_background)

# Add the two images together to create a complete image!
complete_image = masked_image_rgb + crop_background

# Display the result
plt.imshow(complete_image)



'''HSV'''
# Change color to HSV (from BGR)
image_copy_hsv = cv2.cvtColor(image_copy, cv2.COLOR_BGR2HSV)

# Display the image copy
plt.imshow(image_copy_hsv)

#提取图片的蓝色
lower_hsv=np.array([100,43,46])
upper_hsv=np.array([124,255,255])
mask=cv2.inRange(image_copy_hsv,lowerb=lower_hsv,upperb=upper_hsv)
plt.imshow(mask, cmap='gray')
# cv2.imshow("mask",mask)

masked_image_hsv = np.copy(image_copy_hsv)

masked_image_hsv[mask != 0] = [0, 0, 0]

# Display it!
plt.imshow(masked_image_hsv)

# convert image it to HSV

# print(background_image.shape)
background_image_hsv = cv2.cvtColor(background_image, cv2.COLOR_BGR2HSV)

# Crop it to the right size (1482x988)
crop_background = background_image_hsv[0:1482, 0:988]

crop_background[mask == 0] = [0, 0, 0]
plt.imshow(crop_background)

# Add the two images together to create a complete image!
complete_image_hsv = masked_image_hsv + crop_background

# Display the result
plt.imshow(complete_image_hsv)

# Change color to RGB (from HSV)
complete_image_hsv = cv2.cvtColor(complete_image_hsv, cv2.COLOR_HSV2RGB)
# Display the result
plt.imshow(complete_image_hsv)



'''HSL'''
# Change color to HLS (from BGR)
image_copy_hls = cv2.cvtColor(image_copy, cv2.COLOR_BGR2HLS)

# Display the image copy
plt.imshow(image_copy_hls)

#提取图片的蓝色
lower_hls=np.array([100,43,46])
upper_hls=np.array([124,255,255])
mask=cv2.inRange(image_copy_hls,lowerb=lower_hls,upperb=upper_hls)
plt.imshow(mask, cmap='gray')

masked_image_hls = np.copy(image_copy_hls)

masked_image_hls[mask != 0] = [0, 0, 0]

# Display it!
plt.imshow(masked_image_hls)

# convert image it to HLS

# print(background_image.shape)
background_image_hls = cv2.cvtColor(background_image, cv2.COLOR_BGR2HLS)

# Crop it to the right size (1482x988)
crop_background = background_image_hls[0:1482, 0:988]

crop_background[mask == 0] = [0, 0, 0]
plt.imshow(crop_background)


# Add the two images together to create a complete image!
complete_image_hls = masked_image_hls + crop_background

# Display the result
plt.imshow(complete_image_hls)

# Change color to RGB (from HSV)
complete_image_hls = cv2.cvtColor(complete_image_hls, cv2.COLOR_HLS2RGB)
# Display the result
plt.imshow(complete_image_hls)