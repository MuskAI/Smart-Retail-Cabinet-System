#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System
@File    ：handdet_on_frame.py
@IDE     ：PyCharm
@Author  ：haoran
@Date    ：2024/1/11 21:08

直接从视频中读取能够识别，然后返回这些frame的序号
'''
import os

import cv2
import mediapipe as mp

class HandTracking:
    def __init__(self, video_path, max_hands=5, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands,
                                         min_detection_confidence=min_detection_confidence,
                                         min_tracking_confidence=min_tracking_confidence)

        self.cap = cv2.VideoCapture(video_path)

        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.is_show = True
        self.detected_frame = []

    def process_video(self):
        count = 0

        while self.cap.isOpened():
            count += 1
            ret, frame = self.cap.read()
            if not ret:
                break


            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                # detected hands on frame
                self.detected_frame.append(count)

                for hand_landmarks in results.multi_hand_landmarks:
                    h, w, c = frame.shape
                    landmark_arr = [(int(landmark.x * w), int(landmark.y * h)) for landmark in hand_landmarks.landmark]
                    x_min = min([x for x, y in landmark_arr])
                    x_max = max([x for x, y in landmark_arr])
                    y_min = min([y for x, y in landmark_arr])
                    y_max = max([y for x, y in landmark_arr])

                    pad_w, pad_h = int(0.05 * (x_max - x_min)), int(0.05 * (y_max - y_min))
                    x_min = max(x_min - pad_w, 0)
                    y_min = max(y_min - pad_h, 0)
                    x_max = min(x_max + pad_w, w)
                    y_max = min(y_max + pad_h, h)

                    if self.is_show:
                        self.show_frame(frame,x_min,y_min,x_max,y_max,landmark_arr)

    def show_frame(self, frame,x_min,y_min,x_max,y_max,landmark_arr):
        # 在帧上绘制边界框
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # 在帧上绘制关键点
        for x, y in landmark_arr:
            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)

        cv2.imshow('Hand Tracking', frame)
        key = cv2.waitKey(100)  # 1 millisecond
        if key == 27:  # Press 'Esc' to exit
            self.release()


    def release(self):
        self.cap.release()



if __name__ == "__main__":
    video_dir = '/Volumes/HIKVISION/5666条视频数据'
    video_list = os.listdir(video_dir)
    for idx,item in enumerate(video_list):
        video_path = os.path.join(video_dir,item)
        file_size = os.path.getsize(video_path)
        print('Size of '+video_path+'is',file_size)
        if file_size / (1024 * 1024) < 3:
            pass
        else:
            continue
        hand_tracker = HandTracking(video_path)
        hand_tracker.process_video()
        print(hand_tracker.detected_frame) #detected num frames
        hand_tracker.release()
