# !/usr/bin/python3
# _*_ coding: utf-8 _*_


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
    5. 根据特征和label的相关性选择特征, 相关性越大越好

    参数:
    data: DataFrame
    label: label name
    category_columns: list，所有的类别特征，包括0-1特征
    number_columns: list, 所有数值特征

    category_threshold: double，default (0.95)
    missing_threshold: double, default (0.75)
    correlation_threshold:  double, default (0.95)
    std_threshold: double, default (0.05)
    relativity_threshold: double, 去除先关性最低的k个特征，default (0.0005)

    '''
    def __init__(self, data, label, category_columns, number_columns,
                 category_threshold=0.95, missing_threshold=0.75,
                 correlation_threshold=0.95, std_threshold=0.05, relativity_threshold=0.0005):
        self.data = data
        self.label = label
        self._category_columns = category_columns
        self._number_columns = number_columns
        self._category_threshold = category_threshold
        self._missing_threshold = missing_threshold
        self._correlation_threshold = correlation_threshold
        self._std_threshold = std_threshold
        self._relativity_threshold = relativity_threshold

    def identify_missing(self, missing_threshold=None, columns=None):
        """
        根据缺失值进行特征选择，如果缺失值比例大于阈值就是移除特征
        这里判断所有的列，如果没有指定columns
        :param missing_threshold:
        :return: dict { rm_col: missing_ratio}
        """
        if not missing_threshold:
            missing_threshold = self._missing_threshold
        if not columns:
            columns = self._category_columns + self._number_columns

        N = self.data.shape[0]
        missing_series = self.data[columns].isnull().sum() / N
        missing_stats = pd.DataFrame(missing_series).rename(columns={0:'missing_fraction'})
        missing_stats = missing_stats.sort_values('missing_fraction', ascending=False)
        missing_feats = missing_stats[missing_stats['missing_fraction'] > missing_threshold]
        print("Drop features by missing value:", missing_feats)
        drop_list = list(missing_feats.index)
        return drop_list

    def identify_single_unique(self, category_threshold=None, columns=None):
        '''
        判断某个类别中的特征比例，是否超过了阈值，_category_threshold
        :return: drop的feature
        '''
        drop_list = []
        if not category_threshold:
            category_threshold = self._category_threshold
        if not columns:
            columns = self._category_columns

        single_fraction = []
        for col in columns:
            tmp = self.data[col].value_counts()
            if tmp.values[0] / self.data.shape[0] > category_threshold:
                drop_list.append(col)
                single_fraction.append(tmp.values[0] / self.data.shape[0])
        single_stats = pd.DataFrame(data={'drop_feature': drop_list, 'single_fraction': single_fraction})
        print("Drop features by single unique:", single_stats)

        return drop_list

    def identify_std(self, std_threshold=None, columns=None):
        '''
        判断特征的标准差是否小于阈值
        :param std_threshold:
        :param columns:
        :return:
        '''
        drop_list = []
        if not std_threshold:
            std_threshold = self._std_threshold
        if not columns:
            columns = self._number_columns

        std_stats = pd.DataFrame(self.data[columns].std()).rename(columns={0:'std'})
        std_stats = std_stats.sort_values('std', ascending=False)
        std_feats = std_stats[std_stats['std'] < std_threshold]
        print('Drop features by std:', std_feats)
        drop_list = list(std_feats.index)
        return drop_list

    def identify_corlinear(self, correlation_threshold=None, columns=None):
        '''
        根据线性相关性选择特征, 所有特征都可以计算
        :param correlation_threshold:
        :param columns:
        :return: drop_features
        '''
        if not correlation_threshold:
            correlation_threshold = self._correlation_threshold
        if not columns:
            columns = self._number_columns + self._category_columns
        corr_matrix = self.data[columns].corr()

        # 设置右上角矩阵
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        drop_list = [col for col in upper.columns if any(upper[col].abs() > correlation_threshold)]

        corr_stats = pd.DataFrame(columns=['drop_feat', 'corr_feat', 'corr_value'])
        for col in drop_list:
            # 找到相关特征
            corr_features = list(upper[col][upper[col].abs() > correlation_threshold].index)

            # 得到相关性的值
            corr_values = list(upper[col][upper[col].abs() > correlation_threshold])
            drop_feat = [col for _ in range(len(corr_features))]
            df_temp = pd.DataFrame.from_dict({'drop_feat': drop_feat,
                                              'corr_feat': corr_features,
                                              'corr_value': corr_values})
            corr_stats = corr_stats.append(df_temp, ignore_index=True)

        print("Drop features by correlation:", corr_stats)
        return drop_list

    def identify_corlinearlabel(self, relativity_threshold=None, target=None):
        """
        判断特征和target的相关性，小于等与阈值的就进行删除
        :param relativity_threshold: 0.005
        :param target:
        :return:
        """
        if not relativity_threshold:
            relativity_threshold = self._relativity_threshold
        if not target:
            target = self.label

        relativity_stats = pd.DataFrame(self.data.corrwith(self.data[target])).rename(columns={0: 'corlinear'})
        relativity_stats = relativity_stats.sort_values('corlinear',ascending=False)

        drop_relativity = relativity_stats[np.abs(relativity_stats['corlinear']) < relativity_threshold]
        print("Drop feautures by relativity with target:", drop_relativity)
        drop_list = list(drop_relativity.index)
        return drop_list


if __name__ == "__main__":
    pass