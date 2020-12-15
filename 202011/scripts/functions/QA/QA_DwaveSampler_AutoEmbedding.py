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

#繰り返さない！
dw_sampler = DWaveSampler(
        endpoint="https://cloud.dwavesys.com/sapi",
        solver = 'DW_2000Q_6',
        token = "TOKY-1319d5c52b9aa35f34b40feba0cea58a4f5d3c09",
        retry_interval=5
    )
# インスタンス作成
qa_sampler = AutoEmbeddingComposite(dw_sampler)

def calc_marginals(df):
        return np.array([                      
                sum(df['Y']), #0
                np.dot(df['Y'], df['SEX']),      #1
                np.dot(df['Y'], df['AOP']),    #2  
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

    #lin
    lin_list = [sum(lin) for lin in zip(lin_Y, lin_SEX, lin_AOP)]
    lin = {i: lin_list[i] for (i, _) in dup_list}

    #quad
    quad_values = [sum(quad) for quad in zip(quad_Y, quad_SEX, quad_AOP)]
    quad = {ij: quad_values[n] for (n, ij) in enumerate(comb_list)}

    #num
    num = num_Y + num_SEX + num_AOP

    return dimod.BinaryQuadraticModel(lin, quad, num, dimod.Vartype.BINARY)#dic, dic, num


#time_once = timeit.timeit("make_Hamiltonian(df)", globals=globals(), number=1)


class QA_DSampler_AEmbedding:
    def __init__(self, df, chain_strength, num_reads, t_list, bqm, n, time_once):
        self.df = df
        self.chain_strength = chain_strength
        self.num_reads = num_reads
        self.t_list = t_list
        self.bqm = bqm
        self.n = n
        self.time_once = time_once
    
    def find_valid_y_ntimes(self):
        df_list_list = []
        for _ in range(self.n):
            res = qa_sampler.sample(self.bqm, chain_strength=self.chain_strength, chain_break_fraction=True, num_reads=self.num_reads)
            for sample, energy, num_occurrences, chain_break_fraction in res.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
                df_list_list.append([list(sample.values()), energy, num_occurrences, chain_break_fraction])

        valid_y_info_list = []
        valid_y_num = 0    
        for df_list in df_list_list:
            if df_list[1] == 0.0:
                valid_y_num += 1                                        
                valid_y_info_list.append(df_list)

        return  valid_y_info_list, valid_y_num


    def occurance_hist(valid_y_info_list, plot_path):
        occurance_list = [valid_y_info[2] for valid_y_info in valid_y_info_list]
        plt.xlabel('each sample')
        plt.ylabel('number of the occurence')
        plt.bar(x, occurance_list)
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        plt.savefig(plot_path)
        plt.show()

        return occurance_list
    
    def make_result_df(valid_y_info_list, save_path):
        cols = ['sample', 'energy', 'num_occurrences', 'chain_break_fraction']
        valid_y_info_df = pd.DataFrame(index=[], columns=cols)

        for valid_y_info in valid_y_info_list:
            if all(valid_y_info[0] != p for p in valid_y_info_df['sample'].values.tolist()):
                record = pd.Series(valid_y_info, index=valid_y_info_df.columns)
                valid_y_info_df = valid_y_info_df.append(record, ignore_index=True)

        valid_y_info_df.to_csv(save_path)
        return valid_y_info_df


    def y_num_t1_hist(self, valid_y_info_list, plot_path):
        LI = list(self.df['LI'])
        hist_dic = {}

        for valid_y_info in valid_y_info_list:
            valid_y = valid_y_info[0]
            t1 = int(np.dot(LI, valid_y))
            if t1 in hist_dic.keys():
                hist_dic[t1] += 1
            else:
                hist_dic[t1] = 1

        x = [i for i in list(hist_dic.keys())]
        plt.xlabel('value of t1')
        plt.ylabel('number of samples')
        plt.bar(x, hist_dic.values())
        plt.xticks(x, x)
        plt.savefig(plot_path)
        plt.show()

        return hist_dic


    def time_num_y(self, path):
        time_list = []
        time_0 = time.time() 

        valid_y_list= []                                                           
        valid_y_num= 0
        for _ in range(self.n):
            res = qa_sampler.sample(self.bqm, chain_strength = self.chain_strength, chain_break_fraction=True, num_reads=self.num_reads)
            for y_info in list(res.record):
                if y_info[1]==0.:
                    if len(valid_y_list)==0:
                        valid_y_list.append(list(y_info[0]))
                        valid_y_num += 1
                        time_1 = time.time()
                        elapsed_time = time_1 - time_0
                        time_list.append(elapsed_time)

                    elif all(list(y_info[0]) != p for p in valid_y_list): 
                        valid_y_list.append(list(y_info[0]))
                        valid_y_num += 1
                        time_1 = time.time()
                        elapsed_time = time_1 - time_0
                        time_list.append(elapsed_time)

        valid_y_num_list = [i for i in range(1, valid_y_num+1)]

        plt.xlabel('time')
        plt.ylabel('number of hits')
        plt.plot(time_list, valid_y_num_list)
        plt.savefig(path)
        plt.show()

        return valid_y_list, valid_y_num_list, time_list    


    def p_value_transition(self, valid_y_info_list, output_path) :
        bqm = make_Hamiltonian(self.df)
        t1 = int(np.dot(self.df['Y'], self.df['LI']))
        t1_y = 0
        p_dic = {}

        valid_y_num= 0
        valid_y_list = []
        for _ in range(self.n):
            valid_y_info_list = []
            res = qa_sampler.sample(self.bqm, chain_strength = self.chain_strength, chain_break_fraction=True, num_reads=self.num_reads)
            for sample, energy, num_occurrences, chain_break_fraction in res.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
                valid_y_info_list.append([list(sample.values()), energy, num_occurrences, chain_break_fraction])

            for y_info in valid_y_info_list:#sample, energy, num_occurrences, chain_break_fraction
                if y_info[1]==0.:
                    valid_y = y_info[0]
                    if all(valid_y != p for p in valid_y_list):
                        valid_y_num += 1
                        valid_y_list.append(valid_y)
                        if int(np.dot(valid_y, list(self.df['LI'])))==t1:
                            t1_y += 1
                            p_dic[valid_y_num] = t1_y/valid_y_num

        plt.xlabel('number of hits')
        plt.ylabel('p value')
        plt.plot(list(p_dic.keys()), list(p_dic.values()))
        plt.savefig(output_path)
        plt.show()

        return valid_y_num, valid_y_list, p_dic
    
    def time_measurement(self):
        annealing_times = 20*10**-6*self.n
        sum_time = annealing_times + self.time_once
        return sum_time