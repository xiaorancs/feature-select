# !/usr/bin/python3
# _*_coding: utf-8 _*_


################################################
# Time   : 19-3-1                              #
# File:  : stats_feature_selector.py           #
# Author : Ran Xiao                            #
# Email  : xiaoranone@gmial.com                #
################################################


import numpy as np
import scipy  as sp
import pandas as pd
import logging

class StatFeatSelector(object):
    '''
    根据统计方法选择特征，
    1. 类别特征选择，包括0-1特征（单一特征去除）
    2. 根据缺失值选择特征
    3. 实数特征相关性统计，进行可视化，去除相关性高的特征
    4. 实数特征根据特征的方差，选择特征，去除方差小的特征
    5. 根据特征和label的相关性选择特征,

    参数:
    data: DataFrame
    label: label name
    category_columns: list，所有的类别特征，包括0-1特征
    number_columns: list, 所有数值特征

    category_threshold: double，default (0.95)
    missing_threshold: double, default (0.75)
    correlation_threshold:  double, default (0.95)
    std_threshold: double, default (0.05)
    k: int, 去除先关性最低的k个特征，default (0)

    task: regression or binary, multiclasses

    '''
    def __init__(self):
        pass

