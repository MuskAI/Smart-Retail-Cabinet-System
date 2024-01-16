#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：labelfilter.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/11 11:39 
'''
import cv2
import os
import shutil
import random

data_root = "/Volumes/HIKVISION/三批次数据整合-36"  # 将此路径替换为您的数据根目录
dst_root = "/Volumes/HIKVISION/三批次里取有用的"  # 将此路径替换为您想保存图片的目的地目录

def get_new_filename(dst_path, filename):
    """
    如果文件已存在，则生成一个新的文件名。
    """
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(dst_path, new_filename)):
        new_filename = f"{name}_{counter}{ext}"
        counter += 1
    return new_filename

# 创建图片和标注文件的目标子目录
dst_images_path = os.path.join(dst_root, "标注图片")
dst_labels_path = os.path.join(dst_root, "label")
os.makedirs(dst_images_path, exist_ok=True)
os.makedirs(dst_labels_path, exist_ok=True)

# 收集所有图片及对应标注的路径
all_images = []
for category in os.listdir(data_root):
    if category == ".DS_Store":
        continue  # 忽略.DS_Store文件
    category_path = os.path.join(data_root, category)
    images_path = os.path.join(category_path, "标注图片")
    labels_path = os.path.join(category_path, "label")

    for image_name in os.listdir(images_path):
        image_path = os.path.join(images_path, image_name)
        label_name = os.path.splitext(image_name)[0] + '.txt'
        label_path = os.path.join(labels_path, label_name)
        if image_name == ".DS_Store":
            continue  # 忽略.DS_Store文件
        # 只有在对应的标注文件存在时，才添加到列表
        if os.path.exists(label_path):
            all_images.append((image_path, label_path))

# 随机打乱所有图片的顺序
random.shuffle(all_images)

# 设置计数器
count = 0

# 遍历随机打乱后的图片文件
for image_path, label_path in all_images:
    if count >= 500:
        break  # 如果已处理50张图片，则跳出循环

    image_name = os.path.basename(image_path)
    label_name = os.path.basename(label_path)

    # 显示图片
    image = cv2.imread(image_path)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)

    # 如果按下"1"，则保存图片及标注，并增加计数器
    if key == ord('1'):
        # 检查并更新文件名
        new_image_name = get_new_filename(dst_images_path, image_name)
        new_label_name = get_new_filename(dst_labels_path, label_name)

        dst_image_path = os.path.join(dst_images_path, new_image_name)
        dst_label_path = os.path.join(dst_labels_path, new_label_name)

        # 复制文件
        shutil.copy2(image_path, dst_image_path)
        shutil.copy2(label_path, dst_label_path)

        count += 1

cv2.destroyAllWindows()
