#!/usr/bin/env python
# coding: utf-8
import pandas as pd 
import numpy as np
from scipy.special import comb
import math
import itertools
import random
import matplotlib.pyplot as plt
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import AutoEmbeddingComposite
from dwave.embedding.chain_strength import uniform_torque_compensation
import dimod
import timeit
import time
from scipy import stats

#繰り返さない！
dw_sampler = DWaveSampler(
        endpoint="https://cloud.dwavesys.com/sapi",
        solver = 'DW_2000Q_6',
        #token = "TOKY-1319d5c52b9aa35f34b40feba0cea58a4f5d3c09",
        token = "DEV-6a425d517b4cc6a3e4f9fef6c26af9cd037b879e",
        retry_interval=5
    )

qa_sampler = AutoEmbeddingComposite(dw_sampler)

def calc_marginals(df):
        return np.array([                      
                sum(df['Y']),
                np.dot(df['Y'], df['SEX']),
                np.dot(df['Y'], df['AOP']),
            ])
        
def make_Hamiltonian_stander(df):
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

    #lin
    lin_list = [sum(lin) for lin in zip(lin_Y, lin_SEX, lin_AOP)]
    lin_list = list(stats.zscore(lin_list))
    lin = {i: lin_list[i] for (i, _) in dup_list}

    #quad
    quad_values = [sum(quad) for quad in zip(quad_Y, quad_SEX, quad_AOP)]
    quad_values = list(stats.zscore(quad_values))
    quad = {ij: quad_values[n] for (n, ij) in enumerate(comb_list)}

    #num
    num = num_Y + num_SEX + num_AOP

    return dimod.BinaryQuadraticModel(lin, quad, num, dimod.Vartype.BINARY)#dic, dic, num


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

    #lin
    lin_list = [sum(lin) for lin in zip(lin_Y, lin_SEX, lin_AOP)]
    lin = {i: lin_list[i] for (i, _) in dup_list}

    #quad
    quad_values = [sum(quad) for quad in zip(quad_Y, quad_SEX, quad_AOP)]
    quad = {ij: quad_values[n] for (n, ij) in enumerate(comb_list)}

    #num
    num = num_Y + num_SEX + num_AOP

    return dimod.BinaryQuadraticModel(lin, quad, num, dimod.Vartype.BINARY)#dic, dic, num

def make_Hamiltonian_ice(df, gamma):
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

    #lin
    lin_list = [sum(lin) for lin in zip(lin_Y, lin_SEX, lin_AOP)]
    lin = {i: gamma*lin_list[i] for (i, _) in dup_list}

    #quad
    quad_values = [sum(quad) for quad in zip(quad_Y, quad_SEX, quad_AOP)]
    quad = {ij: quad_values[n] for (n, ij) in enumerate(comb_list)}

    #num
    num = num_Y + num_SEX + num_AOP

    return dimod.BinaryQuadraticModel(lin, quad, num, dimod.Vartype.BINARY)#dic, dic, num

def make_Hamiltonian_ice0(df, k):
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

    #lin
    lin_list = [sum(lin) for lin in zip(lin_Y, lin_SEX, lin_AOP)]
    lin = {i: k*lin_list[i] for (i, _) in dup_list}

    #quad
    quad_values = [sum(quad) for quad in zip(quad_Y, quad_SEX, quad_AOP)]
    quad = {ij: k*quad_values[n] for (n, ij) in enumerate(comb_list)}

    #num
    num = num_Y + num_SEX + num_AOP

    return dimod.BinaryQuadraticModel(lin, quad, num, dimod.Vartype.BINARY)#dic, dic, num

    
def sample_(bqm, chain_strength, num_reads):
    res = qa_sampler.sample(bqm, chain_strength = chain_strength, chain_break_fraction=True, num_reads=num_reads)
    return res

def sampler_autoscale(bqm, chain_strength, num_reads):
    res = qa_sampler.sample(
        bqm, chain_strength = chain_strength, 
        chain_break_fraction=True, num_reads=num_reads, auto_scale=True)
    return res

def sampler_autoscale_numspin(bqm, chain_strength, num_reads, num_spin_reversal_transforms):
    res = qa_sampler.sample(
        bqm, chain_strength = chain_strength, 
        chain_break_fraction=True, num_reads=num_reads, 
        auto_scale=True, num_spin_reversal_transforms=num_spin_reversal_transforms)
    return res


def sampler_annealingtime_autoscale(bqm, chain_strength, num_reads, annealing_time):
    res = qa_sampler.sample(
        bqm, chain_strength = chain_strength, 
        chain_break_fraction=True, num_reads=num_reads, 
        annealing_time = annealing_time, auto_scale=True)
    return res

def sampler_timeadjust_autoscale(bqm, chain_strength, num_reads, annealing_time, readout_thermalization):
    res = qa_sampler.sample(
        bqm, chain_strength = chain_strength, 
        chain_break_fraction=True, num_reads=num_reads, 
        annealing_time = annealing_time, 
        readout_thermalization = readout_thermalization, auto_scale=True)
    return res

def sampler_paras(bqm, chain_strength, num_reads, spin_num):
    res = qa_sampler.sample(
        bqm, chain_strength = chain_strength, 
        chain_break_fraction=True, 
        num_reads=num_reads, 
        auto_scale=True, 
        num_spin_reversal_transform = spin_num
    )
    return res

#postprocessツールはadvantageで有効らしい

