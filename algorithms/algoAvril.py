from functools import reduce
from operator import or_, and_


def pro(matrixAdj, v):
    return len(set(filter(lambda x: (matrixAdj[x]["color"] == "blanc" or
                                     matrixAdj[x]["color"] == "bleu")
                          , matrixAdj[v]["voisins"])))


def IC_MIS(matrixAdj):
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
        i += 1
        nbVerticesBlanc = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj.keys()))
        if len(nbVerticesBlanc) == 0:
            break
        print("nbVerticesBlanc : ", nbVerticesBlanc)
        v = max(nbVerticesBlanc, key=lambda x: matrixAdj[x]['nbV'])
        print("maxVbN (rouge): ", v)

        # v est notre condidat rouge (es ce qu'il va devenir dominant ou ces voisant qui vont le devenir
        # D.add(v)
        # verticesToVisite.remove(v)
        matrixAdj[v]['color'] = 'red'

        # .............................. recherche des dominant du rouge ...............................
        # mnt faut choisir les dominants qui sont les voisins de maxVbN, (trouver un max matching des voisins de mxVbN)
        I = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[v]["voisins"]))

        # .............................. choix les dominant du rouge ou le rouge ...............................
        matrixAdj, D, listNeighbor_vn = addDominant(matrixAdj, D, I, v, True)
        print("     comment je suis devenu : ", matrixAdj[v]['color'])
        # ........................................;
        # tt se passe dans [addDominant]
        # ........................................;

        print("     gris : ", set(filter(lambda x: matrixAdj[x]["color"] == "gris", matrixAdj.keys())))
        print("     bleu : ", set(filter(lambda x: matrixAdj[x]["color"] == "bleu", matrixAdj.keys())))
        if listNeighbor_vn:
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

            # .............................. recherche d'un condidat rouge ...............................
            vRed = getRedVertice(matrixAdj, listNeighbor_vn)
            matrixAdj[vRed]['color'] = 'red'  # on a trouver notre noeud rouge
            print("     le new red : ", vRed)

            # .............................. recherche des dominant du rouge ...............................
            # mnt faut choisir les dominants qui sont les voisins de maxVbN, (trouver un max matching des voisins de mxVbN)
            I = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[vRed]["voisins"]))
            print("     I : ", I)
            # .............................. choix les dominant du rouge ou le rouge ...............................
            matrixAdj, D, listNeighbor_vn = addDominant(matrixAdj, D, I, vRed, False)

        print("     D : ", len(D))
        print("     F bleu : ", set(filter(lambda x: matrixAdj[x]["color"] == "bleu", matrixAdj.keys())))

        print("D : ", len(D))
    # return D
    return D, matrixAdj


def propagation(matrixAdj, listNeighbor_vn, v):
    # les voisins vont devenir gris
    # print("         * [propagation] v : ", v)
    neighbor_v = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[v]["voisins"]))

    # supprition des voisins (blanc >> girs)
    # verticesToVisite = list(set(verticesToVisite) - set(neighbor_v))
    # print("     - verticesToVisite : ", verticesToVisite)
    # print("         [propagation] neighbor_v : ", neighbor_v)

    if len(neighbor_v) != 0:
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
    # print("         [propagation] listNeighbor_vn : ", listNeighbor_vn)

    return matrixAdj, listNeighbor_vn


