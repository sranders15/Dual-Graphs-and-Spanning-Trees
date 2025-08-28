# contains functions makeRandomLattice and ST_const

import networkx as nx
import random
import numpy as np
from numpy import linalg

def decision(probability):
    return random.random() < probability
def makeRandomLattice(sidelength,probability):
    g = nx.grid_graph([sidelength[0],sidelength[1]])
    p = probability

    for i in range(0,sidelength[1]-1):
        for j in range(0,sidelength[0]-1):
            # node is the bottom left point of a square
            # with probability p, draw a diagonal in that square
            if decision(p):
                # draw the diagonal
                # direction is chosen 50/50
                if decision(0.5):
                    # draw up right
                    g.add_edge((i,j),(i+1,j+1))
                else:
                    # draw up left
                    g.add_edge((i,j+1),(i+1,j))
    return g

# ST const
def ST_const(graph, forests = False):
    # forests = True means it will calculate spanning FORESTS for disconnected graphs
    # forests = False means it will calculate spanning trees for LARGEST connected component
    if not(forests):
        largest_cc = max(nx.connected_components(graph), key=len)
        graph = graph.subgraph(largest_cc)
    Lap = nx.laplacian_matrix(graph).toarray()
    # remove a row and column
    T = np.delete(Lap,1,0)
    T = np.delete(T,1,1)
    # determinant of T = # of spanning trees
    # we use slogdet to avoid large numbers
    # slogdet computes ln of abs value of det & sign of det
    (sign, logabsdet) = linalg.slogdet(T)
    if sign == 0:
        # i do not know why this happens
        # it has nothing to do with connectivity (?)
        return 0
    else:
        n = graph.number_of_nodes()
        ST = logabsdet/n
        return ST, n
