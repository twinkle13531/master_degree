#!/usr/bin/env python
# coding: utf-8
import pandas as pd                                         
import numpy as np                                          
import random                                                           
import matplotlib.pyplot as plt                                         
import timeit
import time
import math

#t_list = calc_marginals(df)

class make_variables:
    def __init__(self, df, Max_temper, MCMC_step, MCMC_step_each):
        self.df = df
        self.Max_temper = Max_temper
        self.MCMC_step = MCMC_step
        self.MCMC_step_each = MCMC_step_each
        
    def calc_marginals(self):
        return np.array([                      
        sum(self.df['Y']),                     
        np.dot(self.df['Y'], self.df['LI']),  #1    
        np.dot(self.df['Y'], self.df['SEX']),      
        np.dot(self.df['Y'], self.df['AOP']),      
    ])
    
    def each_energy(self, canditate_y):
        t_list = self.calc_marginals()
        ysum = (sum(canditate_y) - t_list[0])**2
        feature_sum = sum([(np.dot(self.df.iloc[:, j], canditate_y) - t_list[j])**2 for j in range(2, len(t_list))])
        return ysum + feature_sum

    def Montecarlo(self, T):    
        num_sample = len(self.df)
        y = self.df['Y']
        y_list = []
        y_list.append(y)
        E_list = []
        E_list.append(0)
        for j in range(self.MCMC_step):    
            i = random.randrange(num_sample)
            ori_yi = y[i]
            y[i] = 1 - y[i]
            if np.all(y == 1) or np.all(y == 0):
                continue
            E_now = self.each_energy(y)
            E_last = E_list[-1]
            r = math.exp(-(E_now-E_last)/T) #温度付き
            R = np.random.uniform(0.0, 1.0)
            if R > r :
                y[i] = ori_yi   
            else:
                E_list.append(E_now)
                y_list.append(y)
        return E_list, y_list


    def mcmc_find_valid_y(self, T):
        E_list, y_list = self.Montecarlo(T)
        valid_y_dic = {}#sample:occurrence_count
        for E, y in zip(E_list, y_list)      :
            if E==0.:
                tup_y = tuple(y)
                if tup_y in list(valid_y_dic.keys()):
                    valid_y_dic[tup_y] += 1
                else:
                    valid_y_dic[tup_y] = 1
        return valid_y_dic

    def Montecarlo_for_replica(self, y, T):
        num_sample = len(self.df)
        t_list = self.calc_marginals()
        y_list = []
        y_list.append(y)#前回の
        E_list = []
        E_list.append(self.each_energy(y))#前回の
        for j in range(self.MCMC_step_each):##  
            i = random.randrange(num_sample)
            ori_yi = y[i]
            y[i] = 1 - y[i]
            if np.all(y == 1) or np.all(y == 0):
                continue
            E_now = self.each_energy(y)
            E_last = E_list[-1]
            r = math.exp(-(E_now-E_last)/T) #温度付き
            R = np.random.uniform(0.0, 1.0)
            if R > r :
                y[i] = ori_yi   
            else:
                E_list.append(E_now)
                y_list.append(y)
        del E_list[0]
        del y_list[0]
        return E_list, y_list

    
    def replica_mcmc(self):
        T = [j for j in range(1, self.Max_temper+1)]
        len_T = len(T)
        b = [1/ l for l in T]
        num_sample = len(self.df)
        y = self.df['Y']#series

        E_Y_dic = {t:[] for t in T}
        for ii in range(int(self.MCMC_step/self.MCMC_step_each)):
            if ii != 0:
                for t in T:#それぞれの温度に対して
                    E_list, y_list = self.Montecarlo_for_replica(E_Y_dic[t][-1][1][-1], t)
                    E_Y_dic[t].append([E_list, y_list])
                    print('here{}'.format(ii))
            else:
                for t in T:#それぞれの温度に対して
                    E_list, y_list = self.Montecarlo_for_replica(y, t)
                    E_Y_dic[t].append([E_list, y_list])
                    print('here{}'.format(ii))

            tt0 = random.randrange(1, len_T)
            tt1 = random.randrange(1, len_T)
            r = math.exp((b[tt1]-b[tt0])* (E_Y_dic[tt1][-1][0][-1]-E_Y_dic[tt0][-1][0][-1]))
            if 1 <= r:
                E_Y_dic[tt1][-1][0][-1], E_Y_dic[tt0][-1][0][-1] = E_Y_dic[tt0][-1][0][-1], E_Y_dic[tt1][-1][0][-1]#eの交換
                E_Y_dic[tt1][-1][1][-1], E_Y_dic[tt0][-1][1][-1] = E_Y_dic[tt0][-1][1][-1], E_Y_dic[tt1][-1][1][-1]#該当するyの交換
        
            
    def replica_mcmc_find_valid_y(self):    
        E_Y_dic = self.replica_mcmc()
        valid_y_dic = {}#sample:occurrence_count
        for t in T:
            for ii in len(E_Y_dic[t]):
                for jj in len(E_Y_dic[t][ii][0]):
                    if E_Y_dic[t][ii][0][jj]==0.:
                        tup_y = tuple(E_Y_dic[t][ii][1][jj])
                        if tup_y in list(valid_y_dic.keys()):
                            valid_y_dic[tup_y] += 1
                        else:
                            valid_y_dic[tup_y] = 1
        return valid_y_dic

