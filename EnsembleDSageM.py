import time
from collections import defaultdict
from operator import or_
from functools import reduce
import pprint

# import pandas as pd
# from sage.all import *

d = 55
f = open("input.points")
vertices = f.read().splitlines()

res = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), vertices))

# un id pour chaque noeud { id : Point(x,y) ....}
verticesIdP = dict(enumerate(res, 0))


def getEdges(verticesIdP):
    matrixAdj = defaultdict()
    for v in verticesIdP:
        matrixAdj[v] = {"voisins": set(), "label": None, "color": "blanc", "nbV": 0, "composant": False}
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

            for n in matrixAdj[v]["voisins"]:
                matrixAdj[n]["color"] = "gris"
                nbVisite += 1
                listVoisinsN = matrixAdj[n]["voisins"]
                listToVisite = reduce(or_, [listToVisite, set(listVoisinsN)])
        listToVisite = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", listToVisite))

    print("<<<<<<< noir : ", noir)
    return noir


def MISV2(matrixAdj, noir, gris):
    noir = []
    for v in list(matrixAdj.keys()):
        if matrixAdj[v]["color"] == "gris":
            continue
        if hasNNeibBlack(matrixAdj, noir, v):
            noir.append(v)
            matrixAdj[v]["color"] = "noir"
            matrixAdj[v]["label"] = "N" + str(v)
            for n in matrixAdj[v]["voisins"]:
                matrixAdj[n]["color"] = "gris"
    print("MISV2 <<<<<<< noir : ", len(noir))
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
    print(" ******************** A ******************** ")
    bleu = set()
    for i in 5, 4, 3, 2:
        for v in matrixAdj.keys():
            if matrixAdj[v]["color"] == "noir" or matrixAdj[v]["color"] == "bleu":
                continue
            listLabel, listNoeud, inComposant = inDiffComposant(matrixAdj, v, i)
            if matrixAdj[v]["color"] == "gris" and len(listLabel) >= i:
                matrixAdj[v]["color"] = "blue"
                bleu.add(v)
                maxLabel = max(listLabel, key=len)
                for e in listNoeud:
                    matrixAdj[e]["composant"] = True
                    if not inComposant:
                        matrixAdj[e]["label"] = ''.join(map(str, listLabel))
                    else:
                        matrixAdj[e]["label"] = maxLabel
    return bleu


a, b, matrixAdj = getEdges(verticesIdP)
edges = list(map(list, a))

tmps1 = time.clock()
noir = MIS(matrixAdj)
tmps2 = time.clock()
print("[MIS] Temps d'execution = ", tmps2 - tmps1)
print(isMIS(matrixAdj.copy(), noir))

bleu = A(matrixAdj)
print("bleu : ", len(bleu))
MISinFile(list(noir) + list(bleu), verticesIdP)
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
