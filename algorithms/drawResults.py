import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import sqrt


def main1():
    fileT = '.csv'

    data = pd.read_csv(fileT)

    dataTimes = {"JavaBD": (data['BBR19'][0], data['LS'][0], data['LSsort'][0], data['DC'][0]),
                 "JavaBD_var": (
                     data['varNbGMTBBR19'][0] * sqrt(1000),
                     0.0,
                     data['varNbGMTLSsort'][0] * sqrt(1000),
                     data['varNbGMTDC'][0] * sqrt(1000)),
                 "NetworkxDB": (data['BBR19'][1], data['LS'][1], data['LSsort'][1], data['DC'][1]),
                 "NetworkxDB_var": (
                     data['varNbGMTBBR19'][1] * sqrt(1000),
                     0.0,
                     data['varNbGMTLSsort'][1] * sqrt(1000),
                     data['varNbGMTDC'][1] * sqrt(1000)),
                 "GABD": (data['BBR19'][3], data['LS'][3], data['LSsort'][3], data['DC'][3]),
                 "GABD_var": (
                     data['varNbGMTBBR19'][3] * sqrt(1000),
                     0.0,
                     data['varNbGMTLSsort'][3] * sqrt(1000),
                     data['varNbGMTDC'][3] * sqrt(1000))}

    dataNbGM = {"Enron": (data['BBR19'][0], data['LS'][0], data['LSsort'][0], data['DC'][0]),
                "Enron_var": (
                    data['varNbGMBBR19'][0] * sqrt(1000),
                    0.0,
                    data['varNbGMLSsort'][0] * sqrt(1000),
                    data['varNbGMDC'][0] * sqrt(1000)),
                "Rollernet": (data['BBR19'][1], data['LS'][1], data['LSsort'][1], data['DC'][1]),
                "Rollernet_var": (
                    data['varNbGMBBR19'][1] * sqrt(1000),
                    0.0,
                    data['varNbGMLSsort'][1] * sqrt(1000),
                    data['varNbGMDC'][1] * sqrt(1000)),

                "B1": (data['BBR19'][2], data['LS'][2], data['LSsort'][2], data['DC'][2]),
                "B1_var": (
                    data['varNbGMBBR19'][2] * sqrt(1000),
                    0.0,
                    data['varNbGMLSsort'][2] * sqrt(1000),
                    data['varNbGMDC'][2] * sqrt(1000)),

                "B2": (data['BBR19'][3], data['LS'][3], data['LSsort'][3], data['DC'][3]),
                "B2_var": (
                    data['varNbGMBBR19'][3] * sqrt(1000),
                    0.0,
                    data['varNbGMLSsort'][3] * sqrt(1000),
                    data['varNbGMDC'][3] * sqrt(1000))}

    dataCoverRate = {"Enron": (
        data['BBR19'][0] * gamma * 2 * 100 / data['V_living'][0],
        data['LS'][0] * gamma * 2 * 100 / data['V_living'][0],
        data['LSsort'][0] * gamma * 2 * 100 / data['V_living'][0],
        data['DC'][0] * gamma * 2 * 100 / data['V_living'][0]),
        "Enron_var": (0.0, 0.0, 0.0, 0.0),

        "Rollernet": (data['BBR19'][1] * gamma * 2 * 100 / data['V_living'][1],
                      data['LS'][1] * gamma * 2 * 100 / data['V_living'][1],
                      data['LSsort'][1] * gamma * 2 * 100 / data['V_living'][1],
                      data['DC'][1] * gamma * 2 * 100 / data['V_living'][1]),
        "Rollernet_var": (0.0, 0.0, 0.0, 0.0),

        "B1": (data['BBR19'][2] * gamma * 2 * 100 / data['V_living'][2],
               data['LS'][2] * gamma * 2 * 100 / data['V_living'][2],
               data['LSsort'][2] * gamma * 2 * 100 / data['V_living'][2],
               data['DC'][2] * gamma * 2 * 100 / data['V_living'][2]),
        "B1_var": (0.0, 0.0, 0.0, 0.0),

        "B2": (data['BBR19'][3] * gamma * 2 * 100 / data['V_living'][3],
               data['LS'][3] * gamma * 2 * 100 / data['V_living'][3],
               data['LSsort'][3] * gamma * 2 * 100 / data['V_living'][3],
               data['DC'][3] * gamma * 2 * 100 / data['V_living'][3]),
        "B2_var": (0.0, 0.0, 0.0, 0.0)
    }

    # 1 plot results Times
    plot1_2Results("Result Time Execution  γ = " + str(gamma), "Times (s)", dataTimes, var=False, path='Discussion/')


def plot1_2Results(title, ylabel, data, var=True, path='', percentage=False):
    # ('BBR19', 'LS', 'DC')
    # ('S-MIS', 'S-MISopti', 'algoK')

    n_groups = 3

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.15

    opacity = 0.3
    error_config = {'ecolor': '0.3'}

    print(data["Rollernet_var"])
    if not var:
        data["Enron_var"] = 0
        data["Rollernet_var"] = 0
        data["B1_var"] = 0
        data["B2_var"] = 0

    rects1 = plt.bar(index - bar_width, data["JavaBD"], bar_width,
                     alpha=opacity,
                     color='b',
                     yerr=data["JavaBD_var"],
                     error_kw=error_config,
                     label='JavaBD')

    rects2 = plt.bar(index, data["NetworkxBD"], bar_width,
                     alpha=opacity,
                     color='r',
                     yerr=data["NetworkxBD_var"],
                     error_kw=error_config,
                     label='ExtractRollernet')

    rects3 = plt.bar(index + bar_width, data["GABD"], bar_width,
                     alpha=opacity,
                     color='g',
                     yerr=data["GABD_var"],
                     error_kw=error_config,
                     label='GABD')

    plt.xlabel('Algorithms')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index + bar_width / 2, ('S-MIS', 'S-MISopti', 'algoK'))
    plt.legend()

    plt.tight_layout()

    plt.savefig('../png/' + path + title + '.png')

    plt.show()
