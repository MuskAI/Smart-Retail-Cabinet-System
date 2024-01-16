#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：analysis_labeled_data.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/15 00:29 
'''
import os
import hashlib
from collections import defaultdict
from tqdm import tqdm

# 定义一个函数来计算文件的MD5值
def calculate_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(8192)  # 以8192字节块读取文件
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

# 输入要处理的文件夹路径
folder_path = '/Volumes/HIKVISION/三批次数据整合-36'

# 初始化一个字典来存储MD5值和对应文件数量的关系
md5_to_file_count = defaultdict(int)

# 使用tqdm添加进度条
for root, _, files in os.walk(folder_path):
    for file in tqdm(files, desc="处理中"):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            file_path = os.path.join(root, file)
            md5 = calculate_md5(file_path)
            md5_to_file_count[md5] += 1

# 统计相同MD5值的图片数量
for md5, count in md5_to_file_count.items():
    if count > 1:
        print(f"MD5: {md5}, 相同图片数量: {count}")
