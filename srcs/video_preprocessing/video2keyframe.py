#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：video2keyframe.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/11 19:07 
'''
import cv2
import numpy as np
import time
class VideoProcessorUpdated:
    def __init__(self, video_path, threshold_ratio):
        self.video_path = video_path
        self.threshold = threshold_ratio
        self.motion_statistics = []
        self.boundaries = [(0.2, 0.8), (0.3, 0.7)]

    def read_video(self):
        print("Opening video...")
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise IOError("Cannot open video")
        print("Video opened successfully.")
        return cap

    def frame_difference(self, frame1, frame2):
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        non_zero_count = np.count_nonzero(diff)
        return non_zero_count

    def crop_image_by_boundaries(self,image):
        # 获取图片尺寸
        height, width, _ = image.shape

        # 计算裁剪的边界
        start_y = int(height * self.boundaries[0][0])
        end_y = int(height * self.boundaries[0][1])
        start_x = int(width * self.boundaries[1][0])
        end_x = int(width * self.boundaries[1][1])

        # 裁剪图片
        cropped_image = image[start_y:end_y, start_x:end_x]

        return cropped_image

    def extract_key_frames(self):
        print("Extracting key frames...")
        cap = self.read_video()
        ret, prev_frame = cap.read()

        if not ret:
            return
        # resize and crop to speed up
        # prev_frame_crop = self.crop_image_by_boundaries(prev_frame)
        #
        # # 获取图片的尺寸
        # height, width = prev_frame_crop.shape[:2]
        #
        # # 计算新的尺寸（原来的一半）
        # new_width = width // 2
        # new_height = height // 2
        #
        # # 使用cv2.resize()缩放图片
        # resized_crop_prev_frame = cv2.resize(prev_frame_crop, (new_width, new_height))


        #############################

        key_frames = []
        frame_count = 0
        while True:
            ret, curr_frame = cap.read()
            if not ret:
                break

            frame_count += 1
            motion = self.frame_difference(prev_frame, curr_frame)
            self.motion_statistics.append(motion)

            if motion > self.threshold:
                print(f"Key frame detected at frame {frame_count}.")
                key_frames.append(curr_frame)
            prev_frame = curr_frame

        print(f"Total number of frames processed: {frame_count}")
        print(f"Number of key frames extracted: {len(key_frames)}")
        print('Key frames ratio:',len(key_frames)/frame_count)
        cap.release()
        return key_frames

    def save_key_frames(self, key_frames, output_folder):
        print(f"Saving key frames to {output_folder}...")
        for i, frame in enumerate(key_frames):
            cv2.imwrite(f"{output_folder}/frame_{i}.jpg", frame)
        print("Key frames saved.")

# Example usage
video_path = "../../demo/demo2.mp4"
threshold = 200000
s1 =time.time()
processor = VideoProcessorUpdated(video_path, threshold)
key_frames = processor.extract_key_frames()
e1 = time.time()
print('Process time:',e1-s1)
processor.save_key_frames(key_frames, "frames_output")


# Note: This code will not run here due to the inability to access external files, but you can run it in your own environment.
