#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：hand_detection_v2.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/9 19:19 
'''
import cv2
import mediapipe as mp
from tqdm import tqdm

# 初始化 MediaPipe 手部模型
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=5, min_detection_confidence=0.3, min_tracking_confidence=0.3)

option = input("Choose an option:\n1. Read from camera\n2. Read from video file\n")

if option == '1':
    # 从摄像头读取
    cap = cv2.VideoCapture(0)
    # 设置摄像头的分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
elif option == '2':
    # 从视频文件读取
    video_path = '../demo/demo2.mp4'  # 你可以更改为实际的视频文件路径
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        exit()
else:
    print("Invalid option. Please choose 1 or 2.")
    exit()

# 获取视频帧总数（仅对视频文件有效）
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if option == '2' else 0

# 创建进度条
progress_bar = tqdm(total=frame_count, desc='Processing Frames', unit='frame')

while cap.isOpened():
    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        break

    # 将BGR图像转换为RGB图像
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 进行手部关键点检测
    results = hands.process(rgb_frame)

    # 获取关键点结果
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 获取手部关键点的边界框坐标
            h, w, c = frame.shape
            landmark_arr = [(int(landmark.x * w), int(landmark.y * h)) for landmark in hand_landmarks.landmark]
            x_min = min([x for x, y in landmark_arr])
            x_max = max([x for x, y in landmark_arr])
            y_min = min([y for x, y in landmark_arr])
            y_max = max([y for x, y in landmark_arr])

            # 添加Padding，例如5%的边界框宽度和高度
            pad_w, pad_h = int(0.05 * (x_max - x_min)), int(0.05 * (y_max - y_min))
            x_min = max(x_min - pad_w, 0)
            y_min = max(y_min - pad_h, 0)
            x_max = min(x_max + pad_w, w)
            y_max = min(y_max + pad_h, h)

            # 绘制边界框
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # 在图像上绘制关键点
            for x, y in landmark_arr:
                cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)

    # 显示结果
    cv2.imshow("Hand Tracking", frame)

    # 更新进度条
    progress_bar.update(1)

    # 退出条件
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
