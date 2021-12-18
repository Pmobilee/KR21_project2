from typing import Union
from typing_extensions import runtime
from BayesNet import BayesNet
import BNReasoner
import os
import ordering
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


cwd = os.getcwd()

NET_SIZES = [15, 25]
ALGORITHMS = ['MAP']
HEURISTICS = ['min_degree']


def create_query_evidence(variables):
    number_evidence = int(len(variables)*0.1)
    number_query = int(number_evidence * 2)
    queries = random.sample(variables,number_query)
    for item in queries:
        variables.remove(item)
    evidence = random.sample(variables, number_evidence)
    evidence_dict = pd.Series({})
    for item in evidence:
        a = bool(random.getrandbits(1))
        evidence_dict[item] = a
    return queries,evidence_dict



all_runtimes = []



for algorithm in range(len(ALGORITHMS)):
    current_algorithm = ALGORITHMS[algorithm]
    print('Running', current_algorithm)

    for heuristic in range(len(HEURISTICS)):
        current_heuristic = HEURISTICS[heuristic]
        print('Running', current_heuristic, 'on', current_algorithm)

        size_runtime_dict = {}
        size_list = []
        for i in range(len(NET_SIZES)):
            size = NET_SIZES[i]
            directory = f'{cwd}/net{size}'
            runtimes = []


            for filename in os.listdir(directory):
                GRAPH = nx.read_gpickle(f'{directory}/{filename}')
                g = BNReasoner.BNReasoner(net=GRAPH)


                variables = g.bn.get_all_variables()
                if "p" in variables:
                    g.bn.del_var('p')
                    variables = g.bn.get_all_variables()
                queries, evidence = create_query_evidence(variables)
                
                if current_algorithm == 'MAP':
                    start_time = time.time()
                    g.MAP(queries,evidence,heuristic)
                    end_time = time.time() - start_time
                else:
                    pass
                runtimes.append(end_time)
                size_list.append(size)
                

        data_end = pd.DataFrame(
            {'size': size_list, "runtime": runtimes})
        data_end.to_csv(f'{current_algorithm}_{current_heuristic}.csv')



