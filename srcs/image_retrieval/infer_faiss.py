import numpy as np
def infer(query,samples=None,index=None,topk=5,topd=None,thr=0.4):
    """
    使用Faiss后的检索
    @param query:
    @param samples: list，数据库中的一个sample 注意，需要是经过norm之后的
    @param index: faiss 的index
    @param topk: 返回结果topk
    @param thr: 按照距离的阈值
    @param topd:
    @return:
    """
    assert index is not None, "need to give either samples"
    assert topd is not None,'请指定topd要返回的数量'
    q_img, q_cls, q_hist = query['img'], query['cls'], query['hist']
    # 利用faiss进行检索
    q_hist = q_hist / np.linalg.norm(q_hist)
    D, I = index.search(q_hist.reshape(1,-1).astype('float32'),topd)
    D = D[0]
    I = I[0]
    # 标准化输出
    std_results = []
    std_results_cxy = []

    top_cls = []

    for _dis, _i in zip(D, I):
        _dis = 1 - _dis
        _cls = samples[_i]['cls']
        _img = samples[_i]['img']
        std_results_cxy.append({'cls': _cls, 'dis': _dis, 'img':_img})
        if len(std_results_cxy) == topk:
            break

    for _dis,_i in zip(D,I):
        _dis = 1 - _dis
        if _dis > thr:
            break
        _cls = samples[_i]['cls']
        if _cls not in top_cls:
            top_cls.append(_cls)
            std_results.append({'cls': _cls,
                                'dis': _dis })
        if len(top_cls) >= topk:
            break
    return top_cls, std_results, std_results_cxy
