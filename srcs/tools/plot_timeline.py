#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：plot_timeline.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/16 16:44 
'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
def plot_timeline(data_list):
    # 创建时间轴
    time_axis = np.arange(len(data_list))

    # 创建一个颜色列表，用于表示非None元素和None元素
    colors = ['blue' if item is not None else 'red' for item in data_list]

    # 绘制时间轴
    plt.figure(figsize=(10, 2))  # 设置图形大小
    plt.bar(time_axis, [1] * len(data_list), color=colors, width=0.9)

    # 可以添加一些额外的样式，如标题和坐标轴标签
    plt.title('incidence / frame')
    plt.xlabel('frames number')

    # 设置x轴标签为时间轴上的位置
    step = max(len(data_list) // 10, 1)  # 设置步长，例如每隔10帧显示一个刻度
    plt.xticks(time_axis[::step], labels=[str(i) for i in time_axis[::step]])  # 设置刻度位置和标签

    # 显示图形
    plt.show()

