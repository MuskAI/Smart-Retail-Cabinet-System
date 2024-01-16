#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：crop_and_save.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/8 11:11 
'''
import os
import cv2
from tqdm import tqdm


def crop_and_save(data_root, dst_root):
    classes = os.listdir(data_root)
    for class_folder in tqdm(classes, desc='Processing Classes'):
        class_path = os.path.join(data_root, class_folder)
        if os.path.isdir(class_path):
            images_folder = os.path.join(class_path, '标注图片')
            labels_folder = os.path.join(class_path, 'label')
            os.makedirs(os.path.join(dst_root, class_folder), exist_ok=True)

            if not os.path.exists(images_folder) or not os.path.exists(labels_folder):
                print(f"Missing folders in {class_folder}")
                continue

            label_files = os.listdir(labels_folder)
            for label_file in tqdm(label_files, desc=f'Processing {class_folder}', leave=False):
                try:
                    label_path = os.path.join(labels_folder, label_file)
                    image_file = label_file.replace('.txt', '.jpg')
                    image_path = os.path.join(images_folder, image_file)

                    if not os.path.exists(label_path) or not os.path.exists(image_path):
                        print(f"Missing files for {label_file} in {class_folder}")
                        continue

                    image = cv2.imread(image_path)
                    h, w, _ = image.shape

                    with open(label_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            data = line.strip().split(' ')
                            x_center = float(data[1]) * w
                            y_center = float(data[2]) * h
                            box_width = float(data[3]) * w
                            box_height = float(data[4]) * h

                            x1 = int(x_center - box_width / 2)
                            y1 = int(y_center - box_height / 2)
                            x2 = int(x_center + box_width / 2)
                            y2 = int(y_center + box_height / 2)

                            cropped_img = image[y1:y2, x1:x2]

                            dst_folder = os.path.join(dst_root, class_folder)
                            os.makedirs(dst_folder, exist_ok=True)
                            dst_image_path = os.path.join(dst_folder, f"{label_file[:-4]}_{x_center}_{y_center}.jpg")
                            cv2.imwrite(dst_image_path, cropped_img)
                except Exception as e:
                    print(f"Error processing {label_file} in {class_folder}: {e}")
                    continue


# 使用示例
data_root = "/Volumes/HIKVISION/三批次数据整合-36"
dst_root = "/Volumes/HIKVISION/crop_data"
crop_and_save(data_root, dst_root)
