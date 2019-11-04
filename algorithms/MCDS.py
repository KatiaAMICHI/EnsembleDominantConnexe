#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
import networkx as nx
import operator
import copy


def MCDS(G):
    """
    algorithm qui permet de trouver un ensemble dominant connexe.
    :param G: graphe en entrée
    :return: NMDS de G
    """
    if not nx.is_connected(G):
        return -1

    G2 = copy.deepcopy(G)
    n = max(dict(G2.degree()).items(), key=operator.itemgetter(1))[0]
    mcds = {n}

    neighbNsort = list(map(lambda x: x[0],
                                     sorted(dict(G2.degree(G2.neighbors(n))).items(),
                                            key=operator.itemgetter(1),
                                            reverse=True)
                                     )
                                 )
    Q = deque(neighbNsort)
    insertedNode = set(list(neighbNsort) + [n])

    while Q:
        u = Q.pop()
        G_copy = copy.deepcopy(G2)
        G_copy.remove_node(u)

        if nx.is_connected(G_copy):
            G2.remove_node(u)
        else:
            mcds.add(u)
            insertNeighbNort = sorted(dict(G2.degree(set(G2.neighbors(u)) - insertedNode)).items(),
                                      key=operator.itemgetter(1),
                                      reverse=True)

            insertNeighbNort = list(map(lambda x: x[0], insertNeighbNort))
            Q.extend(insertNeighbNort)
            insertedNode.update(insertNeighbNort)

    if not nx.is_dominating_set(G, mcds) and not nx.is_connected(G.subgraph(mcds)):
        return -1

    return mcds
