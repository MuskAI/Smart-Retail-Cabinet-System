#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：vis_yolo_label_file.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/8 10:39 
'''
import cv2
import os

def read_yolo_labels(label_file):
    with open(label_file, 'r') as file:
        lines = file.readlines()
        labels = []
        for line in lines:
            data = line.strip().split(' ')
            labels.append([float(data[i]) for i in range(1, len(data))])
        return labels

def visualize_boxes(image_dir, label_dir):
    img_files = sorted(os.listdir(image_dir))  # 排序确保顺序
    index = 0  # 当前图片的索引

    while 0 <= index < len(img_files):

        img_file = img_files[index]
        img_path = os.path.join(image_dir, img_file)
        label_path = os.path.join(label_dir, img_file.replace('.jpg', '.txt'))
        if '.DS_Store' in img_path:
            index +=1
            continue
        image = cv2.imread(img_path)

        h, w, _ = image.shape

        yolo_labels = read_yolo_labels(label_path)
        for label in yolo_labels:
            x_center = int(label[0] * w)
            y_center = int(label[1] * h)
            box_width = int(label[2] * w)
            box_height = int(label[3] * h)

            x1 = int(x_center - box_width / 2)
            y1 = int(y_center - box_height / 2)
            x2 = int(x_center + box_width / 2)
            y2 = int(y_center + box_height / 2)

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow('Image with Boxes', image)
        key = cv2.waitKey(0) & 0xFF

        if key == 27:  # ESC键退出
            break
        elif key == 0 or key==2:  # 上箭头键
            index = max(0, index - 1)
        elif key == 1 or key==3:  # 下箭头键
            index = min(len(img_files) - 1, index + 1)

    cv2.destroyAllWindows()

# 调用示例
img_dirs = "/Volumes/HIKVISION/fix_results/images"
label_dirs = "/Volumes/HIKVISION/fix_results/nms_labels"
visualize_boxes(img_dirs, label_dirs)
