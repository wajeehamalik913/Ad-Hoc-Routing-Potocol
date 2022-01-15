from mpi4py import MPI
import numpy as np
from random import randrange
import time
import random
import sys
import re
import networkx as nx
from networkx.generators.random_graphs import erdos_renyi_graph


n = 50
p = 0.2
g = erdos_renyi_graph(n, p)
list2=list(g.edges)
print("GRAPH:", list2)
file2 = open('topology.txt', 'w')

for element in list2:
        file2.write(''.join(str(element))+'\n')

file2.close()
