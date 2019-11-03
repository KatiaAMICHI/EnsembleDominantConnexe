#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import operator
from collections import deque
import networkx as nx


def MCDS(G):
    # print("nx.is_connected(G) : ", nx.is_connected(G))
    if not nx.is_connected(G):
        return -1

    G2 = copy.deepcopy(G)

    # prend le nœud avec le degré maximum comme nœud de départ
    init_node = max(dict(G2.degree()).items(), key=operator.itemgetter(1))[0]
    # print("starting_node  : ", init_node)

    mcds = {init_node}

    # Mettre en file d'attente les noeuds voisins du noeud de départ sur Q dans l'ordre décroissant de leur degré
    neighbor_nodes = G2.neighbors(init_node)

    a = dict(G2.degree(neighbor_nodes))

    neighbor_nodes_sorted = list(map(lambda x: x[0], sorted(a.items(), key=operator.itemgetter(1), reverse=True)))

    # une file de priorités est gérée de manière centralisée pour décider si un élément ferait partie de MCDS.
    priority_queue = deque(neighbor_nodes_sorted)
    # print("priority_queue : ", priority_queue)
    inserted_set = set(list(neighbor_nodes_sorted) + [init_node])

    i = 0
    while priority_queue:
        # print(" ...............................................................................", i)
        i += 1
        # print("* CDS: ", mcds)
        u = priority_queue.pop()
        # print("u  : ", u)

        # vérifie si le graphique après la suppression de u est toujours connecté
        rest_graph = copy.deepcopy(G2)
        rest_graph.remove_node(u)

        if nx.is_connected(rest_graph):
            # print(" >>> supp de : ", u)
            G2.remove_node(u)

        else:  # si le graph n'est pas connecté
            # print(" <<< ajout de : ", u)
            mcds.add(u)

            # ajoute les voisins de u à la file d'attente prioritaire, qui ne sont jamais insérés dans Q
            inserted_neighbors = set(G2.neighbors(u)) - inserted_set

            inserted_neighbors_sorted = sorted(dict(G2.degree(inserted_neighbors)).items(),
                                               key=operator.itemgetter(1),
                                               reverse=True)

            inserted_neighbors_sorted = list(map(lambda x: x[0], inserted_neighbors_sorted))
            # print("     1 priority_queue : ", priority_queue)
            priority_queue.extend(inserted_neighbors_sorted)
            # print("     2 priority_queue : ", priority_queue)
            # print("     1 inserted_set : ", inserted_set)
            inserted_set.update(inserted_neighbors_sorted)
            # print("     2 inserted_set : ", inserted_set)

    if not nx.is_dominating_set(G, mcds) and not nx.is_connected(G.subgraph(mcds)):
        return -1

    return mcds
