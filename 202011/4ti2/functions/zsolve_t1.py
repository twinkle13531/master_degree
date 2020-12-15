#!/usr/bin/env python
# coding: utf-8
import pandas as pd                                         
import numpy as np                                                      
import matplotlib.pyplot as plt 


def make_result_list(zinhom_path):
    with open(zinhom_path) as f:
        l_strip = [[s.strip()] for s in f.readlines()]
        zinhom_num = int(l_strip[0][0][:-(2+1)])
        zinhom_list = []
        for i in range(1, zinhom_num+1):
            int_y = [int(l_strip[i][0].split()[j]) for j in range(len(l_strip[i][0].split()))]
            zinhom_list.append(int_y)
    return zinhom_num, zinhom_list


def calc_marginals(df):                   
    return np.array([                      
        sum(df['Y']),   
        np.dot(df['Y'], df['SEX']),      
        np.dot(df['Y'], df['AOP']),      
    ])                                 


def y_num_hist(df, zinhom_list, output_path):
    LI = list(df['LI'])
    hist_dic = {}
    print(len(zinhom_list))
    for zinhom in zinhom_list:
        if zinhom == list(df['Y']):
            print('i found')
        t1 = int(np.dot(LI, zinhom))
        if t1 in hist_dic.keys():
            hist_dic[t1] += 1
        else:
            hist_dic[t1] = 1
            
    x = [i for i in list(hist_dic.keys())]
    plt.xlabel('value of t1')
    plt.ylabel('number of samples')
    plt.bar(x, list(hist_dic.values()))
    plt.xticks(x, x)
    plt.savefig(output_path)
    plt.show()
    
    return hist_dic