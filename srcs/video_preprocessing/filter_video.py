#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：filter_video.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/15 11:32 
'''
import cv2
import os

class VideoFilter:
    def __init__(self, input_folder, output_folder, max_duration_seconds):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.max_duration_seconds = max_duration_seconds

    def filter_videos(self):
        # 创建输出文件夹
        os.makedirs(self.output_folder, exist_ok=True)

        for root, _, files in os.walk(self.input_folder):
            for file in files:
                if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv')):
                    input_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(self.output_folder, file)

                    cap = cv2.VideoCapture(input_file_path)
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration_seconds = frame_count / fps

                    if duration_seconds <= self.max_duration_seconds:
                        # 复制视频文件到输出文件夹
                        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                        os.system(f'cp "{input_file_path}" "{output_file_path}"')
                        print(f"过滤视频：{file}")

if __name__ == "__main__":
    input_folder = '/path/to/input_folder'  # 输入视频文件夹路径
    output_folder = '/path/to/output_folder'  # 输出视频文件夹路径
    max_duration_seconds = 600  # 最大允许的视频时长（秒）

    filter_instance = VideoFilter(input_folder, output_folder, max_duration_seconds)
    filter_instance.filter_videos()
