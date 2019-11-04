#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import defaultdict
import networkx as nx

"""
Fichier qui contient les différents méthode caractérisant un graph
    * les sommets
    * les arretes
    * la matrice d'adjacence
    * le noeud de degré maximum
    * isCDS
    * écriture/lecture de fichier
"""


def getVertices(filename, isFloat=False, firstLineIgnore=False):
    """
    retourne une map <identifiant sommet, position(x,y) sommet>
    :param filename:
    :return:
    """

    f = open(filename, 'r')
    vertices = f.read().splitlines()

    if firstLineIgnore:
        del vertices[0]

    if isFloat:
        res = list(map(lambda x: (float(x.split(' ')[0]), float(x.split(' ')[1])), vertices))
    else:
        res = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), vertices))
    verticesIdP = dict(enumerate(res, 0))

    return verticesIdP


def getVerticesFile(file, isFloat=False, firstLineIgnore=False):
    # si le séparateur entre les arrete est '\t'
    # cmd = "tr '\t' '\n' < " + file + " | sort | uniq"
    # sinon
    cmd = "tr ' ' '\n' < " + file + " | sort | uniq"
    vertices = os.popen(cmd).read().split('\n')
    del vertices[-1]

    if isFloat:
        vertices = list(map(float, vertices))
    else:
        vertices = list(map(int, vertices))

    return vertices


def getEdgesFile(file, isFloat, firstLineIgnore=False):
    with open(file, 'r') as f:
        reader = f.read().splitlines()
        if isFloat:
            edges = list(map(lambda x: (float(x.split(' ')[0]), float(x.split(' ')[1])), reader))
        else:
            # si le séparateur entre les arrete est '\t'
            # edges = list(map(lambda x: (int(x.split('\t')[0]), int(x.split('\t')[1])), reader))
            # sinon
            edges = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), reader))
    return edges


def getVerticesG(file, geo=False, isFloat=False):
    if geo:
        return getVertices(file, isFloat)
    return getVerticesFile(file, isFloat)


def getMatrixAdjFile(file, isFloat=False, firstLineIgnore=False):
    vertices = getVerticesFile(file, isFloat, firstLineIgnore=firstLineIgnore)
    edges = getEdgesFile(file, isFloat, firstLineIgnore=firstLineIgnore)

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


def getEdges(file, d, isFloat=False, firstLineIgnore=False):
    verticesIdP = getVertices(file, isFloat, firstLineIgnore=firstLineIgnore)

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
            if isNeighbor(verticesIdP, u, v, d):
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


def isNeighbor(verticesIdP, u, v, d):
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


def isCDS(G, mcds):
    return nx.is_dominating_set(G, mcds) and nx.is_connected(G.subgraph(mcds))


def MISinFile(noir, verticesIdP):
    pointsOutput = []
    result = list(map(lambda x: verticesIdP[x], noir))
    for v in noir:
        pointsOutput.append(verticesIdP[v])

    open("OutputFile", 'w').write('\n'.join('%s %s' % x for x in pointsOutput))
