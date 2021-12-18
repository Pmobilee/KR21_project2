import BNReasoner
import random
import os
import networkx as nx
import pandas as pd
import time
import BayesNet

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






list_networks = os.listdir('net15')
cwd = os.getcwd()
heuristics = ["random"]

num_list = []
size_list = []
random_list = []
mindegree_list = []
minfill_list = []
runtime_list = []
num = 0
for network in list_networks:

    G = nx.read_gpickle(f'{cwd}/net15/{network}')
    g = BNReasoner.BNReasoner(net=G)
    variables = g.bn.get_all_variables()
    if "p" in variables:
        g.bn.del_var('p')
        variables = g.bn.get_all_variables()
    queries, evidence = create_query_evidence(variables)
    for heuristic in heuristics:
        start_time = time.time()
        g.MAP(queries,evidence,heuristic)
        end_time = time.time() - start_time
        if heuristic == "random":
            random_list.append(end_time)
        if heuristic == "min_degree":
            mindegree_list.append(end_time)
        if heuristic == "min_fill":
            minfill_list.append(end_time)
    size_list.append(len(variables))
    num_list.append(num)
    num+=1
    data_end = pd.DataFrame(
        {'num': num_list, 'runtime random': random_list, 'runtime min_degree': mindegree_list, "runtime min_fill": minfill_list,
         "size": size_list})
    data_end.to_csv('net15.csv')

