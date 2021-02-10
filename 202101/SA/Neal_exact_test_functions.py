#!/usr/bin/env python
# coding: utf-8
import pandas as pd                                         
import numpy as np                                              
from scipy.special import comb                                      
import math
from operator import mul
import neal 
import dimod                                                       
import random                                                           
import matplotlib.pyplot as plt                                         
import timeit
import time
from itertools import combinations


def calc_marginals(df):                   
    return np.array([                      
        sum(df['Y']),   
        np.dot(df['Y'], df['SEX']),      
        np.dot(df['Y'], df['AOP']),      
    ])                                 


def make_Hamiltonian(df):
    t_list = calc_marginals(df)
    
    N=len(df)
    dup_list = [(i, i) for i in range(N)]
    comb_list = [(i, j) for i in range(N) for j in range(i+1, N)]
    
    lin_Y = [1-2*t_list[0] for (i, _) in dup_list] #同じy同士
    quad_Y = [2 for (i, j) in comb_list] #異なるy同士
    num_Y = t_list[0]**2 #数字の二乗
    
    SEX = df['SEX'].iloc
    lin_SEX  = [(SEX[i] - 2 * t_list[1]) * SEX[i] for (i, _) in dup_list]
    quad_SEX  = [2*SEX[i] * SEX[j] for (i, j) in comb_list]
    num_SEX  = t_list[1]**2
    
    AOP = df['AOP'].iloc
    lin_AOP = [(AOP[i] - 2 * t_list[2]) * AOP[i] for (i, _) in dup_list]
    quad_AOP = [2*AOP[i] * AOP[j] for (i, j) in comb_list]
    num_AOP = t_list[2]**2
    
    lin_list = [sum(lin) for lin in zip(lin_Y, lin_SEX, lin_AOP)]
    lin = {i: lin_list[i] for (i, _) in dup_list}
    
    #quad
    quad_values = [sum(quad) for quad in zip(quad_Y, quad_SEX, quad_AOP)]
    quad = {ij: quad_values[n] for (n, ij) in enumerate(comb_list)}
    
    #num
    num = num_Y + num_SEX + num_AOP
    
    return dimod.BinaryQuadraticModel(lin, quad, num, dimod.Vartype.BINARY)#dic, dic, num

#make_res_dataとfind_valid_y(res)を合わせた時間をcalculation_timeとする
def make_res_data(df, num_reads):
    sa_sampler = neal.sampler.SimulatedAnnealingSampler()
    initial_states = df['Y'].values.tolist()
    bqm = make_Hamiltonian(df)
    res = sa_sampler.sample(
        bqm, num_reads=num_reads, 
        initial_states=initial_states, 
        initial_states_generator='tile'
    ) 
    return res

def find_valid_y(res):                                                        
    valid_y_info_dic = {}#sample:occurrence
    for y_info in list(res.record):
        if y_info[1]==0.:#energy
            this_time_y = tuple(y_info[0])#sample
            if this_time_y in list(valid_y_info_dic.keys()):
                valid_y_info_dic[this_time_y] += y_info[2]#occurrence
            else:
                valid_y_info_dic[this_time_y] = y_info[2]
    return valid_y_info_dic


def calc_p_value(valid_y_info_dic):
    valid_y_list = list(valid_y_info_dic.kesy())
    t1_y = 0
    t1 = np.dot(df['Y'], df['LI'])
    for valid_y_tu in valid_y_list:
        valid_y = list(valid_y_tu)
        if int(np.dot(valid_y, list(df['LI'])))==t1:
            t1_y += 1
    return t1_y/len(valid_y_info_dic)


def y_num_hist(df, valid_y_info_dic, path):
    LI = list(df['LI'])
    hist_dic = {}
    valid_y_list = list(valid_y_info_dic.keys())
    for valid_y in valid_y_list:
        valid_y_list = list(valid_y)
        t1 = int(np.dot(LI, valid_y_list))
        if t1 in hist_dic.keys():
            hist_dic[t1] += 1
        else:
            hist_dic[t1] = 1
    x = [i for i in list(hist_dic.keys())]
    y = [i for i in list(hist_dic.values())]
    plt.xlabel('value of t1')
    plt.ylabel('number of samples')
    plt.bar(x, y)
    plt.xticks(x, x)
    plt.yticks(y, y)
    plt.savefig(path, format='png')
    plt.close()
    return hist_dic


def occurence_hist(valid_y_info_dic, plot_path):
    x = [i for i in list(valid_y_info_dic.values())]
    plt.xlabel('each sample')
    plt.ylabel('number of the occurrence')
    plt.bar(x, occurrence_list)
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    plt.savefig(plot_path, format='png')
    plt.show()
    plt.close()
    return 0
 
    
def time_num_y(df, num_reads, path):
    sa_sampler = neal.sampler.SimulatedAnnealingSampler()
    initial_states = df['Y'].values.tolist()
    t_list = calc_marginals(df)
    
    valid_y_list= []                                                           
    valid_y_num= 0
    bqm = make_Hamiltonian(df)
    
    time_0 = time.time()
    res = sa_sampler.sample(
        bqm, num_reads=num_reads, 
        initial_states=initial_states, 
        initial_states_generator='tile'
    )                                                      
    time_list = []
    valid_y_info_dic_1 = {}
    for y_info in list(res.record):
        if y_info[1]==0.:
            this_time_y = tuple(y_info[0])#sample
            if this_time_y in list(valid_y_info_dic_1.keys()):
                continue
            else:
                valid_y_info_dic_1[this_time_y] = 1
                time_1 = time.time()
                elapsed_time = time_1 - time_0
                time_list.append(elapsed_time)
    valid_y_num_list = [i for i in range(1, len(valid_y_info_dic_1)+1)]
    plt.xlabel('time')
    plt.ylabel('number of hits')
    plt.plot(time_list, valid_y_num_list)
    plt.savefig(path)
    plt.show()
    plt.close()
    return time_list


def p_value_transition(res, output_path):
    valid_y_list = []
    t1_y = 0
    t1 = int(np.dot(df['Y'], df['LI']))
    p_dic = {}
    for y_info in list(res.record):
        if y_info[1]==0.:
            valid_y = list(y_info[0]) 
            if all(valid_y != p for p in valid_y_list):
                valid_y_list.append(valid_y)
                if int(np.dot(valid_y, list(df['LI'])))==t1:
                    t1_y += 1
                    p_dic[len(valid_y_list)] = t1_y/len(valid_y_list)             
    plt.xlabel('number of hits')
    plt.ylabel('p value')
    plt.plot(list(p_dic.keys()), list(p_dic.values()))
    plt.savefig(output_path)
    plt.show()
    plt.close()
    return valid_y_list, p_dic