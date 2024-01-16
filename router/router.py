#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：router.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/11 14:29 
'''

class Router:
    def __init__(self):
        self.video
        self.key_frame
        self.xAxis
        self.hand_det_result
        self.goods_det_result
        self.retrieval_result
        self.info_type = ('video','frame','xAxis','goods','rr') # 分别对应上面的结果

        self.human = False
        self.human_threshold
    def get_info(self, type,infos):
        """
        从多个地方获取信息
        :param type:
        :return:
        """
        assert type not in self.info_type
        if type == self.info_type[0]:
            pass
        elif type == self.info_type[1]:
            pass
        elif type == self.info_type[2]:
            pass
        elif type == self.info_type[3]:
            pass
        elif type == self.info_type[4]:
            pass
        else:
            raise Exception('Type Error')

    def route(self):
        """
        综合信息决定是否交给人工
        :return:
        """

    def goodenv(self):
        pass
    def goodaxis(self):
        pass
    def goodmove(self):
        pass


