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
import matplotlib.pyplot as plt
import networkx as nx


def main():
    Dataset = "Enron"
    path = "../res/extract" + Dataset + "/"
    filename = 'extractEnron20900000.points'

    geo = False
    if geo:
        edges, edgesDist, matrixAdj = getEdges(path + filename)
    else:
        matrixAdj = getMatrixAdjFile(path + filename)
        edges = getEdgesFile(path + filename)
    vertices = getVerticesG(path + filename, geo=geo)

    print("edges : ", edges)

main()
