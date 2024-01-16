import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('TkAgg')  # 设置Matplotlib的后端为TkAgg
class FrameAnalyzer:
    def __init__(self, video_path, skip_frames=5):
        self.video_path = video_path
        self.skip_frames = skip_frames

    def frame_difference(self, frame1, frame2):
        # 计算两个帧之间的差异
        diff = cv2.absdiff(frame1, frame2)
        non_zero_count = np.count_nonzero(diff)
        normalized_diff = non_zero_count / float(diff.size)
        return normalized_diff

    def analyze_video(self):
        cap = cv2.VideoCapture(self.video_path)
        frame_differences = []

        ret, previous_frame = cap.read()
        if not ret:
            return frame_differences

        frame_index = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 每隔 skip_frames 帧处理一次
            if frame_index % self.skip_frames == 0 and frame_index > 0:
                diff = self.frame_difference(previous_frame, frame)
                frame_differences.append(diff)

            previous_frame = frame
            frame_index += 1

        cap.release()
        return frame_differences

# 设置视频路径
video_path = '../demo/demo.mp4'

# 分析视频
analyzer = FrameAnalyzer(video_path, skip_frames=5)
differences = analyzer.analyze_video()

# 绘制分布图
plt.hist(differences, bins=50, alpha=0.7, color='blue')
plt.title('Frame Differences Distribution')
plt.xlabel('Difference')
plt.ylabel('Frequency')
plt.show()
