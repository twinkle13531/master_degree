#!/usr/bin/env python
# coding: utf-8
# !pwd 202012/4ti2/functions/make_zsolve_data.py
import numpy as np
import pandas as pd
import random

def make_t_list(df):
    t_list = []
    t_list.append(sum(df['Y']))
    t_list.append(np.dot(df['Y'], df['SEX']))
    t_list.append(np.dot(df['Y'], df['AOP']))
    
    return t_list

# make .mat data
def make_mat(df):
    num_samples = df.shape[0]
    feature2 = df['SEX']
    feature3 = df['AOP']
    
    mat_data = [[1]*num_samples] #yの合計

    mat_data.append(feature2.values.tolist())

    mat_data.append(feature3.values.tolist())
    
    return mat_data


def make_data_for_4ti2(df):
    num_samples = df.shape[0]
    #feature1 = df['LI']
    feature2 = df['SEX']
    feature3 = df['AOP']
    
    t_list = make_t_list(df)
    
    mat = []
    mat_data = make_mat(df)
    mat_shape = [len(t_list), num_samples]
    mat += [mat_data, mat_shape]
    
    rel = []
    rel_data = [["="]*len(t_list)]
    rel_shape = [1, len(t_list)]
    rel += [rel_data, rel_shape]
    
    rhs = []
    rhs_data = [t_list]
    rhs_shape = [1, len(t_list)]
    rhs += [rhs_data, rhs_shape]
    
    sign = []
    sign_data = [[1]*num_samples]
    sign_shape = [1, num_samples]
    sign += [sign_data, sign_shape]
    
    ub = []
    ub_data = [[1]*num_samples]
    ub_shape = [1, num_samples]
    ub += [ub_data, ub_shape]
    
    return mat, rel, rhs, sign, ub


def save_system(df, bit_num, data_num):
    mat, rel, rhs, sign, ub = make_data_for_4ti2(df)
    shape_data_list = [mat, rel, rhs, sign, ub]
    name_list= ['mat', 'rel', 'rhs', 'sign', 'ub']
    
    for i, shape_data in enumerate(shape_data_list):
        shape = shape_data[1]
        data = shape_data[0]
        path = "{}bit/{}/{}bit_{}.{}".format(bit_num, data_num, bit_num, data_num, name_list[i])
        
        with open(path, "w") as f:
            f.write(" ".join([str(a) for a in shape])+"\n")
            for d in data:
                f.write(" ".join([str(a) for a in d])+"\n")