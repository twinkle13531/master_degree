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
    #print(zinhom_num)
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
    for zinhom in zinhom_list:
        t1 = int(np.dot(LI, zinhom))
        if t1 in hist_dic.keys():
            hist_dic[t1] += 1
        else:
            hist_dic[t1] = 1

    real_t1 = np.dot(df['Y'], df['LI'])
    x = [i for i in list(hist_dic.keys())]
    y = [i for i in list(hist_dic.values())]
    plt.xlabel('value of t1')
    plt.ylabel('number of samples')
    plt.bar(x, y)
    plt.xticks(x, x)
    plt.yticks(y, y)
    plt.plot(real_t1, 0, marker='o', markersize=20)
    plt.savefig(output_path)
    plt.show()
    plt.close()
    
    return hist_dic


def y_num_hist_all_t1(df, zinhom_list, output_path):
    LI = list(df['LI'])
    hist_dic = {}
    for zinhom in zinhom_list:
        t1 = int(np.dot(LI, zinhom))
        if t1 in hist_dic.keys():
            hist_dic[t1] += 1
        else:
            hist_dic[t1] = 1
            
    for x in range(max(hist_dic.keys())+1):
        if not x in hist_dic.keys():
            hist_dic[x] = 0
            
    x = [i for i in list(hist_dic.keys())]
    y = [i for i in list(hist_dic.values())]
    plt.xlabel('value of t1')
    plt.ylabel('number of samples')
    plt.bar(x, y)
    plt.xticks(x, x)
    plt.yticks(y, y)
    plt.savefig(output_path)
    plt.show()
    
    return hist_dic


def calucurate_p(df, zinhom_list):
    LI = list(df['LI'])
    t1_y_num = 0
    for zinhom in zinhom_list:
        if int(np.dot(LI, df['Y'])) == int(np.dot(LI, zinhom)):
            t1_y_num += 1
    return t1_y_num / len(zinhom_list), len(zinhom_list)