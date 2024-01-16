#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：random_select.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/8 15:12

从三个批次的图片中，随机取出用以标注
'''

import os
import random
import shutil
from tqdm import tqdm

data_root = '/Volumes/HIKVISION/三批次数据整合'  # 数据根目录
output_folder = '/Volumes/HIKVISION/data_process_result/random_select'  # 保存随机选取的图片的目录


k = 70  # 随机选取的图片数量

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

selected_images_count = 0  # 统计已选中的图片数量

# 遍历一级目录下的所有二级目录（类别目录）
for class_folder in tqdm(os.listdir(data_root), desc='Processing Classes'):
    class_path = os.path.join(data_root, class_folder)
    if os.path.isdir(class_path):
        # 获取该类别下的标注图片目录路径
        image_folder = os.path.join(class_path, '标注图片')

        # 检查标注图片目录是否存在
        if os.path.exists(image_folder):
            # 获取标注图片文件列表
            image_files = os.listdir(image_folder)
            # 随机选择k张图片
            selected_images = random.sample(image_files, min(k, len(image_files)))

            # 复制选中的图片到输出文件夹
            for image in selected_images:
                image_path = os.path.join(image_folder, image)
                output_path = os.path.join(output_folder, f"image_{selected_images_count}.jpg")
                shutil.copy(image_path, output_path)
                selected_images_count += 1
