#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd                                         
import numpy as np                                              
from scipy.special import comb                                      
import math
from operator import mul 
import itertools                                                        
import random                                                           
import matplotlib.pyplot as plt                                         
import timeit
import time
from itertools import combinations, product


# In[2]:


def calc_marginals(df):                   
    return np.array([                      
        sum(df['Y']),     
        np.dot(df['Y'], df['SEX']),      
        np.dot(df['Y'], df['AOP']),      
    ])                               


# In[3]:


def find_valid_y(df, num_reads):    
    t_list = calc_marginals(df)                                                                      
        
    valid_y_list = []                                                           
    valid_y_num = 0
    y_lists = np.random.randint(2, size=(num_reads, df.shape[0]))
    for canditate_y in y_lists:                                                     
        if sum(canditate_y) == t_list[0]:#int同士の比較                      
            for j in range(1, len(t_list)):
                if np.dot(df.iloc[:, j+1], canditate_y) != t_list[j]:
                    break                                                       
            else:
                canditate_y_list = list(canditate_y)
                if len(valid_y_list)==0:
                    valid_y_num += 1                                        
                    valid_y_list.append(canditate_y_list)

                elif all([canditate_y_list != p for p in valid_y_list]):
                    valid_y_num += 1                                    
                    valid_y_list.append(canditate_y_list)
                    
                            
    return valid_y_list, valid_y_num                                                                                                                                          


# In[4]:


def y_num_hist(df, num_reads, path):
    LI = list(df['LI'])
    hist_dic = {}
    valid_y_list, valid_y_num = find_valid_y(df, num_reads)
    for valid_y in valid_y_list:
        t1 = int(np.dot(LI, valid_y))
        if t1 in hist_dic.keys():
            hist_dic[t1] += 1
        else:
            hist_dic[t1] = 1
            
    plt.xlabel('value of t1')
    plt.ylabel('number of samples')
    plt.bar(hist_dic.keys(), hist_dic.values())
    plt.savefig(path)
    plt.show()

    return valid_y_list, valid_y_num, hist_dic


# In[5]:


def time_num_y(df, num_reads, path):
    time_list = []
    time_0 = time.time() 
    
    t_list = calc_marginals(df)                                                                      
    valid_y_list = []                                                           
    valid_y_num = 0
    y_lists = np.random.randint(2, size=(num_reads, df.shape[0]))
    for canditate_y in y_lists:                                                     
        if sum(canditate_y) == t_list[0]:#int同士の比較                      
            for j in range(1, len(t_list)):
                if np.dot(df.iloc[:, j+1], canditate_y) != t_list[j]:
                    break                                                       
            else:
                canditate_y_list = list(canditate_y)
                #print(canditate_y_list)
                if len(valid_y_list)==0:
                    valid_y_num += 1                                        
                    valid_y_list.append(canditate_y_list)
                    time_1 = time.time()
                    elapsed_time = time_1 - time_0
                    time_list.append(elapsed_time)

                elif all([canditate_y_list != p for p in valid_y_list]):
                    valid_y_num += 1                                    
                    valid_y_list.append(canditate_y_list)
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


# In[6]:


def time_measurement(df):
    sum_time = 0
    time_once = timeit.timeit("np.random.randint(2, size=(num_reads, df.shape[0]))", globals=globals(), number=1)
    sum_time += time_once
    return sum_time


# In[7]:


#==========
#テストコード
#==========
def test_find_valid_y():
    df = pd.read_csv('../../input/ost16.csv', sep=',', index_col=0)
    valid_y_list, valid_y_num = find_valid_y(df,  num_reads = 1000)
    print(valid_y_list, valid_y_num)
    assert valid_y_num> 0  


# In[8]:


def test_validity():
    df1 = pd.read_csv('../../input/ost6.csv', sep=',',index_col=0)
    df2 = pd.read_csv('../../input/ost6.csv', sep=',',index_col=0)
    new_y = np.array([1, 0, 0, 0, 0, 1])
    df2['Y'] = new_y
    t_list1 = calc_marginals(df1)
    t_list2 = calc_marginals(df2)
    print(t_list1)
    print(t_list2)
    
    assert np.all(t_list1[[0,2]] == t_list2[[0,2]]) 


# In[ ]:




