from algos.EnsembleDSageM import *
from functools import reduce
from operator import or_
from functools import reduce  # python3 required
from functools import reduce
from operator import add


def pro(matrixAdj, v):
    return len(set(filter(lambda x: (matrixAdj[x]["color"] == "blanc" or
                                     matrixAdj[x]["color"] == "bleu")
                          , matrixAdj[v]["voisins"])))


def IC_MIS(matrixAdj, verticesToVisite):
    """

    :param matrixAdj: la matrix adjacent du file input
    :param verticesToVisite: la liste de noeud
    :return: D : l'ensemble de dominant (noeud noir)
    """
    D = set()
    print("matrixAdj : ", matrixAdj)
    # v = sorted(matrixAdj.keys(), key=lambda x: matrixAdj[x]["nbV"])

    nbVerticesBlanc = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj.keys()))

    i = 0
    while len(nbVerticesBlanc) != 0:
        nbVerticesBlanc = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj.keys()))
        if len(nbVerticesBlanc) == 0:
            break
        print("nbVerticesBlanc : ", nbVerticesBlanc)
        v = max(nbVerticesBlanc, key=lambda x: matrixAdj[x]['nbV'])
        if v == 915:
            i += 1
        # v = 1
        print("maxVbN : ", v)

        D.add(v)
        print("     + verticesToVisite : ", verticesToVisite)
        # verticesToVisite.remove(v)
        matrixAdj[v]['color'] = 'black'

        # les voisins vont devenir gris
        neighbor_v = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[v]["voisins"]))
        listNeighbor_vn = set()

        # supprition des voisins (blanc >> girs)
        # verticesToVisite = list(set(verticesToVisite) - set(neighbor_v))
        print("     - verticesToVisite : ", verticesToVisite)
        print("     * neighbor_v : ", neighbor_v)

        if len(neighbor_v) == 0:
            continue
        for vn in neighbor_v:
            matrixAdj[vn]['color'] = 'gris'
            # les voisins des voisins vont devenir bleu
            neighbor_vn = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[vn]["voisins"]))
            # supprition des voisins des voinsins (blanc >> bleu)
            # verticesToVisite = list(set(verticesToVisite) - set(neighbor_vn))
            # se sevenir des voisins des voisins pour le moment d'élire un condidat rouge
            listNeighbor_vn = reduce(or_, [listNeighbor_vn, neighbor_vn])

            for vnn in neighbor_vn:
                if matrixAdj[vnn]['color'] == 'blanc':
                    matrixAdj[vnn]['color'] = 'bleu'

        # print("     gris : ", set(filter(lambda x: matrixAdj[x]["color"] == "gris", matrixAdj.keys())))
        # print("     bleu : ", set(filter(lambda x: matrixAdj[x]["color"] == "bleu", matrixAdj.keys())))

        print("     AV listNeighbor_vn : ", listNeighbor_vn)
        listNeighbor_vn = set(filter(lambda x: matrixAdj[x]["color"] == 'bleu', listNeighbor_vn))
        if len(listNeighbor_vn) == 0:
            print('         color v : ', matrixAdj[v]['color'])
            continue
        print("     AP listNeighbor_vn : ", listNeighbor_vn)
        # on doit trouver le v à partir des noeud bleu
        # on doit vérifier tt les voisins de chaque bleu
        # tt les bleu doivent doivent se mettre d'accord sur un noeud

        # on doit choisir le milleur parmi tt les noeud qui vont etre proposé par chaque neud bleu

        valueRedV = -1
        redV = None
        tupleVbPro = set()
        for vb in listNeighbor_vn:
            # on chechre un condidat pour devenir rouge (le condidat est forcement blanc)
            tupleVbPro = reduce(or_, [tupleVbPro, set(map(lambda x: (x, pro(matrixAdj, x)),
                                                          filter(lambda x: matrixAdj[x]["color"] == "blanc"
                                                                 , matrixAdj[vb]["voisins"])
                                                          ))])

        print("     tupleVbPro : ", tupleVbPro)
        # le noeud qui va devenir rouge !

        if len(tupleVbPro) == 0:
            # donc y a plus de noeuds blanc alors on doit choisir parmi les noeud bleu
            tupleVbPro = set(map(lambda x: (x, pro(matrixAdj, x)), listNeighbor_vn))

        maxVbN = max(tupleVbPro, key=lambda x: x[1])
        print("     maxVbN : ", maxVbN)
        matrixAdj[maxVbN[0]]['color'] = 'red'  # on a trouver notre noeud rouge
        print("     le new red : ", maxVbN[0])

        # mnt faut choisir les dominants qui sont les voisins de maxVbN, (trouver un max matching des voisins de mxVbN)
        I = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[maxVbN[0]]["voisins"]))
        if len(I) == 0:
            # alors le rouge n'a plus de voisins balnc => il va devenir noir
            matrixAdj[maxVbN[0]]['color'] = 'black'
            D.add(maxVbN[0])
            # continue
        else:
            print("     I : ", I)
            dominant = getDominant(matrixAdj, I)
            print("     dominant : ", dominant)
            for d in dominant:
                matrixAdj[d]['color'] = 'black'
                D.add(d)
            # il va redevenir blanc
            matrixAdj[maxVbN[0]]['color'] = 'blanc'  # on a trouver notre noeud rouge

            # reprendre les bleu
            bleu = set(filter(lambda x: matrixAdj[x]["color"] == "bleu", matrixAdj[maxVbN[0]]["voisins"]))
            for b in bleu:
                matrixAdj[b]['color'] = 'gris'

            # verticesWithDegreeVal(matrixAdj, tupleVbPro, valueRedV)

    print("D : ", len(D))
    return D


def getDominant(matrixAdj, listVertices):
    dominant = set()
    tupleVbPro = set(map(lambda x: (x, pro(matrixAdj, x)), listVertices))
    maxVbN = max(tupleVbPro, key=lambda x: x[1])
    print("      * maxVbN : ", maxVbN)
    return verticesWithDegreeVal(matrixAdj, tupleVbPro, maxVbN[1])


def independant(matrixAdj, listVertices, v):
    """

    :param listVertices:
    :param v:
    :return: true si v est independant avec tt les noeuds de listVertices
    """
    # pour chque elements de la liste je doit vérifeir si v n'est pas dans
    # leurs voisins
    # donc je doit récupérer tt les voisins de chaque elements de la liste
    # puis vérfier si il est a l'intérieur (fair un if in en O(n)

    allNeighborInList = list(map(lambda x: matrixAdj[x]['voisins'], listVertices))
    if len(allNeighborInList) == 0:
        return True
    allNeighborInList = set(reduce(add, allNeighborInList))

    return not (v in allNeighborInList)


def verticesWithDegreeVal(matrixAdj, tupleVbPro, deg):
    result = set()
    for elem in tupleVbPro:
        if elem[1] == deg:
            # vérifier qu'il est independant avec les noeuds dans result
            if independant(matrixAdj, result, elem[0]):
                result.add(elem[0])
    print("         * result : ", result)
    return result
