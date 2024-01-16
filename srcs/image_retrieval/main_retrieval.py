#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：main_retrieval.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/12 11:59 

'''

import os
import shutil
import json
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from visualize import ImageDisplayApp
from main_md5_faiss import Retrievaler  # 检索模型，包括建数据库，增量学习，实现检索



class ImageFinder:
    def __init__(self, model_type='holidays'):
        self.project_root = os.getcwd()
        self.model_type = model_type # default
        self.retrievaler = Retrievaler(model_type=model_type)

    def func1(self, img_path,topk=10):
        """


        :param img_path: 图片的绝对路径
        :param topk:
        :return: 返回一个dict，包含前端所需要的所有信息
        """
        if os.path.exists(img_path):
            ret = self.retrievaler.retrieval_one_img(img_path,topk)
            return ret
        else:
            return None

    def choice_one_image(self,idx):
        """
        此功能需要结合前端去实现
        :param idx:
        :return:
        """
        return idx


    def inset(self):
        """
        新增一张图片到样本库
        :return:
        """
        self.retrievaler.insert()

    def create_db(self):
        self.retrievaler.create_db()

    def move_img(self,src_path,dst_path):
        shutil.move(src_path,dst_path) # TODO 1: to Check

# 创建一个列表来保存已选择的图片路径
selected_images = []

def retrieve_image():
    img_path = app.select_image()
    if img_path:
        if img_path not in selected_images:
            selected_images.append(img_path)
            result = finder.func1(img_path=img_path)
            print("Retrieval Result：")
            formatted_dict = json.dumps(result, indent=4, ensure_ascii=False)
            print(formatted_dict)
            app.show_result(result=result['std_result'])

if __name__ == '__main__':
    # 创建 ImageFinder 实例
    finder = ImageFinder(model_type='res50')

    # 创建 tkinter 窗口
    root = tk.Tk()
    app = ImageDisplayApp(root)

    # 创建按钮来触发图像检索
    retrieve_button = tk.Button(root, text="Retrieve Image", command=retrieve_image)
    retrieve_button.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    root.mainloop()

    ###
    # finder = ImageFinder(model_type='res50')
    #
    # # visualize
    # root = tk.Tk()
    # app = ImageDisplayApp(root)
    # img_path = app.select_image()
    #
    # result = finder.func1(img_path=img_path)
    # print("Retrieval Result：")
    # formatted_dict = json.dumps(result, indent=4, ensure_ascii=False)
    #
    # print(formatted_dict)
    #
    #
    # app.show_result(result=result['std_result'])
    # root.mainloop()
    ## test append learning
    # finder.inset()
    ##############################################################

