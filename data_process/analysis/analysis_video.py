import os
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm
import time


# 定义一个函数来获取视频文件的时长
def get_video_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    duration_seconds = total_frames / frame_rate
    cap.release()
    return duration_seconds


# 设置要分析的文件夹路径
folder_path = '/Volumes/HIKVISION/5666条视频数据'  # 替换为你的文件夹路径

# 初始化一个列表来存储视频文件的时长
durations = []

# 遍历文件夹内的所有文件，并添加进度条
for filename in tqdm(os.listdir(folder_path)):
    if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):  # 支持的视频文件扩展名
        video_path = os.path.join(folder_path, filename)
        duration = get_video_duration(video_path)
        durations.append(duration)

# 统计不同时长的占比
duration_counts = {}
total_videos = len(durations)

for duration in durations:
    duration_int = int(duration)
    if duration_int not in duration_counts:
        duration_counts[duration_int] = 1
    else:
        duration_counts[duration_int] += 1

# 打印占比
while True:
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏，适用于Windows和Unix系统
    print("视频时长占比：")
    for key in sorted(duration_counts.keys()):
        percentage = (duration_counts[key] / total_videos) * 100
        print(f"{key} 秒: {percentage:.2f}%")

    time.sleep(1)  # 每隔1秒更新一次占比
