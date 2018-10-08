# -*- coding: utf-8 -*-

import os, sys
from numpy import *
reload(sys)
sys.setdefaultencoding('utf-8')

def loadDataSet():
    dataSet = []
    labelMat = []
    fr = open('./data/testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataSet.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataSet, labelMat

def sigmoid(inX):
    return 1.0/(1 + exp(-inX))

def gradAscent(dataMatIn, classLabels):

    return