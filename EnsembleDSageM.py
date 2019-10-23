import time
from collections import defaultdict
from operator import or_
from functools import reduce
from operator import itemgetter
import pprint

# import pandas as pd
# from sage.all import *

d = 55
f = open("input.points")
vertices = f.read().splitlines()

res = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), vertices))

# un id pour chaque noeud { id : Point(x,y) ....}
verticesIdP = dict(enumerate(res, 0))

dictComposion = {}


def getEdges(verticesIdP):
    matrixAdj = defaultdict()
    for v in verticesIdP:
        matrixAdj[v] = {"voisins": set(), "label": None, "color": "blanc", "nbV": 0, "inComposant": False}
    edges = set()
    edgesDist = set()
    for u in verticesIdP:
        for v in verticesIdP:
            if u == v:
                continue
            dis = getDis(verticesIdP, u, v)
            if isNeighbor(verticesIdP, u, v):
                matrixAdj[u]["voisins"].add(v)
                matrixAdj[v]["voisins"].add(u)
                matrixAdj[u]["nbV"] += 1

                if u < v:
                    edgesDist.add((u, v, dis))
                    edges.add((u, v))
                else:
                    edges.add((v, u))
    return list(edges), list(edgesDist), matrixAdj


def isNeighbor(verticesIdP, u, v):
    return getDis(verticesIdP, u, v) < (d * d)


def getDis(verticesIdP, u, v):
    return (((verticesIdP[u][0] - verticesIdP[v][0]) * (verticesIdP[u][0] - verticesIdP[v][0])) + \
            ((verticesIdP[u][1] - verticesIdP[v][1]) * (verticesIdP[u][1] - verticesIdP[v][1])))


def neighbor(p, vertices):
    result = set()
    for point in vertices:
        print(" p : ", point)
        if point == p:
            continue
        if isNeighbor(vertices, point, p):
            result.add(vertices[point])
    print("result size : ", len(result))


def hasNNeibBlack(matrixAdj, noir, v):
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


def MIS(matrixAdj):
    nbVisite = 0
    listNoeud = list(matrixAdj.keys())

    listToVisite = set()
    listToVisite.add(listNoeud[0])
    noir = []
    while len(listToVisite) != 0:
        v = listToVisite.pop()
        if matrixAdj[v]["color"] == "gris":
            continue
        if hasNNeibBlack(matrixAdj, noir, v):
            noir.append(v)
            matrixAdj[v]["color"] = "noir"
            nbVisite += 1
            matrixAdj[v]["label"] = "N" + str(v)
            dictComposion[matrixAdj[v]["label"]] = set([v])
            for n in matrixAdj[v]["voisins"]:
                matrixAdj[n]["color"] = "gris"
                nbVisite += 1
                listVoisinsN = matrixAdj[n]["voisins"]
                listToVisite = reduce(or_, [listToVisite, set(listVoisinsN)])
        listToVisite = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", listToVisite))

    print("<<<<<<< noir : ", noir)
    return noir


def isMIS(matrixAdj, MIS):
    vertices = list(matrixAdj.keys())
    cpt = 0
    for p in MIS:
        vertices.remove(p)
        vertices = set(vertices) - set(matrixAdj[p]["voisins"])
        cpt += len(matrixAdj[p]["voisins"])
    return len(vertices) == 0


def MISinFile(noir, verticesIdP):
    pointsOutput = []
    for v in noir:
        pointsOutput.append(verticesIdP[v])

    open("OutputFile", 'w').write('\n'.join('%s %s' % x for x in pointsOutput))


def inDiffComposant(matrixAdj, v, i):
    listLabel = set()
    listNoeud = set()
    inComposant = False
    composant = None
    for e in matrixAdj[v]["voisins"]:
        if matrixAdj[e]["color"] == "noir":
            listLabel.add(matrixAdj[e]["label"])

            if matrixAdj[e]["composant"]:
                inComposant = matrixAdj[e]["composant"]
                composant = matrixAdj[e]["label"]

            listNoeud.add(e)

    return listLabel, listNoeud, inComposant, composant


def inDiffComposantA(matrixAdj, dictComposion, v):
    voisinsNoir = set(filter(lambda x: matrixAdj[x]["color"] == "noir", matrixAdj[v]["voisins"]))
    print("      [inDiffComposantA] voisinsNoir : ", voisinsNoir)
    print("      [inDiffComposantA] matrixAdj : ", matrixAdj[list(voisinsNoir)[0]]["label"])

    voisinsNoirComposant = list(map(lambda x: (matrixAdj[x]["label"], matrixAdj[x]["inComposant"]), voisinsNoir))
    print("      [inDiffComposantA] : ", voisinsNoirComposant)
    print("      [inDiffComposantA] d : ", dictComposion)

    voisinsNoirComposantOccen = set()
    for x in voisinsNoirComposant:
        print("         x : ", x)
        # print("         matrixAdj[", x[0], "][label] : ", matrixAdj[int(x[2])]["label"])
        if x[0] not in dictComposion.keys():
            print("            x[0] : ", x[0])
        voisinsNoirComposantOccen.add((x[0], len(dictComposion[x[0]]) if (x[1]) else -1))

    # voisinsNoirComposantOccen = set(
    #  map(lambda x: (x[0], len(dictComposion[matrixAdj[x[0]]["label"]]) if (x[1]) else -1), voisinsNoirComposant))

    return voisinsNoirComposantOccen, voisinsNoir


