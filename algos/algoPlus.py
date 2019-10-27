from algos.EnsembleDSageM import *
from functools import reduce


def hasNeighborWhile(matrixAdj, v):
    return len(set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[v]["voisins"]))) > 0


def MISC(matrixAdj):
    VerticesWhite = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj.keys()))
    VerticesRed = set(filter(lambda x: matrixAdj[x]["color"] == "red", matrixAdj.keys()))

    i = 0
    while len(VerticesWhite) != 0:
        VerticesBlack = set(filter(lambda x: matrixAdj[x]["color"] == "black", matrixAdj.keys()))
        VerticesRed = set(filter(lambda x: matrixAdj[x]["color"] == "red", matrixAdj.keys()))
        print("     -- nb black :", VerticesBlack)
        print("     -- nb red :", VerticesRed)
        print("     -- nb white :", VerticesWhite)

        i += 1
        # maxvMD : verticeMaxDegree blanc
        tupleVerticesRV = list(map(lambda x: (x,
                                              len(list(filter(lambda xn: (matrixAdj[x]["color"] != "black" and
                                                                          matrixAdj[xn]["color"] != "black"),
                                                              matrixAdj[x]["voisins"])))),
                                   matrixAdj.keys()))

        # prendre le rouge avec le plus de voisins blanc
        maxvMD = max(tupleVerticesRV, key=lambda x: x[1])
        if maxvMD[1] == 0:
            continue
        # TODO faut rajouter une condition qui dit : si un noeud est déja connecte dans le graph pas besoin de le rajouter comme noir
        # je pense qu'on a pas besoin

        tupleVerticesRV.remove(maxvMD)
        print("vMD : ", maxvMD)

        print("       je doit supp : ", maxvMD[0])
        if matrixAdj[maxvMD[0]]['color'] == 'blanc':
            print("       >> je supp : ", maxvMD[0])
            VerticesWhite.remove(maxvMD[0])
        matrixAdj[maxvMD[0]]['color'] = 'black'

        # tous les voisins blanc de maxvMD vont devenir rouge
        neighbor_vMD = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[maxvMD[0]]["voisins"]))
        VerticesWhite = list(set(VerticesWhite) - set(neighbor_vMD))
        for vn in neighbor_vMD:
            matrixAdj[vn]['color'] = 'red'
            # VerticesWhite.remove(vn)

        # si maxvMD est rouge, tous les voisins rouge de maxvMD vont devenir gris
        if matrixAdj[maxvMD[0]]['color'] == 'red':
            neighbor_vMD = set(filter(lambda x: matrixAdj[x]["color"] == "red", matrixAdj[maxvMD[0]]["voisins"]))
            for vn in neighbor_vMD:
                matrixAdj[vn]['color'] = 'gris'

        # supprimier tt les noeud rouge qui n'ont pas de blanc en voisins
        # neighbor_v red
        neighbor_vR = set(filter(lambda x: matrixAdj[x]["color"] == "red", matrixAdj[maxvMD[0]]["voisins"]))
        print("     neighbor_vR : ", neighbor_vR)
        for vn in neighbor_vR:
            if not hasNeighborWhile(matrixAdj, vn):
                matrixAdj[vn]['color'] = 'gris'

        VerticesBlack = set(filter(lambda x: matrixAdj[x]["color"] == "black", matrixAdj.keys()))
        VerticesRed = set(filter(lambda x: matrixAdj[x]["color"] == "red", matrixAdj.keys()))
        print("     ++ nb black :", len(VerticesBlack))
        print("     ++ nb red :", len(VerticesRed))
        print("     ++ nb while :", len(VerticesWhite))
    # pprint.pprint(matrixAdj)


def MISCV(matrixAdj):
    i = 0
    VerticesWhite = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj.keys()))
    l = [0, 1, 2, 3]
    sorted_d = sorted(l, key=lambda x: matrixAdj[x]["nbV"])
    print("sorted_d : ", sorted_d)

    # verticeMaxDegree
    vMD = getMaxVwDegree(matrixAdj)
    print("vMD : ", vMD)

    while (VerticesWhite):
        if i == 1:
            break
        i += 1
        matrixAdj[vMD]["color"] = "black"
        # récupérer que les voisins blanc
        neighbor_vMD = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[vMD]["voisins"]))

        print("     neighbor_vMD : ", neighbor_vMD)
        print("     sum : ", sum)

        # pour chacun des voisins vérfier s'il a des voisins blanc
        # map(lambda x: setattr(matrixAdj[x], 'color', 'red'), neighbor_vMD)
        map(lambda x: matrixAdj[x].update({"color": 'red'}), neighbor_vMD)
        for vn in neighbor_vMD:
            matrixAdj[vn]['color'] = 'gris' if (not hasNeighborWhile(matrixAdj, vn)) else 'red'

        # récupérer la liste des rouge
        redVertices = set(filter(lambda x: matrixAdj[x]["color"] == "red", neighbor_vMD))
        print("     redVertices : ", redVertices)

        # avoir une list de tuple (id, nbVoisinsBlanc)
        tupleVerticesRV = list(map(lambda x: (x,
                                              len(list(filter(lambda xn: matrixAdj[xn]["color"] == "blanc",
                                                              matrixAdj[x]["voisins"])))),
                                   redVertices))
        print("     tupleVerticesRV : ", tupleVerticesRV)

        while len(redVertices) != 0:
            # prendre le rouge avec le plus de voisins blanc
            maxVR = max(tupleVerticesRV, key=lambda x: x[1])
            tupleVerticesRV.remove(maxVR)
            redVertices.remove(maxVR[0])

            # mettre le noeud en noir
            matrixAdj[maxVR[0]]['color'] = 'black'
            # mettre ces voisins en gris
            neighbor_maxVR = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj[maxVR[0]]["voisins"]))
            for vn in neighbor_maxVR:
                matrixAdj[vn]['color'] = 'gris'

        print("     .................................")
        # récupérer la liste des rouge
        redVertices = set(filter(lambda x: matrixAdj[x]["color"] == "red", neighbor_vMD))
        print("     redVertices : ", redVertices)

        # avoir une list de tuple (id, nbVoisinsBlanc)
        tupleVerticesRV = list(map(lambda x: (x,
                                              len(list(filter(lambda xn: matrixAdj[xn]["color"] == "blanc",
                                                              matrixAdj[x]["voisins"])))),
                                   redVertices))
        print("     tupleVerticesRV : ", tupleVerticesRV)