def addDominant(matrixAdj, D, I, vRed, blanc):
    print("     [addDominant] independant(matrixAdj, D, vRed) : ", independant(matrixAdj, D, vRed))
    listVertices = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[vRed]["voisins"]))

    tupleVbPro = set(map(lambda x: (x, pro(matrixAdj, x)), listVertices))
    print("     [addDominant] tupleVbPro : ", tupleVbPro)

    maxVbN = -1
    if len(tupleVbPro) > 0:
        maxVbN = max(tupleVbPro, key=lambda x: x[1])[1]
        print("     [addDominant] maxVbN : ", maxVbN)

    print("     [addDominant] if : ", (independant(matrixAdj, D, vRed) or maxVbN == 0))
    # si maxVbN == 0 alors on a pas le coix le noeud est forcement parmi les dominant
    if len(I) == 0 and (independant(matrixAdj, D, vRed) or maxVbN == 0):
        print("         c'est moi le dominant (rouge => noir")
        # alors le rouge n'a plus de voisins blanc => il va devenir noir
        matrixAdj[vRed]['color'] = 'black'
        D.add(vRed)

        # mes voisins vont devenir gris
        listNeighbor_vn = set()
        matrixAdj, listNeighbor_vn = propagation(matrixAdj, listNeighbor_vn, vRed)
        # print("         [addDominant] listNeighbor_vn : ", listNeighbor_vn)
        if not blanc:
            # on arrete la propagation:
            bleu = set(filter(lambda x: matrixAdj[x]["color"] == "bleu", matrixAdj))
            if matrixAdj[vRed]['color'] == 'black':
                for b in bleu:
                    matrixAdj[b]['color'] = 'gris'

        return matrixAdj, D, listNeighbor_vn
    elif len(I) != 0:
        print("     (v:rouge)I : ", I)
        dominant = getDominant(matrixAdj, I, vRed)
        print("     (v:rouge)dominant : ", dominant)

        for d in dominant:
            if not blanc and matrixAdj[d]['color'] == 'blanc':
                # blanc = True
                pass
            if independant(matrixAdj, D, d) or maxVbN == 0:
                matrixAdj[d]['color'] = 'black'
                D.add(d)
            else:
                matrixAdj[d]['color'] = 'gris'
        if matrixAdj[vRed]['color'] != 'black':
            matrixAdj[vRed]['color'] = 'blanc'
        print("     A (v:rouge)d [color] : ", vRed, " : ", matrixAdj[vRed]['color'])

        if blanc:
            # faut élire un nouveu rouge
            # faut retourner en haut et continué
            # faut retourner la ouvelle liste de bleu

            listNeighbor_vn = set()
            print("     ***** propagation ******* ")
            # on doit propager le message à deux saut de notre dominant
            for d in dominant:
                if matrixAdj[d]['color'] != 'black':
                    continue
                matrixAdj, listNeighbor_vn = propagation(matrixAdj, listNeighbor_vn, d)
            print("         [bleu] listNeighbor_vn : ", listNeighbor_vn)
            print("     B (v:rouge)d [color] : ", matrixAdj[vRed]['color'])

            if matrixAdj[vRed]['color'] != 'black':
                matrixAdj[vRed]['color'] = 'blanc'
            print("     C (v:rouge)d [color] : ", matrixAdj[vRed]['color'])

            return matrixAdj, D, listNeighbor_vn

        # reprendre les bleu (bleu vers gris pour les voisins des dominant qui ont était ajouter)
        for d in dominant:
            if matrixAdj[d]['color'] != 'black':
                continue
            print("     (v:rouge) d  :", d)
            bleu = set(filter(lambda x: matrixAdj[x]["color"] == "bleu", matrixAdj[d]["voisins"]))
            for b in bleu:
                matrixAdj[b]['color'] = 'gris'

        bleu = set(filter(lambda x: matrixAdj[x]["color"] == "bleu", matrixAdj))
        for b in bleu:
            matrixAdj[b]['color'] = 'blanc'

        # il va redevenir blanc
        # matrixAdj[vRed]['color'] = 'blanc'  # on a trouver notre noeud rouge
    matrixAdj[vRed]['color'] = 'blanc'
    return matrixAdj, D, None


