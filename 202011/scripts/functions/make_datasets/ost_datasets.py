#!/usr/bin/env python
# coding: utf-8

#!pwd /Users/shihosato/src/github.com/twinkle13531/master_degree/202011/scripts/functions/make_datasets
# from make_datasets import ost_datasets
import pandas as pd
import numpy as np

def make_ost46(ost):
    ost46 = pd.DataFrame(columns=ost.columns[:-1])
    for i in range(ost.shape[0]):
        for _ in range(ost.iloc[i, -1]):
            ost46 = ost46.append(ost.iloc[i, :-1])
    ost46 = ost46.reset_index(drop=True)
    return ost46.to_csv('../../../input/ost46.csv', index=False)

def make_ost_num_df(num_sample):
    ost46 = pd.read_csv('../../../input/ost46.csv')
    ost_num = ost46.sample(num_sample, axis=0)
    ost_num.reset_index(drop=True, inplace=True)
    path = '../../../input/ost{}.csv'.format(num_sample)
    return ost_num.to_csv(path, index=False)

