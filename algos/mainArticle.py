from algos.AlgoAricle import *
from algos.EnsembleDSageM import getEdges, MISinFile
import time

f = open("../input.points")
vertices = f.read().splitlines()

res = list(map(lambda x: (int(x.split(' ')[0]), int(x.split(' ')[1])), vertices))

# un id pour chaque noeud { id : Point(x,y) ....}
verticesIdP = dict(enumerate(res, 0))


a, b, matrixAdj = getEdges(verticesIdP)

# trouver l'element max dans notre dict par rapport au nb voisins
# itemMaxValue = max(matrixAdjT.items(), key=lambda x: len(x[1]["voisins"]))

edges = list(map(list, a))

tmps1 = time.clock()
noir = MIS(matrixAdj)
bleu = A(matrixAdj)
tmps2 = time.clock()
print("[MIS] + [A] Temps d'execution = ", tmps2 - tmps1)
print(" noir : ", len(noir))
print(" bleu : ", len(bleu))
MISinFile(list(noir) + list(bleu), verticesIdP)
