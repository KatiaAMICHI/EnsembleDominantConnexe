#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import networkx.algorithms.approximation as nxaa
from collections import deque
import copy
import operator


def min_connected_dominating_sets_non_distributed(G):
    """Compute a CDS, based on algorithm of Butenko, Cheng, Oliveira, Pardalos
        Based on the paper: BUTENKO, Sergiy, CHENG, Xiuzhen, OLIVEIRA, Carlos A., et al. A new heuristic for the minimum connected dominating set problem on ad hoc wireless networks. In : Recent developments in cooperative control and optimization. Springer US, 2004. p. 61-73.
    """
    assert nx.is_connected(G)

    G2 = copy.deepcopy(G)

    # Step 1: initialization
    # prend le nœud avec le degré maximum comme nœud de départ
    starting_node = max(dict(G2.degree()).items(), key=operator.itemgetter(1))[0]
    cds = {starting_node}

    # Mettre en file d'attente les nœuds voisins du nœud de départ sur Q dans l'ordre décroissant de leur degré
    neighbor_nodes = G2.neighbors(starting_node)

    a = dict(G2.degree(neighbor_nodes))

    neighbor_nodes_sorted = list(map(lambda x: x[0], sorted(a.items(), key=operator.itemgetter(1), reverse=True)))

    # une file de priorités est gérée de manière centralisée pour décider si un élément ferait partie de CDS.
    priority_queue = deque(neighbor_nodes_sorted)

    inserted_set = set(list(neighbor_nodes_sorted) + [starting_node])

    # Étape 2: calculer les cds
    while priority_queue:
        u = priority_queue.pop()

        # vérifie si le graphique après la suppression de u est toujours connecté
        rest_graph = copy.deepcopy(G2)
        rest_graph.remove_node(u)

        if nx.is_connected(rest_graph):
            G2.remove_node(u)

        else:  # si le graph n'est pas connecté
            cds.add(u)

            # ajoute les voisins de u à la file d'attente prioritaire, qui ne sont jamais insérés dans Q
            inserted_neighbors = set(G2.neighbors(u)) - inserted_set

            inserted_neighbors_sorted = sorted(dict(G2.degree(inserted_neighbors)).items(),
                                               key=operator.itemgetter(1),
                                               reverse=True)

            inserted_neighbors_sorted = list(map(lambda x: x[0], inserted_neighbors_sorted))

            priority_queue.extend(inserted_neighbors_sorted)
            inserted_set.update(inserted_neighbors_sorted)

    # Step 3: vérifier le result
    assert nx.is_dominating_set(G, cds) and nx.is_connected(G.subgraph(cds))

    return cds
