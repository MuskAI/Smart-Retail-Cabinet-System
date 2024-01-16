#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：yolo2coco.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/11 16:21 
'''
import json
import os
from PIL import Image

# 源YOLO标注文件的路径
yolo_annotations_path = "/Volumes/HIKVISION/fix_results/fixed_product_dataset/modify_labels"

# 图像文件的根目录
image_root = "/Volumes/HIKVISION/fix_results/fixed_product_dataset/images"

# 目标COCO标注文件的路径
coco_annotations_path = "/Volumes/HIKVISION/fix_results/fixed_product_dataset"

# COCO格式标注文件的基本结构
coco_data = {
    "info": {},
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": []
}

# 读取YOLO标注文件并转换为COCO格式
count = 0
for idx,filename in enumerate(os.listdir(yolo_annotations_path)):
    if filename.endswith(".txt"):
        with open(os.path.join(yolo_annotations_path, filename), "r") as yolo_file:
            lines = yolo_file.readlines()
            # image_id = int(filename.split(".")[0])-1  # 假设YOLO标注文件与图像文件有相同的文件名，仅扩展名不同
            image_filename = filename.replace(".txt", ".jpg")  # 假设图像文件扩展名为.jpg
            image_path = os.path.join(image_root, image_filename)  # 构建图像文件的完整路径

            # 使用PIL库获取图像的宽度和高度
            with Image.open(image_path) as img:
                image_width, image_height = img.size

            # 创建COCO格式的图像信息
            coco_image = {
                "id": idx+1,
                "width": image_width,
                "height": image_height,
                "file_name": image_filename
            }

            coco_data["images"].append(coco_image)

            # 读取YOLO标注信息并转换为COCO格式
            for line in lines:
                class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.split())
                bbox_x = max(0, (x_center - bbox_width / 2) * image_width)
                bbox_y = max(0, (y_center - bbox_height / 2) * image_height)
                bbox_width = min(image_width, bbox_width * image_width)
                bbox_height = min(image_height, bbox_height * image_height)

                count +=1
                coco_annotation = {
                    "id": count+1,
                    "image_id": idx+1,
                    "category_id": int(class_id),
                    "bbox": [bbox_x, bbox_y, bbox_width, bbox_height],
                    "area": bbox_width * bbox_height,
                    "iscrowd": 0  # 如果需要标记分割掩码，可以更改为1
                }

                coco_data["annotations"].append(coco_annotation)

# 填充COCO格式的categories字段（类别信息）
# 请根据YOLO数据集的类别信息进行填写
coco_data["categories"] = [
    {"id": 1, "name": "products"}
]

# 保存COCO格式标注文件
with open(os.path.join(coco_annotations_path, "annotations.json"), "w") as coco_file:
    json.dump(coco_data, coco_file)
