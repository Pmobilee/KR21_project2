# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 20:12:12 2021

@author: Pablo
"""
import random
import pandas as pd
from BayesNet import BayesNet
from typing import Union
from BayesNet import BayesNet
import pandas as pd
from copy import deepcopy
import random
import networkx as nx
import os
import BNReasoner
import gc


def create_variable(net, name):
    
    
    #Select how many parents nodes the new variable will be connected to
    all_parents = net.get_all_variables()
    nr_connections = random.randint(1, len(all_parents))
    
    #Select which parents nodes are connected
    nr=[]
    parents=[]
    for i in range(nr_connections):
        new_parent = all_parents[random.randint(0,len(all_parents)-1)]
        if new_parent not in parents:
            parents.append(new_parent)
    
    #Create cpt for new variable
    cpt = {}
    
    for parent in parents:
        lista = []
        for j in range(2**parents.index(parent)):
            for i in range(2**(len(parents)-parents.index(parent))):
                lista.append(False)
            for i in range(2**(len(parents)-parents.index(parent))):
                lista.append(True)
        cpt[parent] = lista
    lista = []
    
    for i in range(2**(len(parents)+1)):
        if i%2 == 0:
            lista.append(False)
        else:
            lista.append(True)
            
    cpt[name] = lista
    
    #Add probabilities
    prob=[]
    
    for i in range(0, 2**(len(parents)+1), 2): 
        prob1 = random.uniform(0, 1)
        prob.append(prob1)
        prob.append(1-prob1)
    
    cpt['p'] = prob
    cpt = pd.DataFrame(cpt)
    connections = []
    for i in parents:
        connections.append([i, name])
    
    return cpt, connections

def add_several_variables(net, names, nr):
    for i in range(nr):
        cpt, connections = create_variable(net, names[i])
        net.add_var(names[i], cpt)
        for j in connections:
            net.add_edge(j)
    return net

for i in range(0, 100):
    net=BayesNet()
    net.load_from_bifxml('testing/dog_problem.BIFXML')
    net1=net
    names=['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'zz', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z']
    try:
        net2=add_several_variables(net1, names, 20)
    except:
        continue

    path = 'D:/OneDrive/VU/knowledge_representation/PGM/KR21_project2/net25'
    nx.write_gpickle(net2,path+'/net25_'+ str(i) +'.gpickle')
    del net, net1, net2
    gc.collect()

                