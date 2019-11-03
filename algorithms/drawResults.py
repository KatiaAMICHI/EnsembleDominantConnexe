import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main1():
    file = "../result/ResultDBs.csv"

    data = pd.read_csv(file)

    # varian

    cmd = "awk -F',' '{sumLiT+=($4*$4-" + str(data['TalgoLi&'][0] * data['TalgoLi&'][0]) + ")} " + \
          "{sumMT+=($5*$5-" + str(data['TalgoA'][0] * data['TalgoA'][0]) + ")} " + \
          "{sumLiNb+=($7*$7-" + str(data['NBalgoLi&'][0] * data['NBalgoLi&'][0]) + ")}  " + \
          "{sumMNB+=($8*$8-" + str(data['NBalgoA'][0] * data['NBalgoA'][0]) + ")} " + \
          "END{print sqrt(sumLiT/" + str(data['nbFile'][0]) + "), " + \
          "sqrt(sumMT/" + str(data['nbFile'][0]) + "), " + \
          "sqrt(sumLiNB/" + str(data['nbFile'][0]) + "), " + \
          "sqrt(sumMNB/" + str(data['nbFile'][0]) + ")}' ../result/GenJava/resultsFilesGenJava.csv"

    listData = os.popen(cmd).read()
    varGenJava = list(map(float, listData.split(" ")))

    cmd = "awk -F',' '{sumLiT+=($4*$4-" + str(data['TalgoLi&'][1] * data['TalgoLi&'][1]) + ")} " + \
          "{sumMT+=($5*$5-" + str(data['TalgoA'][1] * data['TalgoA'][1]) + ")} " + \
          "{sumLiNb+=($7*$7-" + str(data['NBalgoLi&'][1] * data['NBalgoLi&'][1]) + ")}  " + \
          "{sumMNB+=($8*$8-" + str(data['NBalgoA'][1] * data['NBalgoA'][1]) + ")} " + \
          "END{print sqrt(sumLiT/" + str(data['nbFile'][1]) + "), " + \
          "sqrt(sumMT/" + str(data['nbFile'][1]) + "), " + \
          "sqrt(sumLiNB/" + str(data['nbFile'][1]) + "), " + \
          "sqrt(sumMNB/" + str(data['nbFile'][1]) + ")}' ../result/GenJava/resultsFilesGenJava.csv"

    listData = os.popen(cmd).read()
    varGenNetworkx = list(map(float, listData.split(" ")))

    cmd = "awk -F',' '{sumLiT+=($4*$4-" + str(data['TalgoLi&'][2] * data['TalgoLi&'][2]) + ")} " + \
          "{sumMT+=($5*$5-" + str(data['TalgoA'][2] * data['TalgoA'][2]) + ")} " + \
          "{sumLiNb+=($7*$7-" + str(data['NBalgoLi&'][2] * data['NBalgoLi&'][2]) + ")}  " + \
          "{sumMNB+=($8*$8-" + str(data['NBalgoA'][2] * data['NBalgoA'][2]) + ")} " + \
          "END{print sqrt(sumLiT/" + str(data['nbFile'][2]) + "), " + \
          "sqrt(sumMT/" + str(data['nbFile'][2]) + "), " + \
          "sqrt(sumLiNB/" + str(data['nbFile'][2]) + "), " + \
          "sqrt(sumMNB/" + str(data['nbFile'][2]) + ")}' ../result/GenJava/resultsFilesGenJava.csv"

    listData = os.popen(cmd).read()
    varGenGA = list(map(float, listData.split(" ")))

    dataResultTime = {"JavaDB": (data['TalgoLi&'][0], data['TalgoA'][0]),
                      "JavaDB_var": (
                          0.0,
                          0.0),
                      "NetworkxDB": (data['TalgoLi&'][1], data['TalgoA'][1]),
                      "NetworkxDB_var": (
                          0.0,
                          0.0),
                      "GADB": (data['TalgoLi&'][1], data['TalgoA'][1]),
                      "GADB_var": (
                          0.0,
                          0.0)}

    dataResultSize = {"JavaDB": (data['NBalgoLi&'][0], data['NBalgoA'][0]),
                      "JavaDB_var": (
                          0.0,
                          0.0),
                      "NetworkxDB": (data['NBalgoLi&'][1], data['NBalgoA'][1]),
                      "NetworkxDB_var": (
                          0.0,
                          0.0),
                      "GADB": (data['NBalgoLi&'][2], data['NBalgoA'][2]),
                      "GADB_var": (
                          0.0,
                          0.0)}

    # 1 plot results Times
    plot1_2Results("Result Time Execution CDS problem", "Times (s)", dataResultTime, var=False,
                   path='../resultRaport/png/')

    # 1 plot results size
    plot1_2Results("Result nombre of nodes in CDS", "nombre of nodes", dataResultSize, var=False,
                   path='../resultRaport/png/')


def plot1_2Results(title, ylabel, data, var=True, path='', percentage=False):
    # ('BBR19', 'LS', 'DC')
    # ('S-MIS', 'S-MISopti', 'algoK')

    n_groups = 2

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.10

    opacity = 0.2
    error_config = {'ecolor': '0.2'}

    rects1 = plt.bar(index - bar_width, data["JavaDB"], bar_width,
                     alpha=opacity,
                     color='b',
                     yerr=data["JavaDB_var"],
                     error_kw=error_config,
                     label='JavaDB')

    rects2 = plt.bar(index, data["NetworkxDB"], bar_width,
                     alpha=opacity,
                     color='r',
                     yerr=data["NetworkxDB_var"],
                     error_kw=error_config,
                     label='NetworkxDB')

    rects3 = plt.bar(index + bar_width, data["GADB"], bar_width,
                     alpha=opacity,
                     color='g',
                     yerr=data["GADB_var"],
                     error_kw=error_config,
                     label='GADB')

    plt.xlabel('Algorithms')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index + bar_width, ('S-MIS', 'MCDS'))
    plt.legend()

    plt.tight_layout()

    plt.savefig(path + title.replace(' ', '_') + '.png')

    plt.show()


main1()
