
# _*_ coding:utf-8 _*_

# Author: xiaoran
# Time: 2018-07-06

import numpy as np
import pandas as pd
import sys

sys.path.append("../")

from common.utils import sim_l1, sim_l2, equal, sim

class Relief(object):
    '''
    Relief是一种过滤式特征选择方法，通过设计一个“相关统计量”来度量特征的重要性。该统计量是一个向量，
    其每一个分量分别对应一个初始特征，而特征子集的重要性则是由子集中每个特征所有对应的相关统计量分量之和决定。
    我们需要设计一个阈值t，然后选择比t大的相关统计量分量所对应的特征即可；也可指定欲选择的特征个数k，然后选择
    相关统计量分量最大的k个特征。
    给定训练集{(x1,y1),(x2,y2),...,(xm,ym)},对每一个示例xi,Relief先在xi的同类样本中寻找其最近邻xi,nh,
    称为“猜中紧邻”，再从xi的异类中寻找其最紧邻xi,nm，称为“猜错紧邻”，然后相关统计量对应属性j的分量为
    '''
    
    def __init__(self):
        ''' 
        gama: 阈值，选择大于阈值的分量
        k: 或者选择前k的得分最大的分量
        '''
        self.k = k
        self.gama = gama
        self.data = None
        self.label = None



    def _cal_near_hit(self, i, j):
        '''
        计算每一个样本的同类中的猜中紧邻，使用dict存储，下次直接
        '''
        # get lable for (i,j)
        lable = self.alldata[i][-1]
        tmp_d = alldata[alldata[:,-1]==label]
        pass

    def get_near_miss(self, i, j):
        '''
        得到第i个样本的第j个属性的猜错紧邻

        return 猜错紧邻
        '''
        pass

    def diff(self, a, b, category, sim_cate=equal, sim_real=sim_l1):
        '''
        计算a和b的距离,归一化之后的值
            a和b是list
        categorys: 类别特征,1
            1: 表示是类别特征
            0: 是实数特征
            形如: [1,0,1,..,1] 
        sim_cate:
            计算类别特征的距离，默认使用的直接比较是否相等，
        sim_real:
            默认使用的是l1范式，建议使用归一化之后的值
        '''
        return sim(a,b,category)

    def get_score_by_index(self, data, lable, j):
        '''
        data: 所有的数据集合
        lable: 对应的label
        return 第j属性对应的得分的值 
        '''
        pass


    def relief(self, data, label):
        '''
        data: dataFrame数据，或者numpy的多维数组
        label: 是对应的lable，

        return: 对应的特征的所有得分，根据属性的下标从0开始
        '''
        # 首先我们会对所有的特征归一化
        
        if isinstance(data, pd.DataFrame):
            self.data = data.values
        else:
            self.data = np.array(data)
        if isinstance(label, pd.Series):
            self.label = label.values
        else:
            self.lable = np.array(label)

        if len(data) != len(label):
            raise Exception("length of input datas is not same.")

        self.alldata = np.column_stack((self.data, self.label)) 
        # self.alldata = np.concatenate((self.data, self.label))
        pass



if __name__=="__main__":
    relief = Relief()

    a = [1,2,0,'a',3]
    b = [1,2,1,'b',1]
    category = [0,0,0,1,0]

    print (relief.diff(a,b,category))