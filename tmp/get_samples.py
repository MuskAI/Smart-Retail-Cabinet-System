#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：get_samples.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/7 22:34

为了建立坐标系，需要标注售货柜的下边缘，这个脚本从数据集中提取图片，然后用于标注
'''
import os
import shutil
import random
import glob

def copy_random_images(data_root, dst_root):
    # 创建目标文件夹（如果不存在）
    os.makedirs(dst_root, exist_ok=True)

    # 遍历data_root下所有子目录
    for root, dirs, _ in os.walk(data_root):
        # 如果子目录中有名为“标注图片”的文件夹
        if "标注图片" in dirs:
            source_folder = os.path.join(root, "标注图片")

            # 获取标注图片文件夹中的所有文件
            image_files = glob.glob(os.path.join(source_folder, "*.jpg")) + glob.glob(os.path.join(source_folder, "*.png"))

            # 计算要复制的图片数量（30%）
            num_images_to_copy = int(len(image_files) * 0.3)

            # 随机选择要复制的图片
            images_to_copy = random.sample(image_files, num_images_to_copy)

            # 复制图片到目标文件夹
            for image in images_to_copy:
                destination_path = os.path.join(dst_root, os.path.basename(image))
                shutil.copyfile(image, destination_path)


# 调用函数并传入data_root和目标文件夹路径dst_root
data_root = '/Volumes/HIKVISION/商品标注30%'  # 替换为你的data_root路径
dst_root = '/Users/musk/Desktop/智能售货柜/数据标注/货柜下边缘检测'    # 替换为你的目标文件夹路径
copy_random_images(data_root, dst_root)
