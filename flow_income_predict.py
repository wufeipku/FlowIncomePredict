# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: flow_income_predict.py
# @AUthor: Fei Wu
# @Time: 11月, 17, 2022

import pandas as pd
import lightgbm as lgb
import numpy as np
from frechetdist import frdist
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class IncomeFlowPredictOfAllLife:
    def __init__(self, df_his, df_pre, month:str, delta_days:str, vv_income:str, n=15, m=90):
        """
        :param df_his: 历史流量or收入，按月
        :param df_pre: 需预测月份的发文后n天内流量or收入
        :param month: 月份字段名
        :param delta_days: 发文后时间间隔，发文当天为0
        :param vv_income: 流量or收入
        :param n: 预测月份发文后有流量、收入数据的最小天数 默认15
        :param m: 需要预测的天数
        """
        self.df_his = df_his  #15天收入or收入,保证第一列为发文月份，第二列为发文后第n天，第三列为流量或收入
        self.df_pre = df_pre
        self.month = month
        self.delta_days = delta_days
        self.vv_income = vv_income
        self.n = n
        self.m = m
    def data_select(self):
        data1 = pd.pivot(self.df_his, index=self.delta_days, columns=self.month, values=self.vv_income)
        data2 = pd.pivot(self.df_pre, index=self.delta_days, columns=self.month, values=self.vv_income)
        data1 = data1.iloc[0:self.m].cumsum(axis=0)
        data2 = data2.iloc[0:self.n].cumsum(axis=0)
        corr_dict = {}
        for col in data2.columns:
            temp = data1.iloc[0:self.n].apply(lambda x: np.corrcoef(x, data2[col])[0,1])
            temp.sort_values(ascending=False, inplace=True)
            corr_dict.update({col: temp.index[0]})
        return data1, data2, corr_dict

    def data_select_fr(self):
        data1 = pd.pivot(self.df_his, index=self.delta_days, columns=self.month, values=self.vv_income)
        data2 = pd.pivot(self.df_pre, index=self.delta_days, columns=self.month, values=self.vv_income)
        data1 = data1.iloc[0:self.m].cumsum(axis=0)
        data2 = data2.iloc[0:self.n].cumsum(axis=0)
        scaler = StandardScaler()
        data1_st = pd.DataFrame(scaler.fit_transform(data1.iloc[0:self.n]), index=data1.iloc[0:self.n].index, columns=data1.columns)
        data2_st = pd.DataFrame(scaler.fit_transform(data2), index=data2.index, columns=data2.columns)
        fr_dict = {}
        for col in data2_st.columns:
            temp = data1_st.apply(lambda x: frdist(list(zip(range(self.n), x)), list(zip(range(self.n),data2[col]))))
            temp.sort_values(ascending=False, inplace=True)
            fr_dict.update({col: temp.index[0]})
        return data1, data2, fr_dict

    def calc_income_vv(self, method='corr'):
        if method == 'corr':
            data1, data2, corr_dict = self.data_select()
        else:
            data1, data2, corr_dict = self.data_select_fr()
        result = []
        for col in data2.columns:
            pre = data2.iloc[-1][col] / data1.iloc[self.n-1][corr_dict[col]] * data1.iloc[-1][corr_dict[col]]
            result.append((col, pre))
        return result
if __name__ == '__main__':
    data = pd.read_csv('发文90天内流量.csv', encoding='utf-8')
    his = data[data.month1 != 202207]
    pre = data[data.month1 == 202207]
    cl = IncomeFlowPredictOfAllLife(his, pre, month='month1', delta_days='delta_days', vv_income='vv', n=15, m=90)
    result = cl.calc_income_vv(method='frdist')
    print(result)
    print(pre.sum())