def AAV2(matrixAdj, noir):
    global dictComposion
    bleu = set()

    print("dictComposion size : ", len(dictComposion.keys()))
    for i in 5, 4, 3, 2:
        print(" ******************** A : ", i, " ******************** ")

        verticesToVisite = set(filter(lambda x: matrixAdj[x]["color"] == "gris", matrixAdj.keys()))
        # print("verticesToVisite : ", verticesToVisite)
        while len(verticesToVisite) != 0:
            v = verticesToVisite.pop()
            voisinsNoirComposantOccen, voisinsNoir = inDiffComposantA(matrixAdj, dictComposion, v)
            if len(voisinsNoirComposantOccen) >= i:
                print("v : ", v)
                print(" dictComposion : ", dictComposion)
                matrixAdj[v]["color"] = "bleu"
                bleu.add(v)

                print("     voisinsNoirComposantOccen : ", voisinsNoirComposantOccen)
                composant = max(voisinsNoirComposantOccen, key=itemgetter(1))[0]
                # jusqu'a la j'ai le composant dominant
                print("     composant : ", composant)

                for e in voisinsNoir:
                    compToDelet = matrixAdj[e]["label"]
                    matrixAdj[e]["inComposant"] = True

                    if compToDelet == composant:
                        continue
                    print("     e : ", e)
                    print("         Nom comp DOminant : ", composant)
                    print("         list comp in compToDelete : ", dictComposion[compToDelet])
                    for p in list(dictComposion[compToDelet]):
                        print("           p : ", p)
                        matrixAdj[p]["label"] = composant
                        dictComposion[composant].add(p)
                        # dictComposion[compToDelet].remove(p)

                    del dictComposion[compToDelet]
                    matrixAdj[e]["label"] = composant

                    dictComposion[composant].add(e)

                matrixAdj[v]["inComposant"] = True

                # print(" composant : ", dictComposion)

        print(" bleu : ", len(bleu))
    return bleu


a, b, matrixAdj = getEdges(verticesIdP)

matrixAdjy = {0: {"voisins": [1], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              1: {"voisins": [0, 2, 5, 8], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              2: {"voisins": [1, 5, 3], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              3: {"voisins": [2, 4], 'label': None, 'color': 'blanc', 'nbV': 12, "inComposant": False},
              4: {"voisins": [5, 6, 16, 3], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              5: {"voisins": [1, 2, 4, 7], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              6: {"voisins": [4, 7, 14], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              7: {"voisins": [5, 8, 12, 13, 6], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              8: {"voisins": [1, 9, 10, 12, 7], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              9: {"voisins": [8, 20], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              10: {"voisins": [8, 12, 17], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              11: {"voisins": [12], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              12: {"voisins": [10, 8, 7, 13, 11], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              13: {"voisins": [7, 12, 14], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              14: {"voisins": [6, 15, 13], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              15: {"voisins": [14], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              16: {"voisins": [4], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              17: {"voisins": [10, 18], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              18: {"voisins": [17, 19], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              19: {"voisins": [18], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              20: {"voisins": [9], 'label': None, 'color': 'blanc', 'nbV': 1, "inComposant": False},
              }

# trouver l'element max dans notre dict par rapport au nb voisins
# itemMaxValue = max(matrixAdjT.items(), key=lambda x: len(x[1]["voisins"]))

edges = list(map(list, a))

tmps1 = time.clock()
noir = MIS(matrixAdj)
tmps2 = time.clock()
print("[MIS] Temps d'execution = ", tmps2 - tmps1)
print(isMIS(matrixAdj.copy(), noir))

# bleu = A(matrixAdj)
bleu = AAV2(matrixAdj, noir)
print("bleu : ", len(bleu))
# print("bleu : ", len(bleu))

# MISinFile(list(noir) + list(bleu), verticesIdP)
MISinFile(list(noir), verticesIdP)
# print(list(verticesIdP.keys()))
# edgesD = list(map(list, b))
# 26868
print(edges)
print("vertice : ", verticesIdP.keys())
print("noir : ", len(noir))
# pprint.pprint(matrixAdj)

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
