#!/usr/bin/env python
# -*- coding: utf-8 -*-#

import csv
import sys
import time

import os

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("algorithms", "")
sys.path.append(dir_path)

from algorithms.ArticleAlgorithms import *
from algorithms.GraphMethod import *
from algorithms.GraphMethod import getEdges
from algorithms.MCDS import *

pathFile = str(sys.argv[1])


def main():
    nb_file = 1

    DataSet = "Networkxa"
    isFloat = False

    if DataSet == "Networkx":
        isFloat = True
    i = 0
    path = '../'
    filename = 'input3.points'

    filename = 'input2.points'
    filename = 'input.points'
    filename = 'input3.points'
    filename = 'input4.points'
    filename = 'generatGraph/tests0.txt'
    filename = 'res/extractRollernet/extractRollernet9200.points'

    i += 1
    geo = False
    if geo:
        edges, edgesDist, matrixAdj = getEdges(path + filename, isFloat=isFloat)
    else:
        matrixAdj = getMatrixAdjFile(path + filename, isFloat=isFloat)
        edges = getEdgesFile(path + filename, isFloat=isFloat)

    vertices = getVerticesG(path + filename, geo=geo, isFloat=isFloat)
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
    # MISinFile(list(noir) + list(bleu), vertices)
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
           "T": round(len(edges) / nb_file, 4),
           "TalgoLi&": round(talgoLi / nb_file, 4),
           "TalgoA": round(talgoA / nb_file, 4),
           "TalgoX": round(0 / nb_file, 4),
           "NBalgoLi&": round(len(cdsLi) / nb_file, 4),
           "NBalgoA": round(len(cdsA) / nb_file, 4),
           "NBalgoX": round(0 / nb_file, 4)})

# main()
