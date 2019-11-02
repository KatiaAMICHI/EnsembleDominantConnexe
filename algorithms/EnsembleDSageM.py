from collections import defaultdict
from operator import or_
from functools import reduce
from operator import itemgetter
import pprint
import re
import os
# import pandas as pd
# from sage.all import *
import numpy as np
import csv

# d = 55
d = 0.135
d = 55


def getVertices(filename, isFloat=False):
    """
    retourne une map <identifiant sommet, position(x,y) sommet>
    :param filename:
    :return:
    """
    f = open(filename, 'r')
    vertices = f.read().splitlines()
    if isFloat:
        res = list(map(lambda x: (float(x.split(' ')[0]), float(x.split(' ')[1])), vertices))
    else:
        res = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), vertices))
    # un id pour chaque noeud { id : Point(x,y) ....}
    verticesIdP = dict(enumerate(res, 0))

    return verticesIdP


def getVerticesFile(file, isFloat=False):
    # cmd = "tr '\t' '\n' < " + file + " | sort | uniq"
    cmd = "tr ' ' '\n' < " + file + " | sort | uniq"
    vertices = os.popen(cmd).read().split('\n')
    del vertices[-1]
    if isFloat:
        vertices = list(map(float, vertices))
    else:
        vertices = list(map(int, vertices))

    return vertices


def getEdgesFile(file, isFloat):
    with open(file, 'r') as f:
        reader = f.read().splitlines()
        # edges = list(map(lambda x: (int(x.split('\t')[0]), int(x.split('\t')[1])), reader))
        if isFloat:
            edges = list(map(lambda x: (float(x.split(' ')[0]), float(x.split(' ')[1])), reader))
        else:
            edges = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), reader))
    print("[getEdgesFile] edges : ", len(edges))
    return edges


def getVerticesG(file, geo=False, isFloat=False):
    if geo:
        return getVertices(file, isFloat)
    return getVerticesFile(file, isFloat)


def getMatrixAdjFile(file, isFloat=False):
    vertices = getVerticesFile(file, isFloat)
    edges = getEdgesFile(file, isFloat)

    matrixAdj = defaultdict()

    for v in vertices:
        matrixAdj[v] = {"voisins": set(), "label": None, "color": "blanc", "nbV": 0, "inComposant": False}

    for e in edges:
        u, v = e
        matrixAdj[u]["voisins"].add(v)
        matrixAdj[v]["voisins"].add(u)
        matrixAdj[u]["nbV"] += 1
        matrixAdj[v]["nbV"] += 1

    return matrixAdj


def getEdges(file, isFloat=False):
    verticesIdP = getVertices(file, isFloat)

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
                matrixAdj[v]["nbV"] += 1

                if u < v:
                    edgesDist.add((u, v, dis))
                    edges.add((u, v))
                else:
                    edges.add((v, u))
    return list(edges), list(edgesDist), matrixAdj


def getMaxVwDegree(matrixAdj):
    return max(matrixAdj.keys(), key=lambda x: matrixAdj[x]["nbV"])


def getMaxVwDegreeWithL(matrixAdj, l):
    return max(l, key=lambda x: matrixAdj[x]["nbV"])


def isNeighbor(verticesIdP, u, v):
    return getDis(verticesIdP, u, v) < (d * d)


def getDis(verticesIdP, u, v):
    return (((verticesIdP[u][0] - verticesIdP[v][0]) * (verticesIdP[u][0] - verticesIdP[v][0])) + \
            ((verticesIdP[u][1] - verticesIdP[v][1]) * (verticesIdP[u][1] - verticesIdP[v][1])))


def neighborP(p, vertices):
    """
    get neighor of p with distance
    :param p:
    :param vertices:
    :return:
    """
    result = set()
    result = set(map(lambda x: vertices[point], filter(lambda n: n != p and isNeighbor(vertices, point, p), vertices)))
    result = set()

    for point in vertices:
        if point == p:
            continue
        if isNeighbor(vertices, point, p):
            result.add(vertices[point])
    return result


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
    result = list(map(lambda x: verticesIdP[x], noir))
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
