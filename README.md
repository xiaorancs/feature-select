# featselector
<center><img src="./featselector.png"/></center>

**featselector是一个基于统计分析和模型选择的特征选择器.**

Github: https://github.com/xiaorancs/feature-select
## 背景
特征过多会导致如下后果:     
1. 引起维数灾难，模型推广能力差
2. 特征过于稀疏，模型效果不好
3. 很多冗余特征和相关性高的特征，降低模型精度

在机器学习任务中，有两大难题:
1. 特征提取和选择
2. 模型选择和优化
我们都会一个问题，特征好提取，但是选择很困难。我们很容易基于组合和时间提取出来很多特征，但是这样特征中很多是无效的特征，featselector就是来找到这些冗余的无效的特征.

## featselector
featselector是一个基于统计分析和模型的特征选择器.
1. StatFeatSelector(基于统计的特征选择）
   + identify_missing(缺失值选择)
        > 如果特征的缺失值比例大于阈值(0.9), 就删除该特征
   + identify_single_unique(单一值选择)
        > 如果特征中有一个值出现比例超过阈值(0.97),删除该特征
   + identify_std(方差选择)
        > 实数特征根据方差选择, 如果方差过小, 小于阈值(0.05), 就删除该特征
   + identify_corlinear(特征之间相关性选择)
        > 删除相关性大于阈值(0.96)的特征中的一个，减少冗余性
   + identify_corlinearlabel(特征和目标之间的选相关性选择)
        > 计算特征和目标之间的相关性，删除相关性小于阈值(0.001)的特征
2. ModelFeatSelector(基于树模型的特征选择)
   + identify_importance(删除重要度低的特征)
        > 使用(gbdt,xgb,lgb)模型计算特征的重要性，删除重要性最低的k个特征，或者重要性小于阈值(0.002)的特征

## Install
1. git clone https://github.com/xiaorancs/feature-select.git
2. python steup.py install

## Usage
任何人都可以使用或者修改源码，但请注明出处


## Sample
1. [Kaggle房价预测特征选择](./featselector_sample_housePrice.ipynb)
   + 特征选择之前, score: 0.13296
   + 特征选择之后, score: 0.13112
2. Kaggle泰坦尼克号预测(undo)

## Reference
1. https://github.com/duxuhao/Feature-Selection
2. https://github.com/WillKoehrsen/feature-selector


**注：生活如此，问题不大. 喵～**
