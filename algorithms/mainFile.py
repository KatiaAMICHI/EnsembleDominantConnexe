#!/usr/bin/env python
# -*- coding: utf-8 -*-#

from algos.EnsembleDSageM import *
from algos.v1 import *
import sys
import os
import csv
from algos.AlgoAricle import *
from algos.EnsembleDSageM import getEdges, MISinFile
import time

from algos.algoAvril import *


def main():
    nb_file = 1
    resultFile = r'../result/results.csv'
    csv_Times = open(resultFile, mode='w')
    fieldnamesTimes = ["File", "V", "T", "TalgoLi&", "TalgoA", "TalgoX", "NBalgoLi&", "NBalgoA", "NBalgoX"]
    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    i = 0
    path = '../'
    filename = 'input3.points'

    while i != nb_file:
        filename = 'input2.points'
        filename = 'input.points'
        filename = 'input3.points'

        i += 1
        geo = False
        if geo:
            edges, edgesDist, matrixAdj = getEdges(path + filename)
        else:
            matrixAdj = getMatrixAdjFile(path + filename)
            edges = getEdgesFile(path + filename)
        vertices = getVerticesG(path + filename, geo=geo)

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
        tmps1 = time.process_time()
        cdsA = min_connected_dominating_sets_non_distributed(G)
        tmps2 = time.process_time()
        talgoA = tmps2 - tmps1
        print("cds len : ", len(cdsA))
        print(" --------------- FIN CDSA  avec ", filename, " ---------------")

        writerTimes.writerow({'File': filename.replace(".points", ""),
                              "V": round(len(vertices) / nb_file, 4),
                              "T": round(len(edges) / nb_file, 4),
                              "TalgoLi&": round(talgoLi / nb_file, 4),
                              "TalgoA": round(talgoA / nb_file, 4),
                              "TalgoX": round(0 / nb_file, 4),
                              "NBalgoLi&": round(len(cdsLi) / nb_file, 4),
                              "NBalgoA": round(len(cdsA) / nb_file, 4),
                              "NBalgoX": round(0 / nb_file, 4)})


main()
