# -*- coding: utf-8 -*-
import seaborn as sns
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF


def basic_test(data):
    m, s = sp.stats.norm.fit(data)
    return "{} : Wartosc srednia wynosi {} a odchylenie standardowe {}.".format(data.name, round(m, 3), round(s, 3))

def skew_test(data):
    test1 = sp.stats.skewtest(data)
    st, pv = test1
    print("{} : Test skośności. H0: skosnosc = 0, H1: skosnosc != 0\nP-value wynosi : {}"
          .format(data.name, round(pv, 2)))
    if pv > 0.05:
        return "Nie ma podstaw do odrzucenia hipotezy 0"
    if pv < 0.05:
        return "Orzucono hipoteze 0 na rzecz hipotezy 1"

def kurtosis_test(data):
    test = sp.stats.kurtosistest(data)
    st, pv = test
    print("{} : Test kurtozy. H0: kurtoza = 3, H1: kurtoza != 3\nP-value wynosi : {}".format(data.name, round(pv, 2)))
    if pv > 0.05:
        return "Nie ma podstaw do odrzucenia hipotezy 0"
    if pv < 0.05:
        return "Orzucono hipoteze 0 na rzecz hipotezy 1"

def shapiro_test(data):
    test = sp.stats.shapiro(data)
    st, pv = test
    print("{} : Test Shapiro-Wilka. H0: kurtoza = 3 i skosnosc = 0, H1: kurtoza != 3 lub/i skosnosc !=0\n"
          "P-value wynosi:{}".format(data.name, round(pv, 2)))
    if pv > 0.05:
        return "Nie ma podstaw do odrzucenia hipotezy 0"
    if pv < 0.05:
        return "Orzucono hipoteze 0 na rzecz hipotezy 1"

def kstest_test(data):
    m, s = sp.stats.norm.fit(data)
    test = sp.stats.kstest(data, 'norm', args=(m, s))
    pv = test.pvalue
    print("{} : Test Kołomogorowa-Smirnowa porownuje dystrybuanty\n"
          "P-value wynosi:{}".format(data.name, round(pv, 2)))
    if pv > 0.05:
        return "Nie ma podstaw do odrzucenia hipotezy 0"
    if pv < 0.05:
        return "Orzucono hipoteze 0 na rzecz hipotezy 1"


def plot_test(data, i=0):
    plt.figure(i)
    m, s = sp.stats.norm.fit(data)
    plt.subplot(131)
    plt.axis([0, 130, 0, 1])
    ecdf = ECDF(data)
    plt.step(ecdf.x, ecdf.y, 'r-', label=r'$\hat{F}_n(x)$')

    t1 = np.linspace(-50, 170, 150)
    t2 = sp.stats.norm.cdf(t1, loc=m, scale=s)
    t3 = sp.stats.norm.pdf(t1, loc=m, scale=s)
    plt.plot(t1, t2, 'b--', label=r'$\mathrm{N}(%.2f, %.2f)$' % (m, s))
    plt.legend(loc='best')

    plt.subplot(132)
    sns.distplot(data, bins=8, color='k')
    plt.plot(t1, t3, 'g--')

    plt.subplot(133)
    sp.stats.probplot(data, dist=sp.stats.norm, plot=plt)