class QA_DSampler_AEmbedding:
    def __init__(self, df, bqm, n, num_reads, chain_strength, res):
        self.df = df
        self.bqm = bqm
        self.n = n
        self.num_reads = num_reads
        self.chain_strength = chain_strength
        self.res = res
        
    def find_y(self):
        valid_y_info_dic = {}#sample:[occurrences, chain_break_fraction]
        for sample, energy, num_occurrences, chain_break_fraction in self.res.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
            if energy == 0.0:
                sample_tuple = tuple(sample.values())
                if sample_tuple in list(valid_y_info_dic.keys()):
                    valid_y_info_dic[sample_tuple][0] += num_occurrences
                else:
                    valid_y_info_dic[sample_tuple] = [num_occurrences, chain_break_fraction]
        return valid_y_info_dic
        
class QA_DSampler_AEmbedding_ntimes:
    def __init__(self, df, bqm, n, num_reads, chain_strength):
        self.df = df
        self.bqm = bqm
        self.n = n
        self.num_reads = num_reads
        self.chain_strength = chain_strength
        

    def find_valid_y_time_ntimes(self):
        valid_y_info_dic = {}#sample:[occurrences, chain_break_fraction]
        calculation_time = 0
        for _ in range(self.n):
            res = qa_sampler.sample(self.bqm, chain_strength = self.chain_strength, chain_break_fraction=True, num_reads=self.num_reads)#annealing_time
            for sample, energy, num_occurrences, chain_break_fraction in res.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
                if energy == 0.0:
                    sample_tuple = tuple(sample.values())
                    if sample_tuple in list(valid_y_info_dic.keys()):
                        valid_y_info_dic[sample_tuple][0] += num_occurrences
                    else:
                        valid_y_info_dic[sample_tuple] = [num_occurrences, chain_break_fraction]
        return  valid_y_info_dic, res.info['timing']['anneal_time_per_run']
    
    
    def find_y_time(self):
        valid_y_info_dic = {}#sample:[occurrences, chain_break_fraction]
        calculation_time = 0
        for _ in range(self.n):
            res = qa_sampler.sample(self.bqm, chain_strength = self.chain_strength, chain_break_fraction=True, num_reads=self.num_reads)#annealing_time
            time_0 = time.time()
            for sample, energy, num_occurrences, chain_break_fraction in res.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
                if energy == 0.0:
                    if sample_tuple in list(valid_y_info_dic.keys()):
                        valid_y_info_dic[sample_tuple][0] += num_occurrences
                    else:
                        valid_y_info_dic[sample_tuple] = [num_occurrences, chain_break_fraction]
            time_1 = time.time()
            calculation_time += time_1 - time_0 + 20*10**(-6)
        return  calculation_time

    
    def y_num_t1_hist(self, valid_y_info_dic, plot_path):
        LI = list(self.df['LI'])
        hist_dic = {}

        for valid_y_tu in list(valid_y_info_dic.keys()):
            valid_y = list(valid_y_tu)
            t1 = int(np.dot(LI, valid_y))
            if t1 in hist_dic.keys():
                hist_dic[t1] += 1
            else:
                hist_dic[t1] = 1

        x = [i for i in list(hist_dic.keys())]
        y = [j for j in list(hist_dic.values())]
        plt.xlabel('value of t1')
        plt.ylabel('number of samples')
        plt.bar(x, y)
        plt.xticks(x, x)
        plt.yticks(y, y)
        plt.savefig(plot_path)
        #plt.plot(t1, 0)
        plt.show()
        plt.close()
        return hist_dic


    def num_y_transition(self, path):
        time_list = []#
        valid_y_num_nodup = {}
        time_0 = time.time() 
        for _ in range(self.n):
            res = qa_sampler.sample(self.bqm, chain_strength = self.chain_strength, chain_break_fraction=True, num_reads=self.num_reads)
            for sample, energy, num_occurrences, chain_break_fraction in res.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
                if energy == 0.:
                    sample_tuple = tuple(sample.values())
                    if sample_tuple in list(valid_y_num_nodup.keys()):
                        continue
                    else:
                        valid_y_num_nodup[sample_tuple] = 1
                        time_1 = time.time()
                        elapsed_time = time_1 - time_0
                        time_list.append(elapsed_time)            
        valid_y_num_list = [i for i in range(1, len(valid_y_num_nodup)+1)]
        plt.xlabel('time')
        plt.ylabel('number of valid y')
        plt.plot(time_list, valid_y_num_list)
        plt.savefig(path)
        plt.show()
        plt.close()
        return time_list
    

    def p_value_transition(self, output_path):
        t1 = int(np.dot(self.df['Y'], self.df['LI']))
        t1_y = 0
        p_dic = {}
        valid_y_list = []
        for _ in range(self.n):
            res = qa_sampler.sample(self.bqm, chain_strength = self.chain_strength, chain_break_fraction=True, num_reads=self.num_reads)
            for sample, energy, num_occurrences, chain_break_fraction in res.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
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

    
    def occurrence_hist(self, valid_y_info_dic, plot_path):
        occurrence_list = [int(valid_y_info[0]) for valid_y_info in valid_y_info_dic.values()]
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

    
    def p_value(self, valid_y_info_dic):
        t1 = int(np.dot(self.df['Y'], self.df['LI']))
        LI = list(self.df['LI'])
        p_num = 0
        
        for valid_y_tu in list(valid_y_info_dic.keys()):
            valid_y = list(valid_y_tu)
            if t1 == int(np.dot(valid_y, LI)):
                p_num += 1
        valid_y_num = len(valid_y_info_dic)
        if valid_y_num > 0:
            return p_num/valid_y_num