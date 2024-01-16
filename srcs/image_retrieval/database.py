#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：database.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/12 11:55

检索数据库管理 beta2.0
'''

import cv2
import faiss
import pandas as pd
import os, shutil, sys

sys.path.append('./apis')
sys.path.append('./image_retrieval/apis')
from pprint import pprint
from hashlib import md5
import numpy as np
import time
import sys
from six.moves import cPickle
from infer_faiss import infer
from tqdm import tqdm

sys.path.append('../')
from feat_extractor import FeatExtractor

from abc import abstractmethod


class Database(object):
    """
    1. 创建数据库
    2. 连接数据库
    3. 增删改查接口

    增加恢复出厂设置的功能
    """

    def __init__(self, cache_dir='cache', model_type='',
                 model_path=''):

        ###### check #######

        if not os.path.exists(cache_dir):
            raise FileExistsError('错误：输入的文件夹路径不存在！\n:', cache_dir)
        if not os.path.exists(cache_dir):
            raise FileExistsError('错误：输入的文件夹路径不存在！\n:', model_path)
        assert model_type in ('res50', '')

        ##################


        self.cache_dir = cache_dir
        self.model_type = model_type
        self.pick_layer = 'AveragePooling'
        sample_cache = '{}-{}-{}'.format(self.model_type, self.pick_layer, 'md5')
        initial_sample_cache = '{}-{}-{}'.format(self.model_type, self.pick_layer, 'md5-initial')

        # 各种路径问题，全部转为绝对路径
        self.db_path = os.path.join(self.cache_dir, sample_cache)
        self.proj_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.samples = None
        self.sample_cache = sample_cache
        self.initial_sample_cache = initial_sample_cache
        self.model_path = model_path

        self.feat_dim = 2048
        # faiss index
        self.index = faiss.IndexFlatIP(self.feat_dim)

    def create_db(self, img_dir=''):
        """
          如果数据库文件存在，则不再重新创建，对于需要增删的需求，需要通过增删改查的接口实现
          如果希望重新创建数据库文件，则需要删除原数据库文件
          会保存第一次create db 时的状态

        """
        if not os.path.exists(img_dir):
            raise FileExistsError('错误：输入的文件夹路径不存在！\n:', img_dir)
        self.img_dir = img_dir
        db_path = self.db_path
        if os.path.exists(db_path):
            print('数据库已经存在')
            return None
        else:
            # 导入模型
            method = FeatExtractor(model_path=self.model_path)

            samples = []
            # 开始遍历图片
            for root, _, files in tqdm(os.walk(img_dir, topdown=False)):
                cls = root.split('/')[-1]
                for name in tqdm(files):
                    if not name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                        continue
                    # if not name.endswith('.png') and not name.endswith('.jpg'):
                    #     continue
                    img = os.path.join(root, name)

                    # 开始编码
                    md5_code, new_path = self.get_md5(img_path=img)


                    if new_path is None:
                        pass
                    else:
                        img = new_path

                    query = method.make_single_sample(img, verbose=False, md5_encoding=False)

                    # 开始构建数据库中的项
                    sample = {
                        'md5': md5_code,
                        'img': img if new_path is None else new_path ,
                        'cls': cls,
                        'hist': query['hist'],
                        'data_type': 0,  # 0 is system data , 1 is user data
                        'error_times': 0  # 出错次数，默认为0
                    }
                    samples.append(sample)

            # 保存数据库文件
            cPickle.dump(samples, open(os.path.join(self.cache_dir, self.initial_sample_cache), "wb", True))
            cPickle.dump(samples, open(os.path.join(self.cache_dir, self.sample_cache), "wb", True))

    def connect_db(self):
        # 如果有数据库文件直接load
        samples = cPickle.load(open(self.db_path, "rb", True))

        for sample in samples:
            # sample['hist'] /= np.sum(sample['hist'])  # normalize
            sample['hist'] = sample['hist'] / np.linalg.norm(sample['hist'])

        self.samples = samples

        # 对samples进行检查
        if len(self.samples) == 0:
            raise '您的样本库为空，请删除数据库文件后重新构建'

        # 同时创建faiss index
        self.__create_index()

    def get_md5(self, img_path):
        """
        对图片进行md5编码，编码成功则返回str，失败则返回None
        Args:
            img_path: [str] 需要编码图片的地址

        """
        assert os.path.isfile(img_path)

        try:
            name = img_path.split('/')[-1]
            new_path = None
            if 'md5' in name:
                # 如果编码已经在文件名中，则可以直接从图片名称中获得编码
                md5_code = name.split('-')[-1].split('.')[0]

            else:
                with open(img_path, 'rb') as img:
                    md5_code = md5(img.read()).hexdigest()
                    new_path = os.path.join(img_path.replace(name, ''),
                                            '{}-md5-{}.{}'.format(name.split('.')[0], md5_code,
                                                                  name.split('.')[-1]))
                    os.rename(img_path, new_path)

        except Exception as e:
            return None

        return md5_code, new_path

    def insert(self, img_path_list=[], img_label_list=[]):
        """
        实现增量学习，在数据库中增加新的特征
        有两种方式实现:1.输入对应图片地址和其类别标签 2. 自动检查需要增加的图片  默认使用第二种方式
        Args:
            img_path_list : 图片路径列表 e.g.['./test.jpg','./demo.png']
        """
        assert self.samples, 'connect to db error'
        walk_time = 0
        encode_time = 0
        check_duplicate_time = 0
        s1 = time.time()

        # 使用默认的方式开始增量学习
        img_info_list = []
        if len(img_path_list) == 0 or len(img_label_list) == 0:
            # 开始遍历图片，数据库
            for root, _, files in tqdm(os.walk(self.img_dir, topdown=False)):
                s2 = time.time()
                cls = root.split('/')[-1]
                for name in files:
                    if not name.endswith('.png') and not name.endswith('.jpg'):
                        continue
                    walk_time += (time.time() - s2)
                    img = os.path.join(root, name)

                    # 开始编码, 修改这里还可以提速
                    s3 = time.time()
                    md5_code, _ = self.get_md5(img_path=img)
                    encode_time += (time.time() - s3)

                    img_info_list.append({
                        'md5': md5_code,
                        'img': img,
                        'cls': cls,
                    })

            # 检查重复项

            s4 = time.time()

            diffs = self.check_duplicate(samples=self.samples, img_info_list=img_info_list)
            check_duplicate_time = time.time() - s4
            # 生成需要新增的图片列表
            img_path_list = [i['img'] for i in diffs['insert']]
            img_label_list = [i['cls'] for i in diffs['insert']]

        s5 = time.time()
        method = FeatExtractor(model_path=self.model_path)
        load_mode_time = time.time() - s5

        s6 = time.time()
        for idx, item in enumerate(img_path_list):
            # 首先判断路径是否存在
            if os.path.isfile(item):
                # 开始增量学习
                query = method.make_single_sample(d_img=item)
                # 增加到数据库
                sample = {
                    'md5': self.get_md5(item),
                    'img': item,
                    'cls': img_label_list[idx],
                    'hist': query['hist'],
                    'data_type': 1,  # 0 is system data , 1 is user data
                    'error_times': 0  # 出错次数，默认为0
                }
                self.samples.append(sample)
        study_time = time.time() - s6
        # 如果有修改则重新保存数据库
        s7 = time.time()
        if len(img_label_list) != 0 and len(img_label_list) != 0:
            cPickle.dump(self.samples, open(self.db_path, "wb", True))
            print('增量学习成功！数据库已更新！')
        save_time = time.time() - s7
        total_time = time.time() - s1
        print('总用时{:.5f}\n遍历循环用时{:.5f}\n编码用时{:.5f}\n'
              '集合差集用时{:.5f}\n加载模型用时{:.5f}\n增量学习用时{:.5f}\n保存文件用时{:.5f}\n'.format(total_time,
                                                                                walk_time, encode_time,
                                                                                check_duplicate_time, load_mode_time,
                                                                                study_time, save_time))

    def check_duplicate(self, samples, img_info_list):
        """
        通过文件目录与数据库中对比,找出多余的，和缺失的项

        Args:
             samples: 数据库，是一个list
             img_info_list:获取图片文件夹的信息

        }]
        """
        img_md5_list = [i['md5'] for i in img_info_list]
        img_md5_set = set(img_md5_list)
        samples_md5_list = [i['md5'] for i in samples]
        samples_md5_set = set(samples_md5_list)

        # 求两个集合的交、差集
        c_s = list(img_md5_set.difference(samples_md5_set))  # csv_set - samples_set 新增的数据
        s_c = list(samples_md5_set.difference(img_md5_set))  # samples_set - csv_set 删除的数据

        # 需要添加的图片信息
        insert_list = []
        for i in c_s:
            insert_list.append({
                'md5': img_info_list[img_md5_list.index(i)]['md5'],
                'img': img_info_list[img_md5_list.index(i)]['img'],
                'cls': img_info_list[img_md5_list.index(i)]['cls'],
            })

        # 从samples中找出需要删除的信息
        del_list = []
        for i in s_c:
            del_list.append(samples[samples_md5_list.index(i)])

        diffs = {
            'insert': insert_list,
            'del': del_list
        }
        return diffs

    def delete(self, type='image', key=None, del_numk=0):
        """
        可以根据两种方式删除：
        1. md5码，输入要删除图片的md5，删除样本库中对应的特征
        2. 根据易混淆特征删除，实现删除与输入图片相对应的易混淆特征，比如输入是苹果，而苹果经常被错识别成土豆，
        那么就输入苹果从而在样本库中删除土豆。默认苹果的top1 distance是需要删除的。

        Args:
            type: 需要通过何种方式查询
            key:查询的key，比如type为md5 则key就是md5码，type为image，key就是图片路径
            del_numk:仅仅在key=image的时候才会被使用，删除第几个，默认第一个为易混淆的特征，

        """
        assert type in ('hist', 'md5', 'image', 'cls'), 'Not support type {} at this time'.format(type)

        # 记录一些删除前的状态
        len_samples = len(self.samples)
        all_cls = []

        # 如果type 是 md5 或者hist
        if type == 'hist' or type == 'md5':
            # 找到要删除的索引和内容
            index, sample = self.find(find_key=key, type=type)

        elif type == 'image':
            std_results = self.find(find_key=key, type=type)
            if len(std_results) > del_numk:
                del_md5 = std_results[del_numk]['md5']
                index, sample = self.find(find_key=del_md5, type='md5')
            else:
                print('从数据库中删除特征失败！')
        # 删除整个类别
        elif type == 'cls':
            # 在通过类别删除的时候就不需要find,可以输入'youzi'或['youzi','apple']
            assert isinstance(key, (list, str))  # 暂时只支持通过'apple' or ['apple','garbage]的方式进行修改
            if isinstance(key, str):
                key = [key]
            for idx, k_item in enumerate(self.samples[::-1]):
                all_cls.append(k_item['cls'])
                if k_item['cls'] in key:
                    self.samples.remove(k_item)  # 删除
            all_cls = set(all_cls)

        if type != 'cls' and index == None:
            return
        try:
            if type != 'cls':
                _sample = self.samples.pop(index)
            else:
                _sample = key
            # TODO 确认是要删除的内容
            if len(self.samples) < len_samples:
                # 保存数据库文件
                sample_cache = '{}-{}-{}'.format(self.RES_model, self.pick_layer, 'md5')
                cPickle.dump(self.samples, open(os.path.join(self.cache_dir, sample_cache), "wb", True))

                print('成功从数据库中删除特征 {}'.format(_sample))
            elif len(self.samples) == len_samples and type == 'cls':
                print('删除失败!，{}类别不在数据库中，请重新输入'.format(key))
                print('数据库中的类别为：', all_cls)


        except Exception as e:
            print('从数据库中删除特征失败！')

    def update(self):
        pass

    def find(self, find_key, type='hist'):
        """
        集成各种在数据库查找的功能,返回的是在samples中的index 和 内容
        """
        assert type in ('hist', 'md5', 'image', 'cls'), 'Not support type {} at this time'.format(type)
        assert self.samples is not None, 'Please connect db before you using it.'
        index = None
        # 如果是根据特征查找
        try:
            if type == 'hist':
                _ = [i['hist'] for i in self.samples]
                index = _.index(find_key)

            elif type == 'md5':
                _ = [i['md5'] for i in self.samples]
                index = _.index(find_key)
            elif type == 'image':
                assert os.path.isfile(find_key), '{} is not exist!'.format(find_key)
                method = FeatExtractor(model_path=self.model_path)
                query = method.make_single_sample(find_key, verbose=False, md5_encoding=False)

                # parameters
                topd = 10
                topk = 3
                d_type = 'd1'  # distance type  you can choose 'd1 , d2 , d3  ... d8' and 'cosine' and 'square'
                top_cls, result, std_result = infer(query, samples=self.samples, depth=topd, d_type=d_type, topk=topk,
                                                    thr=1)
                return std_result
            elif type == 'cls':
                # 由于赶时间，先不考虑效率实现
                results = []
                for idx, item in enumerate(self.samples):
                    if item['cls'] == find_key:
                        results.append(item)
                return results
            else:
                pass
        except:
            print('未找到要删除的特征，或已被删除')

        if index is not None:
            return index, self.samples[index]
        else:
            return None, None

    def get_samples(self):
        return self.samples

    def recover_db(self):
        """
        恢复出厂设置
        """
        sample_cache = os.path.join(self.cache_dir, self.sample_cache)
        initial_sample_cache = os.path.join(self.cache_dir, self.initial_sample_cache)
        assert os.path.exists(initial_sample_cache), '初始状态数据库文件不存在，无法恢复出厂设置'

        # 如果可学习样本库文件存在，则进行替换
        if os.path.exists(sample_cache):
            # 删除原本的
            os.remove(sample_cache)
            # 复制新的
            shutil.copy(initial_sample_cache, sample_cache)
        else:
            # 如果可学习样本库文件不存在，则进行创建
            shutil.copy(initial_sample_cache, sample_cache)

        print('恢复出厂设置成功！')

    def __create_index(self):
        """
        创建faiss index
        """
        # assert len(self.samples) != 0, '样本库中没有样本'
        # faiss index
        self.index = faiss.IndexFlatIP(self.feat_dim)
        xb = np.array([sample['hist'] for sample in self.samples], dtype='float32')

        if len(xb.shape) == 4:
            xb = xb.squeeze()
        # if xb.shape[0] ==0 or xb.shape[1]!=1280:
        #     raise 'xb错误,要求是（N,1280),但是你的是{}'.format(xb.shape)
        self.index.add(xb)

    def get_index(self):
        return self.index

    def __len__(self):
        return len(self.samples)

    def __repr__(self):
        return "DATABASE VERSION IS BETA 2.0 "


if __name__ == '__main__':
    db = Database(model_type='res50', model_path=f'../model_zoo/res50_36cls_part.onnx')

    # 创建数据库，如果数据库文件存在则需要删除才能创建
    db.create_db(img_dir='/Users/musk/Desktop/智能售货柜/database_split/train')

    # 连接数据库，使用之前都需要连接数据库
    # db.connect_db()
    # 新增样本，增量学习
    # db.insert()
    # 恢复出厂设置
    # db.recover_db()

    # 删除易混淆的特征，这里的易混淆特征是指：比如苹果经常被识别成土豆，就删除
    # db.delete(type='cls',key='youzi')
    # db.delete(type='image', key='/Users/musk/PycharmProjects/shengxian_retrieval_onnx/database/bailuobo/20211115-114804WCP-md5-2ff80b4530ce5aea4b20a52dc0611060.png')
