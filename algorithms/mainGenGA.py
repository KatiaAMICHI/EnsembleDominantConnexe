#!/usr/bin/env python
# -*- coding: utf-8 -*-#

import time

import networkx as nx

from algorithms.ArticleAlgorithms import *
from algorithms.EnsembleDSageM import *
from algorithms.EnsembleDSageM import getEdges
from algorithms.v1 import MCDS


def main():
    nb_file = 0
    Dataset = "GenGA"

    resultDataset = r'../result/' + Dataset + '/results' + Dataset + '.csv'
    csv_Times = open(resultDataset, mode='w')
    fieldnamesTimesDataset = ["Dataset", "nbFile", "V", "E", "TalgoLi&", "TalgoA", "TalgoX", "NBalgoLi&", "NBalgoA",
                              "NBalgoX"]
    writerTimesDataset = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimesDataset)
    writerTimesDataset.writeheader()

    resultFile = r'../result/' + Dataset + '/resultsFiles' + Dataset + '.csv'
    csv_Times = open(resultFile, mode='w')
    fieldnamesTimes = ["File", "V", "E", "TalgoLi&", "TalgoA", "TalgoX", "NBalgoLi&", "NBalgoA", "NBalgoX"]
    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    resultsFiles = {"V": 0, "E": 0, "TalgoLi&": 0, "TalgoA": 0, "TalgoX": 0, "NBalgoLi&": 0, "NBalgoA": 0, "NBalgoX": 0}

    # path = "../res/" + Dataset + "/decoData/"
    path = "../res/extract" + Dataset + "/"
    path = "../res/" + Dataset + "/"

    geo = True

    firstLineIgnore = False

    for f1 in os.listdir(path):
        if Dataset == "Enron" or Dataset == "Rollernet":
            geo = False
        if Dataset == "GenTests" or Dataset == "GenNetworkx":
            firstLineIgnore = True
            with open(path + f1) as f:
                first_line = f.readline()
                nbNode, d = first_line.split(' ')
        elif Dataset == "GenJava":
            d = 55
        else:
            d = 70

        if geo:
            edges, edgesDist, matrixAdj = getEdges(path + f1, int(d), firstLineIgnore=firstLineIgnore)
        else:
            matrixAdj = getMatrixAdjFile(path + f1)
            edges = getEdgesFile(path + f1, firstLineIgnore=firstLineIgnore)
        vertices = getVerticesG(path + f1, geo=geo)

        print(" +++++++++++++++ algo CDSA  avec ", f1, " +++++++++++++++ ")
        G = nx.Graph()
        G.add_edges_from(edges)
        tmps1 = time.process_time()
        cdsA = MCDS(G)
        tmps2 = time.process_time()
        if cdsA == -1:
            continue
        print("     je suis la ")
        talgoA = tmps2 - tmps1
        print("cds len : ", len(cdsA))
        print(" --------------- FIN CDSA  avec ", f1, " ---------------")
        print()
        print()
        print(" +++++++++++++++ algo Article ", f1, " +++++++++++++++ ")
        tmps1 = time.process_time()
        noir = MIS(matrixAdj)
        bleu = A(matrixAdj)
        tmps2 = time.process_time()
        talgoLi = tmps2 - tmps1
        cdsLi = list(noir) + list(bleu)
        print("cdsLi len : ", len(cdsLi))
        print(" --------------- FIN algo Article  avec ", f1, " --------------- ")

        resultsFiles['V'] += len(vertices)
        resultsFiles['E'] += len(edges)
        resultsFiles["TalgoLi&"] += talgoLi
        resultsFiles["TalgoA"] += talgoA
        resultsFiles["TalgoX"] += 0
        resultsFiles["NBalgoLi&"] += len(cdsLi)
        resultsFiles["NBalgoA"] += len(cdsA)
        resultsFiles["NBalgoX"] += 0

        writerTimes.writerow({'File': f1.replace(".points", ""),
                              "V": len(vertices),
                              "E": len(edges),
                              "TalgoLi&": round(talgoLi, 4),
                              "TalgoA": round(talgoA, 4),
                              "TalgoX": 0,
                              "NBalgoLi&": len(cdsLi),
                              "NBalgoA": len(cdsA),
                              "NBalgoX": 0})
        nb_file += 1

    print("nbFile : ", nb_file)
    writerTimesDataset.writerow({'Dataset': Dataset,
                                 "nbFile": nb_file,
                                 "V": round(resultsFiles["V"] / nb_file, 4),
                                 "E": round(resultsFiles["E"] / nb_file, 4),
                                 "TalgoLi&": round(resultsFiles["TalgoLi&"] / nb_file, 4),
                                 "TalgoA": round(resultsFiles["TalgoA"] / nb_file, 4),
                                 "TalgoX": round(resultsFiles["TalgoX"] / nb_file, 4),
                                 "NBalgoLi&": round(resultsFiles["NBalgoLi&"] / nb_file, 4),
                                 "NBalgoA": round(resultsFiles["NBalgoA"] / nb_file, 4),
                                 "NBalgoX": round(resultsFiles["NBalgoX"] / nb_file, 4)})


main()
