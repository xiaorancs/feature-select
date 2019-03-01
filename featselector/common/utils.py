# _*_ coding:utf-8 _*_
# Author: xiaoran
# Time: 2018-07-10

import numpy as np
import math


def sim_l1(a,b):
    return math.fabs(a-b)
    
def sim_l2(a,b):
    return (a-b)**2

def equal(a, b):
    return a==b

def sim(a,b,category,sim_cate=equal, sim_real=sim_l1):
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
    if len(a) != len(b):
        raise ValueError("a length=%d and b length=%d lengths are different." % (len(a),len(b)))
    if len(a) != len(category):
        raise ValueError("a length=%d and category length=%d lengths are different." % (len(a),len(category)))
    
    dist = 0.0
    for i in range(len(a)):
        if category[i] == 1:
            dist += sim_cate(a[i], b[i])
        else:
            dist += sim_real(a[i], b[i])
    return dist * 1.0 / len(a)

def normalize(arr):
    if isinstance(arr, list):
        arr = np.array(arr)
    mx = np.max(arr)
    mn = np.min(arr)
    m = np.mean(arr)
    arr = (arr - m)*1.0 / (mx-mn+1)
    return arr

def norm(arr,axis=1):
    '''
    axis = 1; 按列归一化
    axis = 0; 按行归一化
    '''
    arr = np.array(arr)
    m,n = arr.shape
    # 按列归一化
    for i in range(n):
        x = normalize(arr[:,i])
        arr[:,i] = x
    return arr

if __name__ == "__main__":
    arr = [[1,2,3],[3,2,1],[5,6,7],[7,8,9],[1,2,3]]

    print(arr)

    print(norm(arr))
