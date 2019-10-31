#!/usr/bin/env python
# -*- coding: utf-8 -*-#


from algos.v1 import *

edges = [[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 6], [3, 7], [3, 8], [4, 8], [4, 9], [5, 10], [9, 12],
         [6, 10],
         [6, 11], [7, 10], [7, 11], [7, 12], [8, 11], [8, 12], [10, 13], [11, 14], [11, 15], [12, 16], [10, 11],
         [11, 12]]

# creation du graph
G = nx.Graph()
G.add_edges_from(edges)

print("G edges : ", G.number_of_edges())
print("G degree : ", G.degree())

# calculate a connected dominating set
cds = MCDS(G)
print("cds : ", len(cds))
print("cds : ", cds)
