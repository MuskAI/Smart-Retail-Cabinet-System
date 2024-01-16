#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：split_train_val.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/9 10:42 
'''
import os
import shutil
import random
from tqdm import tqdm


def split_data(data_root, dst_root):
    train_root = os.path.join(dst_root, 'train')
    val_root = os.path.join(dst_root, 'val')
    os.makedirs(train_root, exist_ok=True)
    os.makedirs(val_root, exist_ok=True)

    classes = os.listdir(data_root)

    for cls in classes:
        class_path = os.path.join(data_root, cls)

        # 排除.DS_Store文件
        if cls == '.DS_Store':
            continue

        images = os.listdir(class_path)
        random.shuffle(images)

        split_index = int(0.9 * len(images))

        train_images = images[:split_index]
        val_images = images[split_index:]

        train_cls_path = os.path.join(train_root, cls)
        val_cls_path = os.path.join(val_root, cls)
        os.makedirs(train_cls_path, exist_ok=True)
        os.makedirs(val_cls_path, exist_ok=True)

        print(f"处理类别 '{cls}' 的数据...")
        for img in tqdm(train_images, desc='复制训练集'):
            src = os.path.join(class_path, img)
            dst = os.path.join(train_cls_path, img)
            shutil.copy(src, dst)

        for img in tqdm(val_images, desc='复制验证集'):
            src = os.path.join(class_path, img)
            dst = os.path.join(val_cls_path, img)
            shutil.copy(src, dst)


# 使用示例
data_root = '/Users/musk/Desktop/智能售货柜/xj_label_result_5000/good_bad_dataset'
dst_root = '/Users/musk/Desktop/智能售货柜/xj_label_result_5000/good_bad_dataset_split'

split_data(data_root, dst_root)
