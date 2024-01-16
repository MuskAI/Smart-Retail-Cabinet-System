#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：vis_data_distribution.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/8 14:41 

统计检索模型输入图片，也就是crop之后的图片的尺寸大小情况


'''
import os
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib
matplotlib.use('TkAgg')  # 尝试使用TkAgg后端

# 存储图片尺寸信息的列表
widths = []
heights = []
areas = []

# 文件夹路径
folder_path = '/Volumes/HIKVISION/crop_data'

# 获取文件夹中图片文件的总数
total_images = sum([len(files) for _, _, files in os.walk(folder_path) if files])

# 使用tqdm创建进度条
with tqdm(total=total_images, desc='Processing Images', unit='image') as pbar:
    # 遍历文件夹及其子文件夹下所有图片
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('png', 'jpg', 'jpeg', 'gif')):  # 确保文件是图片文件
                file_path = os.path.join(root, file)
                with Image.open(file_path) as img:
                    width, height = img.size
                    area = width * height
                    widths.append(width)
                    heights.append(height)
                    areas.append(area)
                pbar.update(1)  # 更新进度条

# 统计信息
print(f"Total images: {len(widths)}")
print(f"Minimum Width: {min(widths)}, Maximum Width: {max(widths)}")
print(f"Minimum Height: {min(heights)}, Maximum Height: {max(heights)}")
print(f"Minimum Area: {min(areas)}, Maximum Area: {max(areas)}")

# 绘制直方图
plt.figure(figsize=(12, 5))

plt.subplot(1, 3, 1)
plt.hist(widths, bins=50, color='skyblue', edgecolor='black')
plt.title('Width Distribution')
plt.xlabel('Width')
plt.ylabel('Frequency')

plt.subplot(1, 3, 2)
plt.hist(heights, bins=50, color='salmon', edgecolor='black')
plt.title('Height Distribution')
plt.xlabel('Height')
plt.ylabel('Frequency')

plt.subplot(1, 3, 3)
plt.hist(areas, bins=50, color='lightgreen', edgecolor='black')
plt.title('Area Distribution')
plt.xlabel('Area')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
