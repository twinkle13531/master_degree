#!/usr/bin/env python
# coding: utf-8
import pandas as pd                                         
import numpy as np                                          
import random                                                           
import matplotlib.pyplot as plt                                         
import timeit
import time

def calc_marginals(df):                   
    return np.array([                      
        sum(df['Y']),                     
        np.dot(df['Y'], df['LI']),  #1    
        np.dot(df['Y'], df['SEX']),      
        np.dot(df['Y'], df['AOP']),      
    ])                               

t_list = calc_marginals(df)

#calculate_timeはこの関数を計測
def find_valid_y(df, num_reads):    
    t_list = calc_marginals(df)
    valid_y_num= 0
    valid_y_dic = {}
    time_0 = time.time()
    y_lists = np.random.randint(2, size=(num_reads, df.shape[0])) #random                                
    for canditate_y in y_lists:                                                     
        if sum(canditate_y) == t_list[0]:#int同士の比較                      
            for j in range(2, len(t_list)):
                if np.dot(df.iloc[:, j], canditate_y) != t_list[j]:
                    break                                                       
            else:
                canditate_y_tuple =tuple(canditate_y)
                if canditate_y_tuple in list(valid_y_dic.keys()):
                    valid_y_dic[canditate_y_tuple] += 1
                else:
                    valid_y_dic[canditate_y_tuple] = 1                      
    time_1 = time.time()
    calculation_time = time_1 - time_0
    return valid_y_dic, calculation_time


class Random_method:
    def __init__(self, df, valid_y_dic, num_reads, t_list):
        self.df = df
        self.valid_y_dic = valid_y_dic
        self.num_reads = num_reads
        self.t_list = t_list


    def y_num_t1_hist(self, plot_path):
        LI = list(self.df['LI'])
        t1_dic = {}
        for valid_y_tupele in self.valid_y_dic:
            valid_y = list(valid_y_tupele)
            this_time_t1 = np.dot(valid_y, LI)
            if this_time_t1 in list(t1_dic.keys()):
                t1_dic[this_time_t1] += 1
            else:
                t1_dic[this_time_t1] = 1

        x = [i for i in list(t1_dic.keys())]
        y = [j for j in list(t1_dic.values())]
        plt.xlabel('value of t1')
        plt.ylabel('number of samples')
        plt.bar(x, y)
        plt.xticks(x, x)
        plt.yticks(y, y)
        plt.show()
        plt.close()
        plt.savefig(plot_path)
        return t1_dic
    

    def p_value(self):
        t1 = int(np.dot(self.df['Y'], self.df['LI']))
        LI = list(self.df['LI'])
        p_num = 0
        for valid_y in self.valid_y_list:
            if t1 == int(np.dot(valid_y, LI)):
                p_num += 1
        if self.valid_y_num > 0:
            return p_num/self.valid_y_num
        else:
            messa = "can't calculate p value"
            return messa
    
    def p_value_transition(self, output_path):
        t1 = int(np.dot(self.df['Y'], self.df['LI']))
        LI = list(self.df['LI'])
        t1_y = 0
        p_dic = {}
        valid_y_num_ever = 0
        valid_y_list_ever = []
        y_lists = np.random.randint(2, size=(self.num_reads, self.df.shape[0])) #random                                
        for canditate_y in y_lists:                                                     
            if sum(canditate_y) == self.t_list[0]:#int同士の比較                      
                for j in range(2, len(self.t_list)):
                    if np.dot(self.df.iloc[:, j], canditate_y) != self.t_list[j]:
                        break                                                       
                else:
                    canditate_y_list = list(canditate_y)
                    if all([canditate_y_list != p for p in valid_y_list_ever]):
                        valid_y_num_ever += 1
                        valid_y_list_ever.append(canditate_y_list)
                        if int(np.dot(canditate_y_list, LI))==t1:
                            t1_y += 1
                            p_dic[t1_y] = t1_y/valid_y_num_ever
        plt.xlabel('number of hits')
        plt.ylabel('p value')
        plt.plot(list(p_dic.keys()), list(p_dic.values()))
        plt.savefig(output_path)
        plt.show()
        plt.close()
        return p_dic

    
    def time_num_y_transition(self, path):
        time_0 = time.time()
        valid_ys = []
        
        time_list = [0]
        valid_y_number = [0]                                 
        y_lists = np.random.randint(2, size=(self.num_reads, self.df.shape[0]))
        for canditate_y in y_lists:                                                     
            if sum(canditate_y) == self.t_list[0]:#int同士の比較                      
                for j in range(2, len(self.t_list)):
                    if np.dot(self.df.iloc[:, j], canditate_y) != self.t_list[j]:
                        break                                                       
                else:
                    canditate_y_list = list(canditate_y)
                    if all([canditate_y_list != p for p in valid_ys]):
                        valid_ys.append(canditate_y_list)
                        valid_y_number.append(valid_y_number[-1]+1)
                        
                        time_1 = time.time()
                        elapsed_time = time_1 - time_0
                        time_list.append(elapsed_time)

        plt.xlabel('time')
        plt.ylabel('number of hits')
        plt.plot(time_list, valid_y_number)
        plt.savefig(path)
        plt.show()
        plt.close()
        return valid_ys, time_list, valid_y_number    