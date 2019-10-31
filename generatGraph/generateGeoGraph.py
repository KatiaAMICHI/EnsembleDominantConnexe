import matplotlib.pyplot as plt
import networkx as nx
import copy


def genNetworkx():
    nbNode = 200
    distance = 0.125
    G = nx.random_geometric_graph(nbNode, distance)
    print("nx.is_connected(G) : ", nx.is_connected(G))
    # position is stored as node attribute data for random_geometric_graph
    pos = nx.get_node_attributes(G, 'pos')
    print("pos : ", pos)
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

    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.axis('off')
    plt.show()


def randomGeoGraphInt():
    nbNode = 200
    distance = 0.125

    # create graph
    G = nx.Graph()
    # ajouter des noeuds
    G.add_nodes_from(nbNode)

    G_copy = copy.deepcopy(G)

    # pour chaque sommet
    for v in nbNode:
        # on doir lui donner une position(x,y) quon doit généré avec les trouve de AG
        # et a chaque foit faut vérifeir si le noeud généré est connecter au graph

    print("nx.is_connected(G) : ", nx.is_connected(G))
