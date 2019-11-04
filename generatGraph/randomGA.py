#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

from algorithms.GraphMethod import getDis
from generatGraph.generateGeoGraph import dataToFile

a = 25214903917
c = 11
m = 2 ** 48


def rand48(n):
    return (a * n + c) % m


def rand48Opti(n):
    if n < 2 ** 40:
        return rand48(n + 2 ** 40)
    return rand48(n)


def randomGA(n):
    valR = rand48(n)
    len_valR = math.floor(math.log10(valR))

    # on choisi 4 chiffre aléatoire
    idx_1 = random.randint(0, len_valR - 3)

    idx_2 = idx_1
    while idx_2 == idx_1:
        idx_2 = random.randint(0, len_valR - 3)

    idx_2 = idx_1
    while idx_2 == idx_1:
        idx_2 = random.randint(0, len_valR - 3)

    idx_3 = idx_1
    while idx_3 == idx_1 or idx_3 == idx_2:
        idx_3 = random.randint(0, len_valR - 3)

    intVal = int(str(valR)[idx_1] + str(valR)[idx_2] + str(valR)[idx_3])

    # récupérer le chifre générer et on choisi 4 chiffre aléatoire
    r_intVal = rand48Opti(intVal)

    idx_1 = random.randint(0, len_valR - 3)

    idx_2 = idx_1
    while idx_2 == idx_1:
        idx_2 = random.randint(0, len_valR - 3)

    idx_2 = idx_1
    while idx_2 == idx_1:
        idx_2 = random.randint(0, len_valR - 3)

    idx_3 = idx_1
    while idx_3 == idx_1 or idx_3 == idx_2:
        idx_3 = random.randint(0, len_valR - 3)

    gen_intVal = int(str(r_intVal)[idx_1] + str(r_intVal)[idx_2] + str(r_intVal)[idx_3])

    return gen_intVal


def getEdges(points, d):
    edges = set()

    for u in points.keys():
        for v in points.keys():
            if u == v:
                continue
            dis = getDis(points, u, v)
            if dis < (d * d):
                if u < v:
                    edges.add((u, v))
                else:
                    edges.add((v, u))
    return list(edges)


def random_geometric_graph_networkx_file(nbNode, d):
    pos = defaultdict()
    for n in range(1, nbNode):
        x = randomGA(n)
        y = randomGA(x)
        pos[n] = [x, y]

    print(pos)
    edges = getEdges(pos, d)

    G = nx.Graph()
    G.add_nodes_from(pos.keys())
    G.add_edges_from(edges)

    return G


def plotGraph(G):
    pos = nx.get_node_attributes(G, 'pos')

    # find node near center (0.5,0.5)
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d

    # color by path length from node near center
    p = dict(nx.single_source_shortest_path_length(G, ncenter))

    plt.figure(figsize=(8, 8))
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=list(p.keys()),
                           node_size=80,
                           node_color=list(p.values()),
                           cmap=plt.cm.Reds_r)

    plt.xlim(-0.05, 1.05 * 1000)
    plt.ylim(-0.05, 1.05 * 1000)
    plt.axis('off')
    plt.show()


def randomGeoGraphGA():
    d = 70

    for i in range(0, 20):
        for e in range(50, 101):
            if e in range(700, 950):
                d = 60
            if e >= 950:
                d = 55
            nbNode = e * 10
            G = nx.random_geometric_graph(nbNode, d)

            while not nx.is_connected(G):
                G = nx.random_geometric_graph(nbNode, d)

            pos = nx.get_node_attributes(G, 'pos')

            print(">>> nx.is_connected(G) : ", nx.is_connected(G))

            dataToFile("../res/GADB/tests" + str(i) + "_" + str(nbNode) + ".point", pos.values(), nbNode, d)


randomGeoGraphGA()
