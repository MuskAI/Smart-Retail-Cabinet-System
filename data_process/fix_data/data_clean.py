#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：data_clean.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/16 11:33 
'''
import os
from PIL import Image
from tqdm import tqdm
if __name__ == '__main__':
    data_dir = '/Volumes/HIKVISION/fix_results/fixed_product_dataset/images'
    for idx, item in tqdm(enumerate(os.listdir(data_dir))):
        image_path = os.path.join(data_dir,item)
        try:
            # 使用PIL库获取图像的宽度和高度
            with Image.open(image_path) as img:
                image_width, image_height = img.size
        except:
            print(item)