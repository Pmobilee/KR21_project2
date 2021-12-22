from typing import Union
from BayesNet import BayesNet
import BNReasoner
import os
import random

from typing import List, Tuple, Dict
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.readwrite import XMLBIFReader
import math
import itertools
import pandas as pd
from copy import deepcopy


cwd = os.getcwd()


# This tests if the networks generated contain the correct amount of variables

for x in range(100):
    filenames = f'{cwd}/net25/net25_{x}gpickle'
    GRAPH = nx.read_gpickle(filenames)
    t = BNReasoner.BNReasoner(net=GRAPH)
    print(len(t.bn.get_all_variables()))

GRAPH = nx.read_gpickle(f'{cwd}/net25/net25_74gpickle')
t = BNReasoner.BNReasoner(net=GRAPH)
print(len(t.bn.get_all_variables()))