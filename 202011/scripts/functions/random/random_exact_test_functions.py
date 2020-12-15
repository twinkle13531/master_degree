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
        np.dot(df['Y'], df['LI']),      
        np.dot(df['Y'], df['SEX']),      
        np.dot(df['Y'], df['AOP']),      
    ])                               

def find_valid_y(df, num_reads):    
    t_list = calc_marginals(df)
    
    valid_y_list = {}                                                                   
    valid_y_num = {}                                                                    
    for t1 in range(0, sum(df['LI'])+1):                                              
        y_lists = np.random.randint(2, size=(num_reads, df.shape[0])) #random                                                           
        valid_y_list[t1] = []                                                           
        valid_y_num[t1] = 0                                                             
        for canditate_y in y_lists:                                                     
            if sum(canditate_y) == t_list[0]:#int同士の比較                                               
                if np.dot(df['LI'], canditate_y) == t1:#int同士の比較                       
                    for j in range(2, len(t_list)):
                        if np.dot(df.iloc[:, j], canditate_y) != t_list[j]:
                            break                                                       
                    else:
                        canditate_y_list = list(canditate_y)
                        if len(valid_y_list[t1])==0:
                            valid_y_num[t1] += 1                                        
                            valid_y_list[t1].append(canditate_y_list)                    
                            #print('perfect')
                    
                        elif all([canditate_y_list != p for p in valid_y_list[t1]]):
                            valid_y_num[t1] += 1                                    
                            valid_y_list[t1].append(canditate_y_list)                  
                            #print('perfect')
                    
                            
    return valid_y_list, valid_y_num


def y_num_t1_hist(valid_y_num, plot_path):
    x = [i for i in range(max(valid_y_num.keys()) +1)]
    plt.xlabel('value of t1')
    plt.ylabel('number of samples')
    plt.bar(x, valid_y_num.values())
    plt.xticks(x, x)
    plt.savefig(plot_path)
    return plt.show()
    

def p_value_transition(df, num_reads, output_path) :
    t1 = int(np.dot(df['Y'], df['LI']))
    t1_y = 0
    p_dic = {}
    t_list = calc_marginals(df)
    valid_y_num= 0
    valid_y_list = []
    y_lists = np.random.randint(2, size=(num_reads, df.shape[0])) #random                                
    for canditate_y in y_lists:                                                     
        if sum(canditate_y) == t_list[0]:#int同士の比較                      
            for j in range(2, len(t_list)):
                if np.dot(df.iloc[:, j], canditate_y) != t_list[j]:
                    break                                                       
            else:
                canditate_y_list = list(canditate_y)
                if all([canditate_y_list != p for p in valid_y_list]):
                    valid_y_num += 1
                    valid_y_list.append(canditate_y_list)
                    if int(np.dot(canditate_y_list, list(df['LI'])))==t1:
                        t1_y += 1
                        p_dic[valid_y_num] = t1_y/valid_y_num

    plt.xlabel('number of hits')
    plt.ylabel('p value')
    plt.plot(list(p_dic.keys()), list(p_dic.values()))
    plt.savefig(output_path)
    plt.show()
    return valid_y_num, valid_y_list, p_dic

    
def time_num_y(df, num_reads, path):
    time_list = [0]
    time_0 = time.time()
    t_list = calc_marginals(df)
    valid_y_list = []
    valid_y_num_list = [0]                                  
    y_lists = np.random.randint(2, size=(num_reads, df.shape[0])) #random                                
    for canditate_y in y_lists:                                                     
        if sum(canditate_y) == t_list[0]:#int同士の比較                      
            for j in range(2, len(t_list)):
                if np.dot(df.iloc[:, j], canditate_y) != t_list[j]:
                    break                                                       
            else:
                canditate_y_list = list(canditate_y)
                if all([canditate_y_list != p for p in valid_y_list]):
                    valid_y_list.append(canditate_y_list)
                    valid_y_num_list.append(valid_y_num_list[-1]+1)
                    time_1 = time.time()
                    elapsed_time = time_1 - time_0
                    time_list.append(elapsed_time)
    
    plt.xlabel('time')
    plt.ylabel('number of hits')
    plt.plot(time_list, valid_y_num_list)
    plt.savefig(path)
    plt.show()
    return valid_y_list, valid_y_num_list, time_list    