#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：inference_onnx.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/12 14:00

读取onnx模型，进行推理，得到结果
'''
import os

import onnxruntime
import numpy as np
import time
import cv2
from PIL import Image
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')


class ONNXInference:
    def __init__(self, model_path='', input_data_size=None, norm=True):
        self.model_path = model_path
        self.session = onnxruntime.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        self.inference_result = None
        self.norm = norm
        self.image = None
        self.image_size = None
        if input_data_size is None:
            raise ValueError('input_data_size is None, Please specify it')
        self.input_data_size = input_data_size  # onnx required input_data_size

    def normalize(self, img):
        """

        :param img: (w,h,c)
        :return:
        """
        # TODO: implement normalize methode
        # 给定均值和方差
        _mean = np.array([123.675, 116.28, 103.53])
        _std = np.array([58.395, 57.12, 57.375])
        # 归一化操作
        _normalized_image = (img - _mean) / _std
        return _normalized_image

    def infer(self, image):
        """
        :param image: numpy array
        :return: detection result of this image (after resize)
        """
        # Ensure input_data is a numpy array
        if not isinstance(image, np.ndarray):
            raise ValueError("Input data must be a numpy array")
        self.image = image

        self.image_size = image.shape[:-1]  # width and height
        ####### resize image######
        if self.image_size != self.input_data_size:
            image = Image.fromarray(image.astype('uint8'))
            image = image.resize((self.input_data_size[1],self.input_data_size[0]))
            image = np.array(image)

        #########################

        if self.norm:
            normalized_image = self.normalize(image)

        if len(image.shape) == 4:
            pass
        else:
            input_data = normalized_image[np.newaxis, :, :, :].transpose(0, 3, 1, 2)

        # Perform inference
        input_data = input_data.astype(np.float32)
        result = self.session.run([self.output_name], {self.input_name: input_data})
        self.inference_result = result[0]
        return self.inference_result

    @abstractmethod
    def filter_result(self):
        pass

    def resize_and_map_coordinates_with_clipping(self, detected_coordinates):
        """
        将检测到的坐标映射回原始图像的函数，并进行截断处理

        参数：
        original_shape：原始图像的形状，如(Height, Width)。
        target_shape：目标图像的形状，如(Resized_Height, Resized_Width)。
        detected_coordinates：检测到的坐标列表，每个坐标为(x1, y1, x2, y2)，表示矩形左上角和右下角的坐标。

        返回：
        mapped_coordinates：映射回原始图像的坐标列表，每个坐标为(x1, y1, x2, y2)。
        """
        if detected_coordinates is None:
            return None
        if isinstance(detected_coordinates, np.ndarray):
            detected_coordinates = detected_coordinates.tolist()
        original_shape = self.image_size
        target_shape = self.input_data_size

        original_height, original_width = original_shape
        target_height, target_width = target_shape

        # 计算高度和宽度的比例
        height_ratio = original_height / target_height
        width_ratio = original_width / target_width

        mapped_coordinates = []
        clipped_coordinates = []

        for bbox_conf in detected_coordinates:
            x1, y1, x2, y2, conf  = map(float,bbox_conf)
            # 将目标图像中的坐标映射回原始图像
            original_x1 = int(x1 * width_ratio)
            original_y1 = int(y1 * height_ratio)
            original_x2 = int(x2 * width_ratio)
            original_y2 = int(y2 * height_ratio)

            # 截断处理坐标，确保它们在原始图像边界内
            original_x1 = max(0, min(original_x1, original_width - 1))
            original_y1 = max(0, min(original_y1, original_height - 1))
            original_x2 = max(0, min(original_x2, original_width - 1))
            original_y2 = max(0, min(original_y2, original_height - 1))

            mapped_coordinates.append((original_x1, original_y1, original_x2, original_y2,conf))

            # 如果坐标被截断，记录到截断坐标列表中
            if (x1 != original_x1 or y1 != original_y1 or x2 != original_x2 or y2 != original_y2):
                clipped_coordinates.append((x1, y1, x2, y2))

            # 打印报告，指示哪些坐标已被截断
            if clipped_coordinates:
                print(f"以下坐标已被截断：{clipped_coordinates}")

        return mapped_coordinates


class ProductInfer(ONNXInference):
    def __init__(self, model_path):
        super().__init__(model_path, norm=True, input_data_size=(256, 416))
        self.threshold = 0.4

    def filter_result(self, detections):
        """
        filter detection result by threshold
        :return:
        """
        if detections is None:
            raise Exception('inference_result is None')

        filtered_result = []
        for detection in detections[0]:
            if detection[4] > self.threshold:  # 过滤掉置信度较低的检测结果
                filtered_result.append(detection)
            else:
                pass
        if len(filtered_result) == 0:
            return None
        else:
            return np.array(filtered_result)

    @staticmethod
    def visualize_result(detections, image):
        # 遍历检测结果并在图像上绘制边界框和标签
        detected_flag = False  # 处理没检测到目标的情况
        # 将图像从BGR转换为RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        for detection in detections:
            if detection[4] > 0.01:  # 过滤掉置信度较低的检测结果
                detected_flag = True
                x1, y1, x2, y2, confidence = detection
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                label = 'product'  # 类别标签

                # 在图像上绘制边界框
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 使用绿色绘制边界框
                # 在图像上绘制类别标签
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # 使用红色绘制标
        if detected_flag:
            # 显示带有边界框和标签的图像
            cv2.imshow("Detection Result", image)
            cv2.waitKey(100)
            cv2.destroyAllWindows()



class UnderlineInfer(ONNXInference):
    def __init__(self, model_path):
        super().__init__(model_path, norm=True, input_data_size=(256, 416))
        self.threshold = 0.4

    def filter_result(self, detections):
        """
        filter detection result by threshold
        :return:
        """
        if detections is None:
            raise Exception('inference_result is None')

        filtered_result = []
        for detection in detections[0]:
            if detection[4] > self.threshold:  # 过滤掉置信度较低的检测结果
                filtered_result.append(detection)
            else:
                pass
        if len(filtered_result) == 0:
            return None
        else:
            return np.array(filtered_result)

    @staticmethod
    def visualize_result(detections, image):
        # 遍历检测结果并在图像上绘制边界框和标签
        detected_flag = False  # 处理没检测到目标的情况
        # 将图像从BGR转换为RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        for detection in detections:
            if detection[4] > 0.01:  # 过滤掉置信度较低的检测结果
                detected_flag = True
                x1, y1, x2, y2, confidence = detection
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                label = 'underline'  # 类别标签

                # 在图像上绘制边界框
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 使用绿色绘制边界框
                # 在图像上绘制类别标签
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # 使用红色绘制标
        if detected_flag:
            # 显示带有边界框和标签的图像
            cv2.imshow("Detection Result", image)
            cv2.waitKey(100)
            # cv2.destroyAllWindows()


# Example usage:
if __name__ == "__main__":
    model_path_underline = "model_zoo/underline-yolov3-mobv2.onnx"  # Replace with your ONNX model file path
    model_path_product = "model_zoo/products-yolov3-mobv2.onnx"
    inference_engine = UnderlineInfer(model_path_underline)
    inference_engine = ProductInfer(model_path_product)
    img_dir = '/Volumes/HIKVISION/三批次里取有用的/标注图片'
    img_list = os.listdir(img_dir)
    for idx, image_path in enumerate(img_list):
        image_path = os.path.join(img_dir, image_path)
        img = cv2.imread(image_path)
        if img is None:
            continue
        # 将图像从BGR转换为RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 检查是否成功读取图像
        if img is None:
            print(f"无法读取图像文件：{image_path}")
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
            inference_engine.visualize_result(ret, img)
