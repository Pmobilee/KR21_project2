from typing import Union
from typing_extensions import runtime
from BayesNet import BayesNet
import BNReasoner
import os
import random
import time
from typing import List, Tuple, Dict
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.readwrite import XMLBIFReader
import math
import itertools
import pandas as pd
from copy import deepcopy
import pickle
import gc



cwd = os.getcwd()

NET_SIZES = [5, 15, 25]
ALGORITHMS = ['MAP',"MPE"]
HEURISTICS = ['min_fill','random','min_degree']


def create_query_evidence(variables, algorithm):
    number_evidence = int(len(variables)*0.1)
    if algorithm == "MAP":
        number_query = int(number_evidence * 2)
    if algorithm == "MPE":
        number_query = 0
    queries = random.sample(variables,number_query)
    for item in queries:
        variables.remove(item)
    evidence = random.sample(variables, number_evidence)
    evidence_dict = pd.Series({})
    for item in evidence:
        a = bool(random.getrandbits(1))
        evidence_dict[item] = a
    return queries,evidence_dict




for algorithm in range(len(ALGORITHMS)):
    current_algorithm = ALGORITHMS[algorithm]
    print('Running', current_algorithm)
    size_runtime_dict = {}
    size_list = []
    runtime_degree = []
    runtime_random = []
    runtime_fill = []

    for i in range(len(NET_SIZES)):
        size = NET_SIZES[i]
        directory = f'{cwd}/net{size}'
        count = 1
        for filename in os.listdir(directory):
            print('---------', count,filename)
            count+=1
            GRAPH = nx.read_gpickle(f'{directory}/{filename}')
            g = BNReasoner.BNReasoner(net=GRAPH)
            variables = g.bn.get_all_variables()
            if "p" in variables:
                g.bn.del_var('p')
                variables = g.bn.get_all_variables()
            queries, evidence = create_query_evidence(variables, current_algorithm)
            size_list.append(size)
            for heuristic in range(len(HEURISTICS)):
                current_heuristic = HEURISTICS[heuristic]
                print('Running', current_heuristic, 'on', current_algorithm)
                start_time = time.time()
                g.MAP(queries,evidence,heuristic = current_heuristic)
                end_time = time.time() - start_time

                if HEURISTICS[heuristic] == 'random':
                    runtime_random.append(end_time)
                if HEURISTICS[heuristic] == 'min_degree':
                    runtime_degree.append(end_time)
                if HEURISTICS[heuristic] == 'min_fill':
                    runtime_fill.append(end_time)
                gc.collect()


    data_end = pd.DataFrame(
        {'size': size_list, "runtime_degree": runtime_degree, "runtime_random":runtime_random,"runtime_minfill":runtime_fill})
    data_end.to_csv(f'{current_algorithm}_{size}.csv')


