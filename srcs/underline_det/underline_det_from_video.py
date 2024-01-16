#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：underline_det_from_video.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/13 02:31 
'''

import os
import sys

import onnxruntime
import numpy as np
import time
import cv2
from PIL import Image
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image, ImageDraw
matplotlib.use("TkAgg")

sys.path.append('')

sys.path.append('../')
from inference_onnx import UnderlineInfer

model_path_product = "../model_zoo/underline-yolov3-mobv2.onnx"
inference_engine = UnderlineInfer(model_path_product)
video_dir = '/Users/musk/Desktop/智能售货柜/测试视频'
video_list = os.listdir(video_dir)
def plot_line_chart(data, title="chat", x_label="X", y_label="Y", legend_label="data"):
    # 创建x轴坐标
    if len(data)==0:
        return None
    x = list(range(len(data)))

    # 绘制折线图
    plt.plot(x, data, marker='o', linestyle='-', color='b', label=legend_label)

    # 添加标题和标签
    # plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # 添加图例
    # plt.legend()

    # 显示折线图
    # plt.imshow()
    plt.savefig(str(time.time())+'.png')

def calculate_bbox_sum_and_draw_histogram(image, x1, y1, x2, y2):
    # Crop the region of interest (ROI) from the image based on the bbox coordinates
    roi = image[y1:y2, x1:x2]

    # Calculate the sum of pixel values within the ROI
    bbox_sum = np.sum(roi)
    return bbox_sum
if __name__ == '__main__':

    all_list = []
    for idx, video_path in enumerate(video_list):
        video_path = os.path.join(video_dir, video_path)
        ###
        video = cv2.VideoCapture(video_path)
        # 循环直到视频结束
        pixel_sum_list = []
        while video.isOpened():
            # 读取下一帧
            ret, frame = video.read()

            # 如果正确读取帧，ret为True
            if not ret:
                print("无法读取视频，或视频播放完毕")
                break

            # img = cv2.imread(image_path)
            img = frame
            if img is None:
                continue
            # 将图像从BGR转换为RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 检查是否成功读取图像
            if img is None:
                # print(f"无法读取图像文件：{image_path}")
                continue
            # 检查图像通道数
            if img.shape[2] == 4:
                # 将四通道图像转换为三通道
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            input_data = np.array(img)

            s1 = time.time()
            ret = inference_engine.infer(input_data)
            ret = inference_engine.filter_result(ret)
            ret = inference_engine.resize_and_map_coordinates_with_clipping(ret)

            e1 = time.time()
            print('Underline detection model Inference time:', e1 - s1)
            if ret is not None:
                _sum = calculate_bbox_sum_and_draw_histogram(frame,
                                                             ret[0][0],
                                                             ret[0][1],
                                                             ret[0][2],
                                                             ret[0][3])
                pixel_sum_list.append(_sum)
                inference_engine.visualize_result(ret, img)
        all_list.append(pixel_sum_list)
        # 释放视频对象
        video.release()



    print(all_list)

    for i in all_list:
        plot_line_chart(i)