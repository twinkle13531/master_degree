#!use/bin/Nenv python
# coding: utf-8

import pandas as pd
import numpy as np
import scipy.special as comb
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
	return np.array(
        [sum(df['Y']),
         np.dot(df['Y'], df['SEX']),
         np.dot(df['Y'], df['AOP'])
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
    
    quad_values = [sum(quad) for quad in zip(quad_Y, quad_SEX, quad_AOP)]
    quad = {ij: quad_values[n] for (n, ij) in enumerate(comb_list)}
    
    num = num_Y + num_SEX + num_AOP
    return dimod.BinaryQuadraticModel(lin, quad, num, dimod.Vartype.BINARY)#dic, dic, num


def make_res_data(df, num_reads):
    sa_sampler = neal.sampler.SimulatedAnnealingSampler()
    initial_states = df['Y'].values.tolist()
    bqm = make_Hamiltonian(df)
    time_0 = time.time()
    res = sa_sampler.sample(
        bqm, num_reads = num_reads,
        initial_states = initial_states,
        initial_states_generator = 'tile'
    )
    time_1 = time.time()
    elapsed_time = time_1 - time_0
    return res, elapsed_time


def find_valid_y(res):
    valid_y_info_dic = {}#sample:occurrence
    for sample, energy, num_occurrences in list(res.data(['sample', 'energy', 'num_occurrences'])):
        if energy==0.:
            this_time_y = tuple(sample.values())
            if this_time_y in list(valid_y_info_dic.keys()):#
                valid_y_info_dic[this_time_y] += num_occurrences#
            else:
                valid_y_info_dic[this_time_y] = num_occurrences#
    return valid_y_info_dic


def num_y_transition_nodup(df, num_reads, path):
    time_0 = time.time()
    sa_sampler = neal.sampler.SimulatedAnnealingSampler()
    bqm = make_Hamiltonian(df)
    res = sa_sampler.sample(
        bqm,
        num_reads = num_reads,
        initial_states = df['Y'].values.tolist(),
        initial_states_generator = 'tile'
    )
    
    valid_y_info_dic_nodup = {}
    time_list = []
    for sample, energy, num_occurrences in list(res.data(['sample', 'energy', 'num_occurrences'])):
        if energy==0.:
            sample_tu = tuple(sample.values())
            if sample_tu in list(valid_y_info_dic_nodup.keys()):
                continue
            else:
                valid_y_info_dic_nodup[sample_tu] = 1
                time_1 = time.time()
                elapsed_time = time_1 - time_0
                time_list.append(elapsed_time)
    valid_y_num_list = [i for i in range(1, len(valid_y_info_dic_nodup)+1)]
    plt.xlabel('time')
    plt.ylabel('number of valid y')
    plt.plot(time_list, valid_y_num_list)
    plt.savefig(path)
    plt.show()
    plt.close()
    return time_list


class SA_res_valid_dic():
    def __init__(self, df, res, valid_y_info_dic, num_reads):
        self.df = df
        self.res = res
        self.valid_y_info_dic = valid_y_info_dic
        self.num_reads = num_reads
        
    def p_value_transition(self, output_path):
        valid_y_list = []
        t1 = int(np.dot(self.df['Y'], self.df['LI']))
        t1_y = 0
        p_dic = {}
        
        for sample, energy, num_occurrences in list(self.res.data(['sample', 'energy', 'num_occurrences'])):
            if energy==0.:
                this_time_y = tuple(sample.values())
                if this_time_y in valid_y_list:
                    continue
                else:
                    valid_y_list.append(this_time_y)#
                    this_time_y_se = pd.Series(this_time_y)
                    if int(np.dot(this_time_y_se, self.df['LI'])) == t1:
                        t1_y += 1
                        p_dic[len(valid_y_list)] = t1_y / len(valid_y_list)
        plt.xlabel('number of valid y')
        plt.ylabel('p value')
        plt.plot(list(p_dic.keys()), list(p_dic.values()))
        plt.savefig(output_path)
        plt.show()
        plt.close()
        return valid_y_list, p_dic
    
    def occurrence_hist(self, plot_path):
        occurrence_list = list(self.valid_y_info_dic.values())
        x = [i for i in range(len(occurrence_list))]
        plt.xlabel('each sample')
        plt.ylabel('number of the occurrence')
        plt.bar(x, occurrence_list)
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        plt.savefig(plot_path)
        plt.show()
        plt.close()
        return occurrence_list
    
    def y_num_hist(self, path):
        t_dic = {}
        valid_y_list = []
        for valid_y in list(self.valid_y_info_dic.keys()):
            if valid_y in valid_y_list:
                continue
            else:
                valid_y_se = pd.Series(valid_y)
                this_time_t1 = int(np.dot(valid_y_se, self.df['LI']))
                if this_time_t1 in list(t_dic.keys()):
                    t_dic[this_time_t1] += 1
                else:
                    t_dic[this_time_t1] = 1
        x = [i for i in list(t_dic.keys())]
        y = [i for i in list(t_dic.values())]
        plt.xlabel('value of t1')
        plt.ylabel('number of sample')
        plt.bar(x, y)
        plt.xticks(x, x)
        plt.yticks(y, y)
        plt.savefig(path)
        plt.show()
        plt.close()
        return t_dic
    
    def calc_p_value(self):
        t1 = int(np.dot(self.df['Y'], self.df['LI']))
        num_t1_y = 0
        for valid_y in list(self.valid_y_info_dic.keys()):
            valid_y_se = pd.Series(valid_y)
            if int(np.dot(valid_y_se, self.df['LI']))==t1:
                num_t1_y += 1
        return num_t1_y/len(self.valid_y_info_dic)