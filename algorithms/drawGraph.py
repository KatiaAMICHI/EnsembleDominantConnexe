import matplotlib.pyplot as plt
import networkx as nx


def mis_i():
    edges = [[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 6], [3, 7], [3, 8], [4, 8], [4, 9], [5, 10], [9, 12],
             [6, 10],
             [6, 11], [7, 10], [7, 11], [7, 12], [8, 11], [8, 12], [10, 13], [11, 14], [11, 15], [12, 16], [10, 11],
             [11, 12]]

    G = nx.Graph()
    G.add_edges_from(edges)

    color_map = []
    for node in G:

        if node in [2, 3, 4]:
            color_map.append('grey')
        elif node in [6, 7, 8, 10, 12, 14, 15]:
            color_map.append('grey')
        elif node in [5, 9, 13, 16]:
            color_map.append('black')
        elif node in [11, 1]:
            color_map.append('black')
        else:
            color_map.append('White')

    print("color_map : ", color_map)

    pos = {1: (5, 5), 2: (4, 4), 3: (5, 4), 4: (6, 4), 5: (2.5, 3), 6: (3.5, 3), 7: (5, 3), 8: (6.5, 3),
           9: (7.5, 3),
           10: (3, 2), 11: (5, 2), 12: (7, 2), 13: (3, 1), 14: (4, 1.25), 15: (6, 1.25), 16: (7, 1)}

    nx.draw(G, node_color=color_map, with_labels=True, pos=pos, font_color='black')

    # ax.collections[0] is a PathCollection object governing the nodes
    # ax.collections[1] is a LineCollection object governing the edges if you have some.

    ax = plt.gca()  # to get the current axis
    ax.collections[0].set_edgecolor("black")
    plt.savefig("mis5.png")

    plt.show()


def MCDS():
    edges = [[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 6], [3, 7], [3, 8], [4, 8], [4, 9], [5, 10], [9, 12],
             [6, 10],
             [6, 11], [7, 10], [7, 11], [7, 12], [8, 11], [8, 12], [10, 13], [11, 14], [11, 15], [12, 16], [10, 11],
             [11, 12]]

    G = nx.Graph()
    G.add_edges_from(edges)

    color_map = []
    for node in G:

        if node in [1, 2, 5, 10, 11, 12]:
            color_map.append('green')
        else:
            color_map.append('White')

    print("color_map : ", color_map)

    pos = {1: (5, 5), 2: (4, 4), 3: (5, 4), 4: (6, 4), 5: (2.5, 3), 6: (3.5, 3), 7: (5, 3), 8: (6.5, 3),
           9: (7.5, 3),
           10: (3, 2), 11: (5, 2), 12: (7, 2), 13: (3, 1), 14: (4, 1.25), 15: (6, 1.25), 16: (7, 1)}

    # edges
    nx.draw_networkx_edges(G, pos,
                           edgelist=[(1, 2), (2, 5), (5, 10), (10, 11), (11, 12)],
                           width=8, alpha=0.5, edge_color='green')

    nx.draw(G, node_color=color_map, with_labels=True, pos=pos, font_color='black')

    # ax.collections[0] is a PathCollection object governing the nodes
    # ax.collections[1] is a LineCollection object governing the edges if you have some.

    ax = plt.gca()  # to get the current axis
    # ax.collections[0].set_edgecolor("black")
    ax.collections[1].set_edgecolor("black")
    plt.savefig("MCDS.png")

    plt.show()


MCDS()
