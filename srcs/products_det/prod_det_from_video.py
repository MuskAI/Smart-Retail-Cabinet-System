#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：prod_det_from_video.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/13 02:13 
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

matplotlib.use('TkAgg')

sys.path.append('')

sys.path.append('../')
from inference_onnx import ProductInfer

model_path_product = "../model_zoo/products-yolov3-mobv2-nohand.onnx"
inference_engine = ProductInfer(model_path_product)
video_dir = '/Volumes/HIKVISION/5666条视频数据（3秒内）'
video_list = os.listdir(video_dir)


for idx, video_path in enumerate(video_list):
    video_path = os.path.join(video_dir, video_path)
    ###
    video = cv2.VideoCapture(video_path)
    # 循环直到视频结束
    while video.isOpened():
        # 读取下一帧
        ret, frame = video.read()

        # 如果正确读取帧，ret为True
        if not ret:
            print("无法读取视频，或视频播放完毕")
            break
        #
        # # 显示帧
        # cv2.imshow('Frame', frame)
        #
        # 按 'q' 键退出循环
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     break

    # 释放视频对象qq
    # video.release()
    # 关闭所有OpenCV窗口
    # cv2.destroyAllWindows()

    ####3



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
        print('Product detection model Inference time:', e1 - s1)
        if ret is not None:
            inference_engine.visualize_result(ret, img)

