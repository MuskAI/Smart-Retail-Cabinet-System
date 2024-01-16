#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/11 21:37 
'''
import os
import cv2
import json
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from inference_onnx import UnderlineInfer
from inference_onnx import ProductInfer


# dev tools
from tools.display_frames import display_frames
from tools.plot_timeline import plot_timeline

###################



class SRCS:
    def __init__(self):
        self.video_length_thr = 5
        self.detected_list = {'product': [], 'underline': []}  # store three kinds of detected results
        self.video_capture = None
        self.frame_list = None
        self.underline_model_path = 'model_zoo/underline-yolov3-mobv2.onnx'
        self.product_model_path = 'model_zoo/products-yolov3-mobv2-nohand.onnx'
        self.underlineInfer = UnderlineInfer(self.underline_model_path)
        self.productInfer = ProductInfer(self.product_model_path)

    def read_video_and_filter(self,video_path):
        """
        1. read video
        2. filter video according to video length
        :param video_path:
        :return:  None ( this video is filtered )
        """
        if os.path.exists(video_path):
            video_capture = cv2.VideoCapture(video_path)  # 将'video.mp4'替换为您要打开的视频文件的路径

            # 获取视频的帧率（每秒帧数）
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))

            # 获取视频的总帧数
            total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

            # 计算视频的时长（以秒为单位）
            video_duration = total_frames / fps

            # 将时长转换为分钟和秒
            minutes = int(video_duration // 60)
            seconds = int(video_duration % 60)

            ###
            if minutes==0 and seconds<=self.video_length_thr:
                self.video_capture = video_capture
                return video_capture
            else:
                return None


            #####################
        else:
            raise FileExistsError("Video path not found")

    def get_all_frames(self):
        # 初始化一个空列表来存储帧
        frame_list = []

        while True:
            # 读取一帧
            ret, frame = self.video_capture.read()

            # 如果成功读取帧，将其添加到列表中
            if ret:
                frame_list.append(frame)
            else:
                break  # 如果没有更多帧可读取，则退出循环

        # 释放视频对象
        # self.video_capture.release()
        # self.video_capture = None
        self.frame_list = frame_list
        return frame_list

    def key_frames(self):
        pass

    def underline_det(self, frame):
        """
        Input one frame
        :param frame:
        :return:
        """
        row_result = self.underlineInfer.infer(frame)
        filter_result = self.underlineInfer.filter_result(row_result)
        result = self.underlineInfer.resize_and_map_coordinates_with_clipping(filter_result)
        if result is None:
            return None
        else:
            return result

    def product_det(self, frame):
        """
        Input one frame
        :param frame:
        :return:
        """
        row_result = self.productInfer.infer(frame)
        filter_result = self.productInfer.filter_result(row_result)
        result = self.productInfer.resize_and_map_coordinates_with_clipping(filter_result)
        if result is None:
            return None
        else:
            return result

    def product_infer_frames(self, frames):
        """
        对这段视频里的所有商品进行检测

        :param frames: 一段视频里的所有帧
        :return:
        """
        for idx, frame in enumerate(frames):
            frame_det_result = self.product_det(frame)
            self.detected_list['product'].append(frame_det_result)

        return self.detected_list['product']

    def underline_infer_frames(self, frames):
        """
        对这段视频里的所有下边缘进行检测

        :param frames: 一段视频里的所有帧
        :return:
        """
        for idx, frame in enumerate(frames):
            frame_det_result = self.product_det(frame)
            self.detected_list['underline'].append(frame_det_result)

        return self.detected_list['underline']

if __name__ == '__main__':
    srcs_engine = SRCS()
    video_path = '/Volumes/HIKVISION/5666条视频数据（5秒内）/308277952_top_1700012900589.mp4'
    video_capture = srcs_engine.read_video_and_filter(video_path)
    # if video_capture is not None:
    #     frames = srcs_engine.get_all_frames()
    #     underline_result = srcs_engine.underline_infer_frames(frames)
    #     # dev tools
    #     plot_timeline(underline_result)
    #     #####
    #     formatted_list = json.dumps(underline_result, indent=4)
    #     print(formatted_list)
    #     display_frames(srcs_engine.frame_list)

    if video_capture is not None:
        frames = srcs_engine.get_all_frames()
        product_result = srcs_engine.product_infer_frames(frames)
        plot_timeline(product_result)
        formatted_list = json.dumps(product_result, indent=4)
        print(formatted_list)
        display_frames(srcs_engine.frame_list)


