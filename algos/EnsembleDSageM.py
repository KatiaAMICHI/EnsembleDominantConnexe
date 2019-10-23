from collections import defaultdict
from operator import or_
from functools import reduce
from operator import itemgetter
import pprint

# import pandas as pd
# from sage.all import *


d = 55


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
