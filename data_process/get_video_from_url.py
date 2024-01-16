#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：get_video_from_url.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/9 13:34

功能：
1. 拿到客户给的excel文件，自动下载并分类里面的video

'''
import os
import requests
from tqdm import tqdm
import pandas as pd

class VideoProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.excel_data = pd.read_excel(file_path)

    def create_product_video_dict(self):
        """
        This function takes a dataframe with product information and returns a dictionary.
        Each key in the dictionary is a unique product name, and the value is a list of corresponding '头部视频' links.
        """
        product_videos_dict = self.excel_data.groupby('产品名称')['侧面视频'].apply(list).to_dict()
        return product_videos_dict

    def download_videos(self, product_videos_dict, dst_dir):
        """
        Download videos based on the provided URL in the product_videos_dict and save them in dst_dir.
        Each key in the dictionary is considered as a folder name where the videos will be saved.
        """
        for product, videos in product_videos_dict.items():
            product_dir = os.path.join(dst_dir, str(product))
            os.makedirs(product_dir, exist_ok=True)

            for idx, video_url in enumerate(videos):
                # Assuming the video URLs are valid and accessible
                if pd.isna(video_url):
                    continue
                video_filename = f"{product}_video_{idx}.mp4"
                video_path = os.path.join(product_dir, video_filename)

                # Download video from URL with progress bar
                response = requests.get(video_url, stream=True)
                total_size_in_bytes = int(response.headers.get('content-length', 0))
                block_size = 1024  # 1 Kibibyte

                progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
                with open(video_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
                    progress_bar.close()

                print(f"视频 '{video_filename}' 已下载至 '{product_dir}'")

# Example usage
file_path = '/Users/musk/Desktop/智能售货柜/产品视频资料2.1.xlsx'
video_processor = VideoProcessor(file_path)
product_videos = video_processor.create_product_video_dict()

destination_directory = '/Volumes/HIKVISION/侧面视频下载'
video_processor.download_videos(product_videos, destination_directory)
