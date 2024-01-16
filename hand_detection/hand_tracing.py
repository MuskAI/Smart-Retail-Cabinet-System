#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：hand_tracing.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/8 12:22 
'''
import cv2
import math
import time
import mediapipe as mp
from os import listdir

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 调用mediapipe库中的Hand函数，这个函数就可以识别手部
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("没有图像")
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    # result是调用hands函数得到的结果，里面包含了手的各点坐标，通过results.multi_hand_landmarks调用
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        # 得到results.multi_hand_landmarks中所有点的坐标，并进行绘制
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('result', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cv2.destroyAllWindows()
hands.close()
cap.release()
