import time
from collections import defaultdict
from operator import or_
from functools import reduce
import pprint

# import pandas as pd
# from sage.all import *

d = 100
f = open("input.points")
vertices = f.read().splitlines()

res = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), vertices))

# un id pour chaque noeud { id : Point(x,y) ....}
verticesIdP = dict(enumerate(res, 0))


def getEdges(verticesIdP):
    matrixAdj = defaultdict()
    for v in verticesIdP:
        matrixAdj[v] = {"voisins": [], "label": None, "color": "blanc", "nbV": 0, "composant": False}
    edges = set()
    edgesDist = set()
    for u in verticesIdP:
        for v in verticesIdP:
            if u == v:
                continue
            dis = getDis(verticesIdP, u, v)
            if isNeighbor(verticesIdP, u, v):
                matrixAdj[u]["voisins"].append(v)
                matrixAdj[u]["nbV"] += 1

                if u < v:
                    edgesDist.add((u, v, dis))
                    edges.add((u, v))
                else:
                    edges.add((v, u))
    return list(edges), list(edgesDist), matrixAdj


def isNeighbor(verticesIdP, u, v):
    return getDis(verticesIdP, u, v) <= d * d


def getDis(verticesIdP, u, v):
    return ((verticesIdP[u][0] - verticesIdP[v][0]) * (verticesIdP[u][0] - verticesIdP[v][0]) + \
            (verticesIdP[u][1] - verticesIdP[v][1]) * (verticesIdP[u][1] - verticesIdP[v][1]))


noir = []
gris = []


def hasNNeibBlack(matrixAdj, noir, v):
    # print(" [hasNNeibBlack]")
    if len(noir) == 0:
        return True
    if matrixAdj[v]["color"] == "gris":
        return False
    # print("      matrixAdj[", v, "][color] : ", matrixAdj[v]["color"])
    for n in matrixAdj[v]["voisins"]:
        # print("         AVANT n : ", n)
        if n in noir:
            # print("       [noir] n : ", n)
            return False
        for nn in matrixAdj[n]["voisins"]:
            if nn == v:
                continue
            # print("       [noir] nn : ", nn)
            if nn in noir:
                # print("         m        atrixAdj[n][voisins]")
                return True
    return False


def MIS(matrixAdj, noir, gris):
    nbVisite = 0
    listNoeud = list(matrixAdj.keys())

    listToVisite = set()
    listToVisite.add(listNoeud[0])
    while len(listToVisite) != 0:
        v = listToVisite.pop()
        if matrixAdj[v]["color"] == "gris":
            continue
        if hasNNeibBlack(matrixAdj, noir, v):
            noir.append(v)
            matrixAdj[v]["color"] = "noir"
            nbVisite += 1
            matrixAdj[v]["label"] = "N" + str(v)

            for n in matrixAdj[v]["voisins"]:
                matrixAdj[n]["color"] = "gris"
                nbVisite += 1
                listVoisinsN = matrixAdj[n]["voisins"]
                listToVisite = reduce(or_, [listToVisite, set(listVoisinsN)])
        listToVisite = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", listToVisite))

    print("<<<<<<< noir : ", noir)


def MISV2(matrixAdj, noir, gris):
    i = 0
    # print("noir : ", noir)
    nbGris = 0
    nbNoir = 0
    listNoeud = list(matrixAdj.keys())
    noir = []
    for v in listNoeud:
        if matrixAdj[v]["color"] == "gris":
            continue
        # print("********************** FOR ***************************")
        # print(" matrixAdj[v][voisins]: ", matrixAdj[v]["voisins"])
        # print("n1 : ", v)
        if hasNNeibBlack(matrixAdj, noir, v):
            # print(">>>>>> ajou de n1 dans noir")
            noir.append(v)
            matrixAdj[v]["color"] = "noir"
            matrixAdj[v]["label"] = "N" + str(v)
            for n in matrixAdj[v]["voisins"]:
                listV = matrixAdj[n]["voisins"]
                # if n in matrixAdjCopy:
                # print("     n: ", n)
                # if not hasNNeibBlack(matrixAdj, noir, n):
                matrixAdj[n]["color"] = "gris"
    print("MISV2 <<<<<<< noir : ", noir)


