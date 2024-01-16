#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：video2frame.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/11 19:07

功能：
读取视频，获取所有的帧，时序

'''
import cv2
import os


class VideoAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.frames = []
        self.save_frames_locally = False

    def read_video(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise Exception("Failed to open video file")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self.frames.append(frame)

        cap.release()

    def analyze_video(self):
        total_frames = len(self.frames)
        fps = 0
        if total_frames > 0:
            fps = cv2.VideoCapture(self.video_path).get(cv2.CAP_PROP_FPS)
        total_duration = total_frames / fps if fps > 0 else 0

        print(f"Total Frames: {total_frames}")
        print(f"Total Duration (seconds): {total_duration:.2f}")
        print(f"Frames per Second (FPS): {fps:.2f}")

    def save_frames(self, output_directory):
        if not self.save_frames_locally:
            return

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for i, frame in enumerate(self.frames):
            frame_filename = os.path.join(output_directory, f"frame_{i:04d}.jpg")
            cv2.imwrite(frame_filename, frame)

    def set_save_frames_locally(self, save_frames_locally):
        self.save_frames_locally = save_frames_locally

if __name__ == "__main__":
    video_path = "../../demo/demo.mp4"  # Replace with your video file path
    analyzer = VideoAnalyzer(video_path)

    analyzer.read_video()
    analyzer.analyze_video()

    save_frames_locally = False  # Set to True to save frames locally
    analyzer.set_save_frames_locally(save_frames_locally)

    if save_frames_locally:
        output_directory = "frames_output"
        analyzer.save_frames(output_directory)
        print(f"Frames saved to {output_directory}")
