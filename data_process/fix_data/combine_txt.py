
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：combine_txt.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/15 01:06 
'''
import os
import hashlib
import shutil

from collections import defaultdict
from tqdm import tqdm
from six.moves import cPickle

class FileProcessor:
    def __init__(self, folder_path,fix_results):
        self.folder_path = folder_path
        self.fix_results = fix_results
        self.md5_to_file_count = defaultdict(int)
        self.md5_to_txt_files = defaultdict(list)
    def calculate_md5(self, file_path):
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(8192)  # 以8192字节块读取文件
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()


    def process_files(self):
        if os.path.exists('md5_to_file_count.pkl'):
            self.md5_to_file_count = cPickle.load(open('md5_to_file_count.pkl', "rb", True))
            self.md5_to_txt_files = cPickle.load(open('md5_to_txt_files.pkl', "rb", True))
        else:
            for root, _, files in os.walk(self.folder_path):
                for file in tqdm(files, desc="处理中"):
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                        file_path = os.path.join(root, file)
                        md5 = self.calculate_md5(file_path)
                        self.md5_to_file_count[md5] += 1
                        self.md5_to_txt_files[md5].append(file_path)

            cPickle.dump(self.md5_to_file_count, open('md5_to_file_count.pkl', "wb", True))
            cPickle.dump(self.md5_to_txt_files, open('md5_to_txt_files.pkl', "wb", True))

    def merge_files(self):
        for md5, img_files in tqdm(self.md5_to_txt_files.items(), desc="合并中"):
            merged_txt_filename = f"{md5}.txt"
            merged_image_filename = f"{md5}.jpg"
            if len(img_files) >= 1:
                shutil.copyfile(img_files[0], os.path.join(self.fix_results, 'images', merged_image_filename))
                with open(os.path.join(self.fix_results, 'labels', merged_txt_filename), 'w', encoding='utf-8') as merged_txt_file:
                    for txt_file in img_files:
                        txt_file = txt_file.replace('标注图片','label').replace('.jpg','.txt')
                        with open(txt_file, 'r') as txt_content:
                            merged_txt_file.write(txt_content.read())

if __name__ == "__main__":
    folder_path = '/Volumes/HIKVISION/三批次数据整合-36-for-fix'  # 输入要处理的文件夹路径
    dst_path = '/Volumes/HIKVISION/fix_results2'
    processor = FileProcessor(folder_path,dst_path)
    processor.process_files()
    processor.merge_files()
    print("合并完成！")