#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
from functools import reduce
from operator import or_

dictComposion = {}

"""
Dans ce fichier, on a implémenté les différents algorithmes de l'article, et les méthodes vérifiant les lemmas 
"""


def hasNNeibBlack(matrixAdj, noir, v):
    """
    Lemma 2

    :param matrixAdj: la matrice d'adjacence
    :param noir: la liste des noeuds noir
    :param v: un noeud
    :return: true si v a un noeud noir dans les voisins des ses voisins
    """

    if len(noir) == 0:
        return True
    if matrixAdj[v]["color"] == "gris":
        return False
    for n in matrixAdj[v]["voisins"]:
        if n in noir:
            return False
        for nn in matrixAdj[n]["voisins"]:
            if nn == v:
                continue
            if nn in noir:
                return True
    return False


def getDegreeWh(matrixAdj, v):
    """


    :param matrixAdj:
    :param v:
    :return:
    """
    return len(list(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[v]['voisins'])))


def getNodeMaxDegree(matrixAdj, listToVisite):
    listToVisite = list(
        map(lambda x: x, sorted(listToVisite, key=lambda p: getDegreeWh(matrixAdj, p), reverse=True)))
    maxDegree = listToVisite[0]
    del listToVisite[0]
    return set(listToVisite), maxDegree


def MIS(matrixAdj):
    nbVisite = 0
    listNoeud = list(matrixAdj.keys())

    listToVisite = set()
    listToVisite.add(listNoeud[0])
    noir = []
    while len(listToVisite) != 0:
        listToVisite, v = getNodeMaxDegree(matrixAdj, listToVisite)

        if matrixAdj[v]["color"] == "gris":
            continue
        if hasNNeibBlack(matrixAdj, noir, v):
            noir.append(v)
            matrixAdj[v]["color"] = "noir"
            nbVisite += 1
            matrixAdj[v]["label"] = "N" + str(v)
            dictComposion[matrixAdj[v]["label"]] = {v}
            for n in matrixAdj[v]["voisins"]:
                matrixAdj[n]["color"] = "gris"
                nbVisite += 1
                listVoisinsN = matrixAdj[n]["voisins"]
                listToVisite = reduce(or_, [listToVisite, set(listVoisinsN)])
        listToVisite = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", listToVisite))
    return noir


def inDiffComposantA(matrixAdj, dictComposion, v):
    voisinsNoir = set(filter(lambda x: matrixAdj[x]["color"] == "noir", matrixAdj[v]["voisins"]))
    voisinsNoirComposant = list(map(lambda x: (matrixAdj[x]["label"], matrixAdj[x]["inComposant"]), voisinsNoir))
    voisinsNoirComposantOccen = set(
        map(lambda x: (x[0], len(dictComposion[x[0]]) if (x[1]) else -1), voisinsNoirComposant))

    return voisinsNoirComposantOccen, voisinsNoir


def A(matrixAdj):
    global dictComposion
    bleu = set()

    for i in 5, 4, 3, 2:
        # print(" ******************** A : ", i, " ******************** ")

        verticesToVisite = set(filter(lambda x: matrixAdj[x]["color"] == "gris", matrixAdj.keys()))
        while len(verticesToVisite) != 0:
            v = verticesToVisite.pop()
            voisinsNoirComposantOccen, voisinsNoir = inDiffComposantA(matrixAdj, dictComposion, v)
            if len(voisinsNoirComposantOccen) >= i:
                matrixAdj[v]["color"] = "bleu"
                bleu.add(v)

                composant = max(voisinsNoirComposantOccen, key=itemgetter(1))[0]
                # jusqu'a la j'ai le composant dominant

                for e in voisinsNoir:
                    compToDelet = matrixAdj[e]["label"]
                    matrixAdj[e]["inComposant"] = True

                    if compToDelet == composant:
                        continue
                    for p in list(dictComposion[compToDelet]):
                        matrixAdj[p]["label"] = composant
                        dictComposion[composant].add(p)

                    del dictComposion[compToDelet]
                    matrixAdj[e]["label"] = composant

                    dictComposion[composant].add(e)

                matrixAdj[v]["inComposant"] = True
    return bleu
