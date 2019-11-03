import copy
import random

import matplotlib.pyplot as plt
import networkx as nx

Dataset = "NetworkxSet"
path = "../" + Dataset + "/"
NBFILES = 4


def dataToFile(file, result, nbNode, d):
    with open(file, 'w') as f:
        # premiere ligne [nombre de noeud, la distance]
        f.write(str(nbNode) + " " + str(d) + "\n")

        for line in result:
            f.write(str(line[0]) + " " + str(line[1]) + "\n")


def random_geometric_graph_networkxDS():
    d = 70

    for i in range(0, 20):
        for e in range(50, 101):
            nbNode = e * 10

            if e in range(700, 950):
                d = 60
            if e >= 950:
                d = 55

            print(" ........................................................................................ ")
            G = nx.random_geometric_graph(nbNode, d)

            print("nx.is_connected(G) : ", nx.is_connected(G))
            while not nx.is_connected(G):
                G = nx.random_geometric_graph(nbNode, d)

            pos = nx.get_node_attributes(G, 'pos')
            print(">>> nx.is_connected(G) : ", nx.is_connected(G))

            dataToFile("../res/GenNetworkx/tests" + str(i) + "_" + str(e * 10) + ".point", pos.values(), e * 10, d)


def random_geometric_graph_networkx_file():
    d = 70
    nbPoint = 500

    G = nx.random_geometric_graph(nbPoint, d)

    print("nx.is_connected(G) : ", nx.is_connected(G))
    while not nx.is_connected(G):
        G = nx.random_geometric_graph(nbPoint, d)

    pos = nx.get_node_attributes(G, 'pos')
    print(">>> nx.is_connected(G) : ", nx.is_connected(G))

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
