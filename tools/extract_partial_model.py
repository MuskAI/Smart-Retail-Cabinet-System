#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：cxy 
@File    ：extract_partial_model.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2023/4/30 14:19 
'''
import onnx
# neck/gap/GlobalAveragePool_output_0
# onnx.utils.extract_model('original_end2end.onnx', 'small_partial_model.onnx', ['input'], ['/head/layers.0/act/Mul_output_0'])

onnx.utils.extract_model('../srcs/model_zoo/res50_36cls.onnx', '../srcs/model_zoo/res50_36cls_part.onnx', ['input'], ['onnx::Flatten_493'])
