# !/usr/bin/python3
# _*_coding: utf-8 _*_


##############################################
# Time   : 19-3-1                            #
# File:  : model_feature_selector.py         #
# Author : Ran Xiao                          #
# Email  : xiaoranone@gmial.com              #
##############################################


import numpy as np
import pandas as pd
import lightgbm as lgb
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier, GradientBoostingRegressor

lgb_params = {
    'boosting_type': 'gbdt',
    'n_estimators': 1000,
    'learning_rate': 0.05,
    'min_child_samples': 46,
    'min_child_weight': 0.01,
    'subsample_freq': 2,
    'num_leaves': 40,
    'max_depth': 7,
    'subsample': 0.85,
    'colsample_bytree': 0.85,
    'verbose': -1,
    'seed': 2019
}

xgb_params = {
    'booster': 'gbtree',
    'learning_rate': 0.05,
    'max_depth': 5,
    'subsample': 0.85,
    'colsample_bytree': 0.85,
    'n_estimators': 1000,
    'min_child_weight': 3,
    'gamma': 0,
    'silent': True,
    'n_jobs': 4,
    'random_state': 2019,
    'verbose': 1
}

gbdt_params = {
    'learning_rate': 0.1,
    'n_estimators': 1000,
    'random_state': 2019
}

class ModelFeatSelector(object):
    def __init__(self, data, label, task, model_name='lgb', eval_metric=None, importance_threshold=0.0):
        '''
        :param data: DataFrame
        :param label: label name
        :param task:  任务类型， [regression, classification]
        :param model: ['gbdt', 'xgb', 'lgb']
        :param importance_threshold, 除去小于阈值的特征
        '''
        self.data = data
        self.label = label
        self.task = task
        self.model_name = model_name
        self._importance_threshold = importance_threshold

        self.model = None
        # 根据任务和label的值，设置验证准则
        self.eval_metric = None

        if model_name == 'lgb':
            if self.task == 'classification':
                self.model = lgb.LGBMClassifier(**lgb_params)
                if self.data[self.label].unique().shape[0] == 2:
                    self.eval_metric = 'logloss'
                else:
                    self.eval_metric = 'logloss'
            elif self.task == 'regression':
                self.model = lgb.LGBMRegressor(**lgb_params)
                self.eval_metric = 'l2'
            else:
                raise ValueError('Task must be either "classification" or "regression"')
        elif model_name == 'xgb':
            if self.task == 'classification':
                self.model = xgb.XGBClassifier(**xgb_params)
                if self.data[self.label].unique().shape[0] == 2:
                    self.eval_metric = 'logloss'
                else:
                    self.eval_metric = 'mlogloss'
            elif self.task == 'regression':
                self.model = xgb.XGBRegressor(**xgb_params)
                self.eval_metric = 'rmse'
            else:
                raise ValueError('Task must be either "classification" or "regression"')
        else: # gbdt
            if self.task == 'classification':
                self.model = GradientBoostingClassifier(**gbdt_params)
            elif self.task == 'regression':
                self.model = GradientBoostingRegressor(**gbdt_params)
            else:
                raise ValueError('Task must be either "classification" or "regression"')
        if not eval_metric:
            self.eval_metric = eval_metric


    def identify_importance(self, feats=None, k=None, importance_threshold=None, eval_frac=0.15,
                            n_iterations=5, early_stopping=True):
        '''
        移除重要度最小的k个特征
        :param feats: 所有特征
        :param eval_frac: 验证集合的比例
        :param n_iterations:  迭代次数，根据不同的划分数据集求特征平均性
        :param early_stopping:
        :return: 小于阈值的特征那么
        '''

        if not importance_threshold:
            importance_threshold = self._importance_threshold

        if not feats:
            feats = list(self.data.columns)

        if self.label in feats:
            feats.remove(self.label)

        # 划分数据集
        data = self.data[feats]
        labels = self.data[self.label]

        if self.model_name == 'gbdt':
            early_stopping = False

        feature_importance_values = np.zeros(len(feats))
        print('Training %s Model\n' % self.model_name)
        for _ in range(n_iterations):
            if early_stopping:
                X_train, X_valid, y_train, y_valid = train_test_split(data, labels, test_size=eval_frac)
                self.model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_valid, y_valid)],
                               eval_metric=self.eval_metric, early_stopping_rounds=50, verbose=50)

                del X_train, X_valid, y_train, y_valid
            else:
                self.model.fit(data, labels)

            feature_importance_values += self.model.feature_importances_ / n_iterations

        # sort by importance
        feature_importances = pd.DataFrame({'feature': feats, 'importance': feature_importance_values})
        feature_importances = feature_importances.sort_values('importance', ascending=False).reset_index(drop=True)

        # normalize the features importances
        feature_importances['normalized_importance'] = feature_importances['importance'] / feature_importances[
            'importance'].sum()
        feature_importances['cumulative_importance'] = np.cumsum(feature_importances['normalized_importance'])

        low_importance_feats = feature_importances[feature_importances['importance'] < importance_threshold]

        print("Drop features by importance:", low_importance_feats)
        drop_feats = list(low_importance_feats['feature'].values)
        if k:
            drop_feats = list(low_importance_feats['feature'].values[-k:])

        return drop_feats

if __name__ == "__main__":
    pass