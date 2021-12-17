import BNReasoner
import random
import os
import networkx as nx
import pandas as pd

def create_query_evidence(variables):
    number_evidence = int(len(variables)*0.1)
    number_query = int(number_evidence * 2)
    queries = random.sample(variables,number_query)
    for item in queries:
        variables.remove(item)
    evidence = random.sample(variables, number_evidence)



list_networks = os.listdir('network')

cwd = os.getcwd()


for network in list_networks:
    G = nx.read_gpickle(f'{cwd}/network/{network}')
    g = BNReasoner.BNReasoner(net=G)

    if "p" in variables:
        g.bn.del_var('p')
        variables = g.bn.get_all_variables()
    else:
        variables = g.bn.get_all_variables()

    g.MAP([], order, pd.Series({}))
