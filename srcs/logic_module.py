#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：logic_module.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/13 11:25

利用传统算法，统计underline所在区域的信息，来获取手或商品进出的逻辑判断
'''
from inference_onnx import UnderlineInfer
import cv2
import os,time
import numpy as np
class LogicalModule:
    def __init__(self, engine):
        self.infer_engine = engine
        self.first_bbox = None
        self.stable_bbox = None
        self.bboxes_per_frame = []
        self.k = 5
        self.stable_k = (3,8)


    def method1(self):
        """
        利用Underline模型获取bbox区域，对区域进行一定程度的pad，然后统计像素特征等图像特征
        :return:
        """
        pass

    def method2(self):
        pass

    @staticmethod
    def crop_image_with_padding(image, coordinates, x_pad=0, y_pad=0):
        try:
            x1, y1, x2, y2 = coordinates
            h, w = image.shape[:2]

            # 计算裁剪区域的坐标
            crop_x1 = max(x1 - x_pad, 0)
            crop_y1 = max(y1 - y_pad, 0)
            crop_x2 = min(x2 + x_pad, w)
            crop_y2 = min(y2 + y_pad, h)

            # 进行裁剪，并确保裁剪区域不会超出图像边界
            cropped_image = image[crop_y1:crop_y2, crop_x1:crop_x2]

            return cropped_image
        except Exception as e:
            print(f"图像裁剪失败：{str(e)}")
            return None

    def average_bboxes(self):
        bboxes = self.bboxes_per_frame
        k = self.k
        if k <= 0 or k > len(bboxes):
            return None  # 处理无效的k值

        # 初始化平均bbox的坐标
        avg_x1, avg_y1, avg_x2, avg_y2 = 0, 0, 0, 0

        # 计算前k个bbox的坐标总和
        for i in range(k):
            bbox = bboxes[i]
            x1, y1, x2, y2 = bbox
            avg_x1 += x1
            avg_y1 += y1
            avg_x2 += x2
            avg_y2 += y2

        # 计算坐标平均值
        avg_x1 /= k
        avg_y1 /= k
        avg_x2 /= k
        avg_y2 /= k
        avg_x1, avg_y1, avg_x2, avg_y2 = map(int,[avg_x1, avg_y1, avg_x2, avg_y2])
        return [avg_x1, avg_y1, avg_x2, avg_y2]

    def compute_and_display_grayscale_histogram(self,image, num_bins=256):
        try:
            # 读取灰度图像
            image_gray = cv2.cvtColor(image,cv2.IMREAD_GRAYSCALE)


            # 计算直方图
            histogram = cv2.calcHist([image_gray], [0], None, [num_bins], [0, 256])

            # 创建一个空白图像来绘制直方图
            hist_image = np.zeros((256, 256, 3), dtype=np.uint8)

            # 标准化直方图数据
            cv2.normalize(histogram, histogram, 0, 255, cv2.NORM_MINMAX)

            # 绘制直方图
            for i in range(1, num_bins):
                cv2.line(hist_image, (i - 1, 255 - int(histogram[i - 1])), (i, 255 - int(histogram[i])), (255, 255, 255), 2)

            # 创建一个窗口并显示直方图
            cv2.namedWindow("Grayscale Histogram", cv2.WINDOW_NORMAL)
            cv2.imshow("Grayscale Histogram", hist_image)
            # cv2.waitKey(100)
            # cv2.destroyAllWindows()

        except Exception as e:
            print(f"计算和显示灰度直方图失败：{str(e)}")

if __name__ == '__main__':
    model_path_product = "model_zoo/underline-yolov3-mobv2.onnx"
    inference_engine = UnderlineInfer(model_path_product)
    video_dir = '/Users/musk/Desktop/智能售货柜/测试视频'
    video_list = os.listdir(video_dir)
    all_list = []
    logical_module = LogicalModule(inference_engine)
    cv2.namedWindow('Show')

    for idx, video_path in enumerate(video_list):
        video_path = os.path.join(video_dir, video_path)
        ###
        video = cv2.VideoCapture(video_path)
        # 循环直到视频结束
        pixel_sum_list = []
        only_one_flag = True
        stable_bbox = None
        count_frame = 0
        while video.isOpened():
            count_frame +=1
            # 读取下一帧
            ret, frame = video.read()

            # 如果正确读取帧，ret为True
            if not ret:
                print("无法读取视频，或视频播放完毕")
                break

            # img = cv2.imread(image_path)
            img = frame
            if img is None:
                continue
            # 将图像从BGR转换为RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 检查是否成功读取图像
            if img is None:
                # print(f"无法读取图像文件：{image_path}")
                continue
            # 检查图像通道数
            if img.shape[2] == 4:
                # 将四通道图像转换为三通道
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            input_data = np.array(img)

            s1 = time.time()
            ret = inference_engine.infer(input_data)
            ret = inference_engine.filter_result(ret)
            ret = inference_engine.resize_and_map_coordinates_with_clipping(ret)

            e1 = time.time()
            print('Underline detection model Inference time:', e1 - s1)
            if ret is not None:
                if count_frame >  logical_module.stable_k[0]:
                    logical_module.bboxes_per_frame.append(ret[0][:-1])
                    first_frame_bbox = logical_module.bboxes_per_frame[0]

                if len(logical_module.bboxes_per_frame) > logical_module.stable_k[1]:
                    if only_one_flag:
                        stable_bbox = logical_module.average_bboxes()
                        only_one_flag = False
                    # print('Stable,',stable_bbox)
                    crop_ret = logical_module.crop_image_with_padding(frame, stable_bbox,x_pad=500,y_pad=10)

                    if crop_ret is not None:
                        cv2.imshow('Show',crop_ret)
                        logical_module.compute_and_display_grayscale_histogram(crop_ret)
                        cv2.waitKey(100)

        all_list.append(pixel_sum_list)
        # 释放视频对象
        video.release()

