#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt

def make_result_list(matmar_path):
    with open(matmar_path) as f:
        l_strip = [[s.strip()] for s in f.readlines()]
        result_num = int(l_strip[0][0][:-(2+1)])
        result_list = []
        for i in range(1, result_num+1):
            int_y = [int(l_strip[i][0].split()[j]) for j in range(len(l_strip[i][0].split()))]
            result_list.append(int_y)
    return result_list

#result_list = make_result_list(matmar_path)

def make_canditate_y(result_list, canditate_y):
    i = random.randrange(len(result_list))
    this_time_y = result_list[i]
    j = random.randrange(2)
    if j==1:
        canditate_y = [x + y for (x, y) in zip(canditate_y, this_time_y)]
    else:
        canditate_y = [x - y for (x, y) in zip(canditate_y, this_time_y)]
    return canditate_y

def calculate_energy(df, y):
    series_y = pd.Series(y)
    E_dot = (sum(y) - sum(df['Y']))**2 
    + (np.dot(series_y, df['SEX']) - np.dot(df['Y'], df['SEX']))**2 
    + (np.dot(series_y, df['AOP']) - np.dot(df['Y'], df['AOP']))**2

    E_num = sum([0 if each_y==1 or each_y ==0 else 1 for each_y in y])  
    return E_dot + E_num

##########################################################################
class make_samples_using_markov_basis:
    def __init__(self, df, matmar_path, result_list):
        self.df = df
        self.matmar_path = matmar_path
        self.result_list = result_list


    def random(self, num):
        ori_y = list(self.df['Y'])
        #print('len(result_list)=', len(self.result_list))
        valid_y = [ori_y]
        #print('start', ori_y)
        for _ in range(num):
            i = random.randrange(len(self.result_list))
            this_time_y = self.result_list[i]
            canditate_y = [x + y for (x, y) in zip(valid_y[-1], this_time_y)]
            while calculate_energy(self.df, canditate_y)==0 and all(canditate_y != pp for pp in valid_y): 
                    valid_y.append(canditate_y)
                    #print('new valid_y ==', canditate_y)
                    #print('this_time_y == +', this_time_y)
                    canditate_y = [x + y for (x, y) in zip(valid_y[-1], this_time_y)]

            else:
                canditate_y = [x - y for (x, y) in zip(valid_y[-1], this_time_y)]
                while calculate_energy(self.df, canditate_y)==0 and all(canditate_y != pp for pp in valid_y):
                        valid_y.append(canditate_y)
                        #print('new valid_y ==', canditate_y)
                        #print('this_time_y == -', this_time_y)
                        canditate_y = [x - y for (x, y) in zip(valid_y[-1], this_time_y)]

                else:
                    #print('next')
                    continue

        #print('finish')
        return valid_y


    def SA(self, MCMC_steps):
        T_list = [i for i in reversed(range(1, MCMC_steps))]
        E_list = [0]
        valid_y = [list(self.df['Y'])]
        for i in range(len(T_list)):
            canditate_y = make_canditate_y(self.result_list, valid_y[-1])
            E_canditate = calculate_energy(self.df, canditate_y) 
            E_list.append(calculate_energy(self.df, canditate_y)) 

            transition_rate = 1
            delta = E_canditate - E_list[-1]
            if  delta > 0:
                transition_rate = math.exp(-1/T_list[i]*delta) 
            R = np.random.uniform(0.0, 1.0)

            if R < transition_rate:
                if E_list[-1]==0 and all(canditate_y != pp for pp in valid_y): 
                    valid_y.append(canditate_y)

        return E_list, valid_y


    
################################################################    
def Temp_num_plot(max_temp, i_list, valid_y_num, output_path):
    plt.xlabel('temperature')
    plt.ylabel('number of valid y')
    T_list = [i for i in reversed(range(1, max_temp))]
    x = [T_list[i] for i in i_list]
    plt.plot(x, valid_y_num)
    plt.savefig(output_path)
    return plt.show()


def result_plot(E_list, save_plot): 
    plt.xlabel('steps')
    plt.ylabel('energy')
    x = [i for i in range(len(E_list))]
    plt.plot(x, E_list)
    plt.savefig(save_plot)
    return plt.show()


def y_num_t1_hist(df, valid_y_list, plot_path):
    LI = list(df['LI'])
    hist_dic = {}

    for valid_y in valid_y_list:
        t1 = int(np.dot(LI, valid_y))
        if t1 in hist_dic.keys():
            hist_dic[t1] += 1
        else:
            hist_dic[t1] = 1

    x = [i for i in list(hist_dic.keys())]
    y = [j for j in list(hist_dic.values())]
    plt.xlabel('value of t1')
    plt.ylabel('number of samples')
    plt.xticks(x, x)
    plt.yticks(y, y)
    plt.bar(x, y)
    
    plt.savefig(plot_path)
    plt.show()
    
    return hist_dic

def p_value(df, valid_y_list):
    LI = list(df['LI'])
    p_num = 0

    for valid_y in valid_y_list:
        if int(np.dot(LI, valid_y)) == int(np.dot(LI, df['Y'])):
            p_num += 1
    
    return p_num/len(valid_y_list)


## usage example ##
#valid_y = ms.random1(10000)
#print('valid_y=', valid_y)
#print('len(valid_y)=', len(valid_y))
#hist_dic = markov_samples.y_num_t1_hist(df, valid_y, "../../output/4ti2/markov/markov_basis_ost25_random1_10000_t_num")
#hist_dic
