#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Smart-Retail-Cabinet-System 
@File    ：db_module.py
@IDE     ：PyCharm 
@Author  ：haoran
@Date    ：2024/1/12 11:57 
'''
import os,sys,shutil

class DBIO:
    def __init__(self,db_path=None):
        assert db_path is None
        # 获取项目所在绝对路径
        self.proj_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.db_path = os.path.join(self.proj_dir,'cache/mobilenetV2-avgPooling-md5')
        print('DB PATH IS {}'.format(self.db_path))
    def d_in(self,in_db_path=None):
        """
        导入数据库文件到项目目录cache里
        """
        assert in_db_path and os.path.isfile(in_db_path)
        shutil.copy(in_db_path,self.db_path)
        print('\033[41m导入数据库文件成功！')

    def d_out(self,out_db_path=None):
        """
        导出数据库到指定目录
        """
        assert out_db_path
        shutil.copy(self.db_path,out_db_path)
        print('\033[41m导出数据库文件成功！')

if __name__ == '__main__':
    IOer = DBIO()
    IOer.d_in('/Users/musk/PycharmProjects/shengxian_retrieval_onnx/apis/test.db')
    IOer.d_out('/Users/musk/PycharmProjects/shengxian_retrieval_onnx/apis/demo')
