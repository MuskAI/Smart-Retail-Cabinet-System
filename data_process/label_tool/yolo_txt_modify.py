#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：yolo_txt_modify.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/11 15:18 
'''
import os

import os

# 源文件路径
src_path = "/Volumes/HIKVISION/fix_results/nms_labels"
#
# # 目标文件保存路径
dst_root = "/Volumes/HIKVISION/fix_results/modify_labels"
#
#
# images_path = '/Volumes/HIKVISION/三批次里取有用的/标注图片'
# images_list = os.listdir(images_path)
# # 获取源路径下的所有txt文件
# txt_files = [f for f in os.listdir(src_path) if f.endswith(".txt")]
txt_files = os.listdir(src_path)
# 循环遍历每个txt文件
for txt_file in txt_files:
    src_file_path = os.path.join(src_path, txt_file)
    dst_file_path = os.path.join(dst_root, txt_file)
    print(src_file_path)

    # 打开源文件进行读取和处理
    with open(src_file_path, 'r') as src_file:
        lines = src_file.readlines()
        print(lines)

    # 如果文件不为空，替换第一个空格前的数字为'1'
    new_lines = []
    for idx in range(len(lines)):
        cls = lines[idx].split(' ')[0]
        new_line = ''
        _ = lines[idx].split(' ')
        for i in range(len(_)):
            if i ==0:
                new_line+='1'
            else:
                new_line += ' '+_[i]


        new_lines.append(new_line)


    # 将修改后的内容写入目标文件
    with open(dst_file_path, 'w') as dst_file:
        dst_file.writelines(new_lines)