def getRedVertice(matrixAdj, listNeighbor_vn):
    tupleVbPro = set()
    for vb in listNeighbor_vn:
        # on chechre un condidat pour devenir rouge (le condidat est forcement blanc)
        tupleVbPro = reduce(or_, [tupleVbPro, set(map(lambda x: (x, pro(matrixAdj, x)),
                                                      filter(lambda x: matrixAdj[x]["color"] == "blanc"
                                                             , matrixAdj[vb]["voisins"])
                                                      ))])

    # print("     tupleVbPro : ", tupleVbPro)
    # le noeud qui va devenir rouge !

    if len(tupleVbPro) == 0:
        # donc y a plus de noeuds blanc alors on doit choisir parmi les noeud bleu
        tupleVbPro = set(map(lambda x: (x, pro(matrixAdj, x)), listNeighbor_vn))

    maxVbN = max(tupleVbPro, key=lambda x: x[1])
    # print("     maxVbN : ", maxVbN)
    return maxVbN[0]


def poidsV(matrixAdj, D, v):
    """
    Calculer le poind d'un noeud
    :param matrixAdj:
    :param D:
    :param v:
    :return:
    """
    # def 5
    verticesBlack = set(filter(lambda x: matrixAdj[x]["color"] == "black", matrixAdj[v]['voisins']))
    verticesGris = set(filter(lambda x: matrixAdj[x]["color"] == "gris", matrixAdj[v]['voisins']))

    return 2 * len(verticesBlack) + len(verticesGris)


def poidsE(matrixAdj, D, u, v):
    """
    Calculer le poind d'une arrete
    :param matrixAdj:
    :param D:
    :param u:
    :param v:
    :return:
    """
    # def 6
    return 1 / (len(reduce(and_, [matrixAdj[v]['voisins'], matrixAdj[u]['voisins']])))


def Kruskal(matrixAdj, D):
    C = set()
    E = set()

    # prend un noeud
    s = D[0]
    for s in D:
        # si s a un noeud noir comme voisins alors on pass (?)
        # nbVerticesBlanc = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj.keys()))

        # cherche le noeud noir d qui est à deux saut de s
        neighborS = matrixAdj[s]['voisins']

        for ns in neighborS:
            if matrixAdj[ns]['color'] == 'black':
                break
            neighbor_ns = set(filter(lambda x: matrixAdj[x]["color"] == "black", neighborS))
            if len(neighbor_ns) != 0:
                t = ns
                d = list(neighborS)[0]
                if (s, t) not in E or (t, d) not in E:
                    matrixAdj[t]['color'] = 'bleu'
                    C.add(d)
                    E.add((s, t))
                    E.add((t, d))
                    break

    # print("C : ", len(C))
    # print("E : ", E)
    return C


def getDominant(matrixAdj, listVertices, v):
    print("     [getDominat] listVertices : ", listVertices)
    valV = pro(matrixAdj, v)
    tupleVbPro = set(map(lambda x: (x, pro(matrixAdj, x)), listVertices))
    print("     [getDominat] tupleVbPro : ", tupleVbPro)
    maxVbN = max(tupleVbPro, key=lambda x: x[1])
    if maxVbN[1] == 0:
        maxVbN = (v, valV)
        return {v}
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

    allNeighborInList = list(map(lambda x: set(matrixAdj[x]['voisins']), listVertices))
    if len(allNeighborInList) == 0:
        return True

    # print("     , AV [independant] allNeighborInList : ", allNeighborInList)

    # for elem in allNeighborInList:
    #    print("     elem : ", elem)

    allNeighborInList = reduce(set.union, allNeighborInList)
    # allNeighborInList = set(reduce(add, allNeighborInList))

    # print("     , AP [independant] allNeighborInList : ", allNeighborInList)

    return not (v in allNeighborInList)


def verticesWithDegreeVal(matrixAdj, tupleVbPro, deg):
    result = set()
    # print("     . [verticesWithDegreeVal] tupleVbPro : ", tupleVbPro)
    for elem in tupleVbPro:
        if elem[1] == deg:
            # vérifier qu'il est independant avec les noeuds dans result
            # print("     . [verticesWithDegreeVal] result : ", result)
            if independant(matrixAdj, result, elem[0]):
                result.add(elem[0])
    print("         * result : ", result)
    return result
