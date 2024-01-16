#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：vis_coco_label_file.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/8 11:59 
'''
import os
from pycocotools.coco import COCO
import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # 尝试使用TkAgg后端

# COCO标注文件路径
annotation_file = '/Volumes/HIKVISION/fix_results/fixed_product_dataset/annotations.json'
# 图片文件夹路径
image_folder = '/Volumes/HIKVISION/fix_results/fixed_product_dataset/images'
# 初始化COCO对象
coco = COCO(annotation_file)

# 获取所有图片ID
image_ids = coco.getImgIds()

# 遍历图片并可视化标注结果
for img_id in image_ids:
    img_info = coco.loadImgs(img_id)[0]
    image_path = os.path.join(image_folder, img_info['file_name'])

    # 读取图像
    image = cv2.imread(image_path)

    # 获取该图像的所有标注
    ann_ids = coco.getAnnIds(imgIds=img_id)
    annotations = coco.loadAnns(ann_ids)

    # 绘制标注框
    for annotation in annotations:
        bbox = annotation['bbox']
        x, y, w, h = bbox
        category_id = annotation['category_id']
        category_info = coco.loadCats(category_id)[0]
        category_name = category_info['name']

        # 绘制矩形框
        cv2.rectangle(image, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 2)
        cv2.putText(image, category_name, (int(x), int(y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # 显示图像
    cv2.imshow('Annotation Visualization', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()