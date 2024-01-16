#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：video_to_frame.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/9 16:20 
'''
import cv2
import os
from tqdm import tqdm
import numpy as np

class FrameExtractor:
    def __init__(self, data_root, show_frames=False, time_threshold=10, blur_threshold=100.0, skip_frames=5):
        self.data_root = data_root
        self.show_frames = show_frames
        self.time_threshold = time_threshold
        self.blur_threshold = blur_threshold
        self.skip_frames = skip_frames  # 每隔几帧处理一次

    def is_blurry(self, frame, mask):
        # 使用拉普拉斯算子计算图像的方差
        laplacian_var = cv2.Laplacian(frame, cv2.CV_64F).var()
        return laplacian_var < self.blur_threshold

    def extract_frames_by_frame_difference(self, threshold=20, dst_dirs='frames_by_frame_difference'):
        # 确保目标目录存在
        if not os.path.exists(dst_dirs):
            os.makedirs(dst_dirs)

        # 遍历 data_root 下的所有视频文件
        for root, dirs, files in os.walk(self.data_root):
            for file in tqdm(files, desc="Processing Videos"):
                video_path = os.path.join(root, file)
                if not video_path.endswith('.mp4'):  # 只处理 mp4 视频文件
                    continue

                cap = cv2.VideoCapture(video_path)
                fgbg = cv2.createBackgroundSubtractorKNN()  # 使用KNN背景减法

                fps = cap.get(cv2.CAP_PROP_FPS)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = total_frames / fps

                if duration > self.time_threshold:
                    print(f"Skipping video {file}: Duration {duration:.2f}s exceeds threshold.")
                    cap.release()
                    continue

                frame_index = 0
                key_frame_count = 0

                ret, previous_frame = cap.read()
                if not ret:
                    continue

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # 每隔 skip_frames 帧处理一次
                    if frame_index % self.skip_frames != 0:
                        frame_index += 1
                        continue

                    fgmask = fgbg.apply(frame)
                    _, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)
                    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    if contours:  # 仅当存在轮廓时才检查模糊度
                        motion_masks = [np.zeros_like(fgmask) for _ in contours]
                        for i, contour in enumerate(contours):
                            cv2.drawContours(motion_masks[i], [contour], -1, 255, -1)

                        for motion_mask in motion_masks:
                            if not self.is_blurry(frame, motion_mask):
                                if self.show_frames:
                                    cv2.imshow("Key Frame", frame)
                                    cv2.waitKey(1)

                                frame_filename = os.path.join(dst_dirs, f"{file}_frame_diff_frame_{frame_index:04d}.png")
                                cv2.imwrite(frame_filename, frame)
                                key_frame_count += 1
                                break

                    frame_index += 1

                cap.release()
                cv2.destroyAllWindows()
                print(f"{file}: Total frames = {frame_index}, Key frames = {key_frame_count}, Ratio = {key_frame_count/frame_index:.2f}")

# 使用示例
data_root = '/Users/musk/Desktop/智能售货柜/测试视频'
dst_dirs = '/Users/musk/Desktop/智能售货柜/视频测试结果'
frame_extractor = FrameExtractor(data_root, show_frames=True, time_threshold=10, blur_threshold=100.0, skip_frames=2)
frame_extractor.extract_frames_by_frame_difference(dst_dirs=dst_dirs,threshold=4)


