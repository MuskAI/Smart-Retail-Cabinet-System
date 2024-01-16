# from apis.infer import infer
import sys
from database import Database
from feat_extractor import FeatExtractor

from infer_faiss import infer
import time
import os


class Retrievaler:
    def __init__(self, model_type='res50',project_root=''):
        """
        一个检索模型，需要确定好是使用小模型还是大模型
        :param model_type: small or big
        """
        if project_root is not '':
            self.project_root = project_root
        else:
            self.project_root = os.path.join(os.getcwd(),'retrieval-DL-based')

        print('Your input project root is:', project_root)
        cache_dir = os.path.join(project_root, 'cache')

        self.model_type = model_type
        self.model_path = '../model_zoo/res50_36cls_part.onnx'
        self.db = Database(cache_dir=cache_dir, model_type=model_type,model_path=self.model_path)
        self.connect_db()


    def retrieval_one_img(self, img_path, topk=10):
        """
        检索一张图片
        :return: 返回是topk个检索结果
        """
        topd = int(self.db.__len__())
        if os.path.exists(img_path):
            pass
        else:
            assert '要检索的图片路径不对'
        top_cls, std_result, std_result_cxy = self.inference(self.db, img_path, self.model_path, self.model_type,
                                                             topk=topk, topd=topd)

        res = {'style_1':top_cls,'style_2':std_result,'std_result':std_result_cxy}
        return res

    def connect_db(self):
        self.db.connect_db()

    def create_db(self):
        self.db.create_db()

    def insert(self):
        self.db.insert() # 自动检测的方式进行学习

    def inference(self,db, img, model_path, model_type, topk=5, topd=None, thr=2.0):
        """

        @param db:
        @param img:
        @param model_path:
        @param model_type:
        @param topk:
        @param topd:在检索中返回topd distance，一般设置为样本库的数量通过db.__len__() 获取
        @return:
        """
        assert topd is not None, '请指定topd'
        if model_type == 'res50':
            method = FeatExtractor(model_path=model_path)

        samples = db.get_samples()
        index = db.get_index()
        query = method.make_single_sample(img)
        # parameters
        s1 = time.time()
        top_cls, std_result, std_result_cxy = infer(query, samples=samples, index=index, topk=topk, topd=topd, thr=thr)
        e1 = time.time()

        isShow = False
        if isShow:
            print('检索用时{}'.format((e1 - s1)))
            print('topk results:', std_result_cxy)
            print('topk possible predicted classes:', top_cls)
            print('按阈值过滤后的结果:', std_result)

        return top_cls, std_result, std_result_cxy



#
# if __name__ == '__main__':
#
#     # database is saved in ./database
#     model_type = 'small'
#
#
#     project_root = os.getcwd()
#     model_path = switch_model(model_type,mode=1) # mode == 1 means get path
#
#     detector_model_path = os.path.join('')
#     db = Database(img_dir='database', cache_dir='./cache',model_type=model_type)
#     db.connect_db()
#     topd = int(db.__len__())
#
#     img = '/Users/musk/Desktop/cxy/test/A0H268/A0H268_20151125130249_6739717343.jpg'
#     inference(db, img, model_path, model_type, topk=10, topd=topd)
