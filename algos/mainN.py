#!/usr/bin/env python
# -*- coding: utf-8 -*-#


from algos.EnsembleDSageM import getEdges, MISinFile
from algos.v1 import *
import sys
import os

# add the parent directory ../../ to PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

filename = '../input2.points'
filename = '../input.points'
f = open(filename)

# creation du graph
G = nx.Graph()
vertices = f.read().splitlines()

res = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), vertices))

# un id pour chaque noeud { id : Point(x,y) ....}
verticesIdP = dict(enumerate(res, 0))

edges, b, matrixAdj = getEdges(verticesIdP)
G.add_edges_from(edges)
print("G edges : ", G.number_of_edges())
print("G degree : ", G.degree())

# calculate a connected dominating set
cds = min_connected_dominating_sets_non_distributed(G)
print("cds : ", len(cds))

# draw the graph
out_file = 'florentine_families_graph_cds_non_distributed.png'
# PlotGraph.plot_graph(G, filename=out_file, colored_nodes=cds)

# MISinFile(list(cds), verticesIdP)
