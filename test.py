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

t = BNReasoner.BNReasoner(net = f'{cwd}/testing/lecture_example2.BIFXML')
