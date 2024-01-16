#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：display_frames.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/16 16:39 
'''
import matplotlib.pyplot as plt

# 示例图像帧列表，这里使用了随机生成的示例图像
import numpy as np

import matplotlib.pyplot as plt
import numpy as np


def display_frames(frames_list):
    num_frames = len(frames_list)

    # 计算图像排列的行和列数
    rows = int(num_frames ** 0.5)
    cols = num_frames // rows
    if num_frames % rows != 0:
        cols += 1

    # 创建一个新的图形，按照计算出的行列数布局
    fig, axes = plt.subplots(rows, cols, figsize=(12, 8))

    for i, ax in enumerate(axes.ravel()):
        if i < num_frames:
            frame = frames_list[i]
            if frame is None:
                continue

            ax.imshow(frame)
            ax.axis('off')
            ax.set_title(f'Frame {i + 1}')  # 添加帧的序号作为标题
        else:
            ax.axis('off')  # 隐藏空的子图

    plt.tight_layout()
    plt.show()


