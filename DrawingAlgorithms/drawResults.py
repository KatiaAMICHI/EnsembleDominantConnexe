#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def autolabel(ax, rects, percentage=False):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = int(rect.get_height())
        if height < 1:
            continue
        value = height
        if percentage:
            value = str(height) + '%'

        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * int(height),
                value,
                ha='center', va='bottom')


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
                      "GADB": (data['NBalgoLi&'][2], data['NBalgoA'][2]),
                      "GADB_var": (
                          0.0,
                          0.0)}

    # 1 plot results Times
    plot1_2Results("Result Time Execution CDS problem", "Times (s)", dataResultTime, var=False,
                   path='../resultRaport/png/')

    # 1 plot results size
    plot1_2Results("Result numbre of nodes in CDS", "numbre of nodes", dataResultSize, var=False,
                   path='../resultRaport/png/')


def main_pourcentage():
    file = "../result/ResultDBs.csv"

    data = pd.read_csv(file)

    # varian

    dataResultSize = {"JavaDB": (data['NBalgoLi&'][0] / data['V'][0] * 100, data['NBalgoA'][0] / data['V'][0] * 100),
                      "JavaDB_var": (
                          0.0,
                          0.0),
                      "NetworkxDB": (
                      data['NBalgoLi&'][1] / data['V'][1] * 100, data['NBalgoA'][1] / data['V'][1] * 100),
                      "NetworkxDB_var": (
                          0.0,
                          0.0),
                      "GADB": (data['NBalgoLi&'][2] / data['V'][2] * 100, data['NBalgoA'][2] / data['V'][2] * 100),
                      "GADB_var": (
                          0.0,
                          0.0)}

    # 1 plot results size
    plot1_2Results("Result percentage numbre of nodes in CDS", "percentage of numbre of nodes", dataResultSize,
                   var=False,
                   path='../resultRaport/png/', percentage=True)


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
    if percentage:
        plt.ylim(0, 100)
        plt.xlim(-1, 2)
        autolabel(ax, rects1, percentage)
        autolabel(ax, rects2, percentage)
        autolabel(ax, rects3, percentage)

    plt.savefig(path + title.replace(' ', '_') + '.png')

    plt.show()


main_pourcentage()
main1()
