#!/usr/bin/env python
# -*- coding: utf-8 -*-#

import os
import sys
import time

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("algorithms", "")
sys.path.append(dir_path)

from algorithms.ArticleAlgorithms import *
from algorithms.GraphMethod import *
from algorithms.GraphMethod import getEdges
from algorithms.MCDS import *

filename = str(sys.argv[1])


def main():
    nb_file = 1

    geo = True  # true si le graph est géomitrique, false sinon
    if geo:
        firstLineIgnore = False  # doit etre mis a True pour les fichier de test de GADB
        if firstLineIgnore:
            f = open(filename, 'r')
            vertices = f.read().splitlines()
            d = vertices[0].split(' ')[1]
            print("d : ", d)
        elif "Java" in filename:
            d = 70
        else:
            d = 70

        edges, edgesDist, matrixAdj = getEdges(filename, int(d), firstLineIgnore=firstLineIgnore)
    else:
        matrixAdj = getMatrixAdjFile(filename)
        edges = getEdgesFile(filename)

    vertices = getVerticesG(filename, geo=geo)
    print(" vertices : ", len(vertices))
    print(" edges : ", len(edges))

    print(" +++++++++++++++ algo Article ", filename, " +++++++++++++++ ")
    tmps1 = time.process_time()
    noir = MIS(matrixAdj)
    bleu = A(matrixAdj)
    tmps2 = time.process_time()
    talgoLi = tmps2 - tmps1
    cdsLi = list(noir) + list(bleu)
    print("cdsLi len : ", len(cdsLi))
    print(" --------------- FIN algo Article  avec ", filename, " --------------- ")
    print()
    print()
    print(" +++++++++++++++ algo CDSA  avec ", filename, " +++++++++++++++ ")
    G = nx.Graph()
    G.add_edges_from(edges)
    print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> density : ", nx.density(G))
    print("nx.is_connected(G) : ", nx.is_connected(G))
    tmps1 = time.process_time()
    cdsA = MCDS(G)
    tmps2 = time.process_time()
    talgoA = tmps2 - tmps1
    print("cds len : ", len(cdsA))
    print(" --------------- FIN CDSA  avec ", filename, " ---------------")

    print({'File': filename.replace(".points", ""),
           "V": round(len(vertices) / nb_file, 4),
           "E": round(len(edges) / nb_file, 4),
           "TalgoLi&": round(talgoLi / nb_file, 4),
           "TalgoA": round(talgoA / nb_file, 4),
           "TalgoX": round(0 / nb_file, 4),
           "NBalgoLi&": round(len(cdsLi) / nb_file, 4),
           "NBalgoA": round(len(cdsA) / nb_file, 4),
           "NBalgoX": round(0 / nb_file, 4)})


main()
