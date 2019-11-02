from algorithms.AlgoAricle import *
from algorithms.EnsembleDSageM import *
import time

from algorithms.algoAvril import *
from algorithms.algoPlus import MISC

path = "../"
f1 = "input4.points"

# VerticesIdP  un id pour chaque noeud { id : Point(x,y) ....}

geo = True
if geo:
    a, edgesDist, matrixAdj = getEdges(path + f1)
else:
    matrixAdj = getMatrixAdjFile(path + f1)
    a = getEdgesFile(path + f1)
vertices = getVerticesG(path + f1, geo=geo)

# trouver l'element max dans notre dict par rapport au nb voisins
# itemMaxValue = max(matrixAdjT.items(), key=lambda x: len(x[1]["voisins"]))

edges = list(map(list, a))
matrixAdja = {0: {"voisins": [1], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [0]},
              1: {"voisins": [0, 2, 5, 8], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [1]},
              2: {"voisins": [1, 5, 3], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [2]},
              3: {"voisins": [2, 4], 'label': None, 'color': 'blanc', 'nbV': 2, "composant": False, "inComposant": [3]},
              4: {"voisins": [5, 6, 16, 3], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [4]},
              5: {"voisins": [1, 2, 4, 7], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [5]},
              6: {"voisins": [4, 7, 14], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [6]},
              7: {"voisins": [5, 8, 12, 13, 6], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                  "inComposant": [7]},
              8: {"voisins": [1, 9, 10, 7], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                  "inComposant": [8]},
              9: {"voisins": [8], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [9]},
              10: {"voisins": [8, 12], 'label': None, 'color': 'blanc', 'nbV': 2, "composant": False,
                   "inComposant": [10]},
              11: {"voisins": [12], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [11]},
              12: {"voisins": [10, 7, 13, 11], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                   "inComposant": [12]},
              13: {"voisins": [7, 12, 14], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                   "inComposant": [13]},
              14: {"voisins": [6, 15, 13], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                   "inComposant": [14]},
              15: {"voisins": [14], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [15]},
              16: {"voisins": [4], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [16]}}

matrixAdjy = {1: {"voisins": [2, 3, 4, 5, 6, 7], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [1]},
              2: {"voisins": [1, 3, 8], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [2]},
              3: {"voisins": [1, 2, 8, 9, 6], 'label': None, 'color': 'blanc', 'nbV': 2, "composant": False,
                  "inComposant": [3]},
              4: {"voisins": [1, 6], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [4]},
              5: {"voisins": [1, 7], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [5]},
              6: {"voisins": [1, 4, 3, 9], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [6]},
              7: {"voisins": [1, 2, 5], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                  "inComposant": [7]},
              8: {"voisins": [2, 3], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                  "inComposant": [8]},
              9: {"voisins": [3, 6], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [9]}}

matrixAdjs = {1: {"voisins": [2, 3, 4], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [1]},
              2: {"voisins": [1, 5, 6], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [2]},
              3: {"voisins": [1, 6, 7, 8], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [3]},
              4: {"voisins": [1, 8, 9], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [4]},
              5: {"voisins": [2, 10], 'label': None, 'color': 'blanc', 'nbV': 2, "composant": False,
                  "inComposant": [5]},
              6: {"voisins": [2, 3, 10, 11], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [6]},
              7: {"voisins": [3, 10, 11, 12], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [7]},
              8: {"voisins": [3, 4, 11, 12], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [8]},
              9: {"voisins": [4, 12], 'label': None, 'color': 'blanc', 'nbV': 2, "composant": False,
                  "inComposant": [9]},
              10: {"voisins": [5, 6, 7, 13, 11], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                   "inComposant": [10]},
              11: {"voisins": [6, 7, 8, 14, 15, 10, 12], 'label': None, 'color': 'blanc', 'nbV': 7, "composant": False,
                   "inComposant": [11]},
              12: {"voisins": [7, 8, 9, 16, 11], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                   "inComposant": [12]},
              13: {"voisins": [10], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False,
                   "inComposant": [13]},
              14: {"voisins": [11], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False,
                   "inComposant": [14]},
              15: {"voisins": [11], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [15]},
              16: {"voisins": [12], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [16]}}

matrixAdjp = {1: {"voisins": [2, 3, 4], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [1]},
              2: {"voisins": [1, 5, 6], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [2]},
              3: {"voisins": [1, 6, 7, 8], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [3]},
              4: {"voisins": [1, 8, 9], 'label': None, 'color': 'blanc', 'nbV': 3, "composant": False,
                  "inComposant": [4]},
              5: {"voisins": [2, 10], 'label': None, 'color': 'blanc', 'nbV': 2, "composant": False,
                  "inComposant": [5]},
              6: {"voisins": [2, 3, 10, 11], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [6]},
              7: {"voisins": [3, 10, 11, 12], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [7]},
              8: {"voisins": [3, 4, 11, 12], 'label': None, 'color': 'blanc', 'nbV': 4, "composant": False,
                  "inComposant": [8]},
              9: {"voisins": [4, 12], 'label': None, 'color': 'blanc', 'nbV': 2, "composant": False,
                  "inComposant": [9]},
              10: {"voisins": [5, 6, 7, 13, 11], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                   "inComposant": [10]},
              11: {"voisins": [6, 7, 8, 14, 15, 10, 12], 'label': None, 'color': 'blanc', 'nbV': 7, "composant": False,
                   "inComposant": [11]},
              12: {"voisins": [7, 8, 9, 16, 11], 'label': None, 'color': 'blanc', 'nbV': 5, "composant": False,
                   "inComposant": [12]},
              13: {"voisins": [10], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False,
                   "inComposant": [13]},
              14: {"voisins": [11], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False,
                   "inComposant": [14]},
              15: {"voisins": [11], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [15]},
              16: {"voisins": [12], 'label': None, 'color': 'blanc', 'nbV': 1, "composant": False, "inComposant": [16]}}

verticesIdP = getVertices(path + f1)

# ALGO article
noir = MIS(matrixAdj)
bleu = A(matrixAdj)

print(" noir : ", len(noir))
print(" bleu : ", len(bleu))
MISinFile(list(noir) + list(bleu), verticesIdP)
#############################################################
# ALGO plus
# MISC(matrixAdj)

# ALGO avril
# verticesToVisite = list(matrixAdj.keys())
# noir, matrixAdj = IC_MIS(matrixAdj)
# print("noir : ", len(noir))
# bleu = Kruskal(matrixAdj, list(noir))
# MISinFile(list(noir), verticesIdP)