def verticesWithMaxDegree(TupleVertices, degree):
    result = []
    for v in TupleVertices:
        if v[1] == degree:
            result.append(v)
    return result


def minimalDegree(matrixAdj, ListVertices):
    tupleVerticesRV = list(map(lambda x: (x,
                                          len(list(filter(lambda xn: matrixAdj[xn]["color"] == "black",
                                                          matrixAdj[x]["voisins"])))),
                               ListVertices))

    # prendre le rouge avec le plus de voisins blanc (avec le degree max)
    maxVr = min(tupleVerticesRV, key=lambda x: x[1])
    return maxVr


# Algo 1
def IADSP(matrixAdj):
    NbB = set(filter(lambda x: matrixAdj[x]["color"] == "black", matrixAdj.keys()))
    NbR = set(filter(lambda x: matrixAdj[x]["color"] == "red", matrixAdj.keys()))

    if len(NbB) > 0:
        # ne pas selectionnné de noeud rouge comme dominateur
        pass
    if len(NbB) == 0 and len(NbR) > 1:
        # calculer les noeuds indépendant (degree) des ces noeud rouge
        tupleVerticesRV = list(map(lambda x: (x,
                                              len(list(filter(lambda xn: matrixAdj[xn]["color"] == "blanc",
                                                              matrixAdj[x]["voisins"])))),
                                   matrixAdj.keys()))

        # prendre le rouge avec le plus de voisins blanc (avec le degree max)
        maxVr = max(tupleVerticesRV, key=lambda x: x[1])
        k = verticesWithMaxDegree(tupleVerticesRV, maxVr)
        if len(k) == 1:
            # alors il devient dominateur
            matrixAdj[k[0][0]]['color'] = 'black'
        elif len(k) > 1:
            # selectionné celui qui est connecter a moins de noir
            # min vertices red independant (dominateur)
            minVrId = minimalDegree
            matrixAdj[minVrId]['color'] = 'black'
    return k


dominator = dict()


def algo2(matrixAdj):
    v = None  # le noeud sur le qulle on va trvailler

    # si un message gris du voisin j est reçu
    msgG = True
    if msgG:
        # changer le status de ses voisins :
        pass

    # si un message noir du voisoins k est recu
    msgB = True
    if msgB:
        # changer le status de ses voisins :
        # mettre k dans la liste des enfants d'un dominant
        pass

    NbW = set(filter(lambda x: matrixAdj[x]["color"] == "blanc", matrixAdj.keys()))
    NbR = set(filter(lambda x: matrixAdj[x]["color"] == "red", matrixAdj.keys()))

    # si tout les noeud sont soit noir ou gris
    if len(NbW) == 0 and len(NbR) == 0:
        truc = True
        # si le domiant n'a pas d'enfoant qu'il domine alors :
        if truc:
            m = BDPP(matrixAdj)
            if m > 1:
                matrixAdj[v]['color'] = 'gris'
                # défuser le message gris-message a ces voisins


# pour les noeuds blanc
def algo4(matrixAdj):
    v = None # le noeud sur le quel on travaille
    # mettre un temps T pour attendre un message des noeud rouge
    truc1 = False
    # si tout les message des voisins rouge en été reçu ou T a éxpérer alors
    if truc1:
        # algo1
        k = IADSP(matrixAdj)
        # mettre le voisin k dans le message Req-IADSP
        # envoyer le message Rep-IADSP au voinsin sélectionnée k (l'envoyer a k)
        # supprimer T

    truc2 = True
    # si un message gris de j a été reçu
    if truc2:
        # changer le status du voinsin j
        pass

    # si un message noir de j est reçu
    truc3 = True
    if truc3:
        matrixAdj[v]['color'] = 'red'
        # changer le status de son voisins j
        # j va devenir son parent
