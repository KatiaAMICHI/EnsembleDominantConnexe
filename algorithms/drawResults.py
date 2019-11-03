import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import sqrt


def main1():
    file = "../result/ResultDBs.csv"

    data = pd.read_csv(file)

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
                      "GADB": (data['NBalgoLi&'][1], data['NBalgoA'][1]),
                      "GADB_var": (
                          0.0,
                          0.0)}

    # 1 plot results Times
    plot1_2Results("Result Time Execution CDS problem", "Times (s)", dataResultTime, var=False, path='Discussion/')
    plot1_2Results("Result size of CDS ", "size(CDS)", dataResultSize, var=False, path='Discussion/')


def plot1_2Results(title, ylabel, data, var=True, path='', percentage=False):
    # ('BBR19', 'LS', 'DC')
    # ('S-MIS', 'S-MISopti', 'algoK')

    n_groups = 3

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.10

    opacity = 0.3
    error_config = {'ecolor': '0.3'}

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
    plt.xticks(index + bar_width / 2, ('S-MIS', 'algoK'))
    plt.legend()

    plt.tight_layout()

    # plt.savefig('../png/' + path + title + '.png')

    plt.show()


main1()
