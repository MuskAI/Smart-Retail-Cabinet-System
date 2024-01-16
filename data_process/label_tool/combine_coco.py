#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System
@File    ：combine.py
@IDE     ：PyCharm
@Author  ：haoran
@Date    ：2024/1/11 19:21
'''
import json

# 读取第一个COCO标注文件
with open("/Users/musk/Downloads/product-coco1.json", "r") as coco1_file:
    coco1_data = json.load(coco1_file)

# 读取第二个COCO标注文件
with open("/Users/musk/Downloads/product-coco(1).json", "r") as coco2_file:
    coco2_data = json.load(coco2_file)

# 计算第二个COCO标注文件中的ID偏移量，以便重新编号
id_offset = max(image["id"] for image in coco1_data["images"]) + 1
ann_id_offset = max(ann["id"] for ann in coco1_data["annotations"]) + 1




# 更新第二个COCO标注文件中的图像ID字段，并合并到第一个COCO数据中
for image in coco2_data["images"]:
    image["id"] += id_offset
    coco1_data["images"].append(image)

# 更新第二个COCO标注文件中的ID字段，并合并到第一个COCO数据中
for annotation in coco2_data["annotations"]:
    annotation["image_id"] += id_offset
    annotation["id"] += ann_id_offset
    coco1_data["annotations"].append(annotation)



# 更新第二个COCO标注文件中的类别ID字段，并合并到第一个COCO数据中
for category in coco2_data["categories"]:
    # 检查是否已存在相同的类别名称，如果已存在，则跳过
    if all(cat["name"] != category["name"] for cat in coco1_data["categories"]):
        coco1_data["categories"].append(category)

# 保存合并后的COCO标注文件
with open("/Users/musk/Desktop/智能售货柜/数据标注/xj-product/product-combine-nohand-coco.json", "w") as merged_coco_file:
    json.dump(coco1_data, merged_coco_file, indent=4)