def inDiffComposant(matrixAdj, v, i):
    listLabel = set()
    listNoeud = set()
    inComposant = False
    for e in matrixAdj[v]["voisins"]:
        if matrixAdj[e]["color"] == "noir":
            listLabel.add(matrixAdj[e]["label"])
            if matrixAdj[e]["composant"]:
                inComposant = matrixAdj[e]["composant"]
            # if i <= 3:
            #   print("   AVANT  matrixAdj[", e, "][composant] ", matrixAdj[e]["composant"])
            listNoeud.add(e)
    # print("     ", i, " [inDiffComposant] ")

    return listLabel, listNoeud, inComposant


def A(matrixAdj):
    # pprint.pprint(matrixAdj)
    print(" ******************** A ******************** ")
    for i in 5, 4, 3, 2:
        for v in matrixAdj.keys():
            if matrixAdj[v]["color"] == "noir" or matrixAdj[v]["color"] == "bleu":
                continue
            # print("v : ", v, " | ", i)

            listLabel, listNoeud, inComposant = inDiffComposant(matrixAdj, v, i)
            if matrixAdj[v]["color"] == "gris" and len(listLabel) >= i:
                # print("             listLabel: ", listLabel)
                # print("             listComposant: ", listNoeud)
                matrixAdj[v]["color"] = "blue"
                maxLabel = max(listLabel, key=len)
                for e in listNoeud:
                    matrixAdj[e]["composant"] = True
                    if not inComposant:
                        # print("         je suis dans le if")
                        matrixAdj[e]["label"] = ''.join(map(str, listLabel))
                    else:
                        # print("         je suis dans le else")
                        matrixAdj[e]["label"] = maxLabel
                    # print("         je change en blue matrixAdj[", e, "][label] : ", matrixAdj[e]["label"])
                    # print("   APRES  matrixAdj[", e, "][composant] ", matrixAdj[e]["composant"])
    # pprint.pprint(matrixAdj)


a, b, matrixAdj = getEdges(verticesIdP)
edges = list(map(list, a))
# print("matrixAdj : ")
# pprint.pprint(matrixAdj)
# print("edges : ", b)
# print("v[A] : ", matrixAdj[1]["nbV"])
# print(matrixAdj)

matrixAdj = {0: {"voisins": [1], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             1: {"voisins": [0, 2, 5, 8], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             2: {"voisins": [1, 5, 3], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             3: {"voisins": [2, 4], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             4: {"voisins": [5, 6, 16, 3], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             5: {"voisins": [1, 2, 4, 7], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             6: {"voisins": [4, 7, 14], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             7: {"voisins": [5, 8, 12, 13, 6], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             8: {"voisins": [1, 9, 10, 12, 7], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             9: {"voisins": [8], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             10: {"voisins": [8, 12], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             11: {"voisins": [12], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             12: {"voisins": [10, 8, 7, 13, 11], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             13: {"voisins": [7, 12, 14], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             14: {"voisins": [6, 15, 13], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             15: {"voisins": [14], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False},
             16: {"voisins": [4], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False}}

tmps1 = time.clock()
MIS(matrixAdj, noir, gris)
tmps2 = time.clock()
print("[MIS] Temps d'execution = ", tmps2-tmps1)

tmps1 = time.clock()
MISV2(matrixAdj, noir, gris)
tmps2 = time.clock()
print("[MISV2] Temps d'execution = ", tmps2-tmps1)

# A(matrixAdj)
# print(list(verticesIdP.keys()))
# edgesD = list(map(list, b))
# 26868
# print("edgesD : ", edgesD)

"""
edgesList = str(sys.argv[1]).split(".")
edges = []
for e in edgesList:
    edges.append(list(map(int, e.split(","))))

g = Graph(edges)
first5 = g.vertices()[:5]
st = g.steiner_tree(first5)
st.is_tree()
"""
