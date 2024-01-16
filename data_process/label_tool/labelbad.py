#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：labelbad.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/10 15:35 

This script is a tiny tool to label images for retrieval
1. good
2. normal
3. bad
4. very bad

'''
import cv2
import os
import random
import shutil

# ASCII codes for 1, 2, 3, 4, 5 对应的标签文本
label_texts = {49: "good", 50: "normal", 51: "bad", 52: "verybad", 53: "notsingle"}


def display_image_with_label(img_path, label):
    image = cv2.imread(img_path)
    if image is None:
        print(f"Warning: Unable to load image at {img_path}")
        return None

    # 放大两倍
    image = cv2.resize(image, (0, 0), fx=2.0, fy=2.0)

    cv2.imshow('Image Labeling', image)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    return key


def label_images(data_root, dst_dir):
    img_paths = []
    for root, dirs, files in os.walk(data_root):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_paths.append(os.path.join(root, file))

    random.shuffle(img_paths)  # 随机打乱图片顺序

    for img_path in img_paths:
        file_name = os.path.basename(img_path)
        print(f"Displaying: {img_path}")

        label = 0
        while label not in [49, 50, 51, 52, 53]:  # ASCII codes for 1, 2, 3, 4, 5
            label = display_image_with_label(img_path, label)
            if label is None:
                continue

        # 保存标注结果
        label_dir = os.path.join(dst_dir, label_texts[label].replace(" ", "_"))  # Replace spaces for folder names
        if not os.path.exists(label_dir):
            os.makedirs(label_dir)
        shutil.copy(img_path, os.path.join(label_dir, file_name))
        print(f"Labeled {file_name} as {label_texts[label]}")
# 使用示例
data_root = '/Volumes/HIKVISION/crop_data_batch2'
dst_dir = '/Volumes/HIKVISION/label_result'
label_images(data_root, dst_dir)
