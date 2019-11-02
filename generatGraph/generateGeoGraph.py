import copy

import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx

Dataset = "NetworkxSet"
path = "../" + Dataset + "/"
NBFILES = 4


def dataToFile(file, result):
    with open(file, 'w') as f:
        for line in result:
            f.write(str(line[0]) + " " + str(line[1]) + "\n")


def random_geometric_graph_networkxV1():
    d = 55

    for nb in range(NBFILES):
        nbNode = 400

        if nb in range(0, 1):
            # ok
            d = 125
            nbNode = 500

        if nb in range(1, 2):
            d = 80
            nbNode = 500

        if nb in range(2, 3):
            # ok
            d = 100
            nbNode = 700

        if nb in range(3, 4):
            d = 55
            nbNode = 1000

        G = nx.random_geometric_graph(nbNode, d * 10)

        print("nx.is_connected(G) : ", nx.is_connected(G))
        while not nx.is_connected(G):
            G = nx.random_geometric_graph(500, d * 10)

        pos = nx.get_node_attributes(G, 'pos')
        print("pos : ", pos.values())

        dataToFile("tests0.txt", pos.values())


def random_geometric_graph_networkx():
    d = 100
    nbPoint = 700

    G = nx.random_geometric_graph(nbPoint, d)

    print("nx.is_connected(G) : ", nx.is_connected(G))
    while not nx.is_connected(G):
        G = nx.random_geometric_graph(nbPoint, d)

    pos = nx.get_node_attributes(G, 'pos')
    print("pos : ", pos.values())
    print(">>> nx.is_connected(G) : ", nx.is_connected(G))

    dataToFile("tests0.txt", pos.values())
    # position is stored as node attribute data for random_geometric_graph

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


def randomGeoGraphAG():
    nbNode = 500
    distance = 0.55

    # create graph
    G = nx.Graph()
    # ajouter des noeuds
    G.add_nodes_from(nbNode)

    G_copy = copy.deepcopy(G)

    # pour chaque sommet
    for v in nbNode:
        # on doir lui donner une position(x,y) quon doit généré avec les trouve de AG
        # et a chaque foit faut vérifeir si le noeud généré est connecter au graph
        pass

    print("nx.is_connected(G) : ", nx.is_connected(G))


random_geometric_graph_networkx()
