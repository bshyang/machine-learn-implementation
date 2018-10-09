# -*- coding: utf-8 -*-

import os, sys
from numpy import *

def loadDataSet(fileName):
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split("\t")
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat

def selectJrand(i,m):
    #i是alpha的下标。输出非本身德下标
    j = i
    while j==i:
        #random generate a number range (0, m)
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj, H, L):
    #调整大于H或小于L的alpha值
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    b = 0
    m,n = shape(dataMat)
    alpha = mat(zeros((m,1)))
    iter = 0
    while iter < maxIter:
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alpha, labelMat).T * (dataMatrix * dataMatrix[i, :].T)) + b
            Ei = fXi - float(labelMat[i])
            if (labelMat[i]*Ei < -toler and alpha[i] < C) or (labelMat[i]*Ei > toler and alpha[i] >0):
                j = selectJrand(i, m)
                fXj = float(multiply(alpha, labelMat).T*(dataMatrix*dataMatrix[j,:].T)) +b
                Ej = fXj - float(labelMat[j])
                alphaIold = alpha[i].copy()
                alphaJold = alpha[j].copy()
                if labelMat[i] != labelMat[j]:
                    L = max(0, alpha[j] - alpha[i])
                    H = min(C, C + alpha[j] - alpha[i])
                else:
                    L = max(0, alpha[j] + alpha[i] - C)
                    H = min(C, alpha[j] + alpha[i])
                if L == H:
                    print  "L == H"
                    continue
                eta = 2.0 * dataMatrix[i, :]*dataMatrix[j, :].T - dataMatrix[i, :]*dataMatrix[i, :].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0:
                    print "eta >= 0"
                    continue
                alpha[j] -= labelMat[j]*(Ei-Ej)/eta
                alpha[j] = clipAlpha(alpha[j], H, L)
                if abs(alpha[j] - alphaJold) < 0.00001:
                    print "J not moving enough"
                    continue
                alpha[i] += labelMat[j]*labelMat[i]*(alphaJold - alpha[j])
                b1 = (b - Ei - labelMat[i] * (alpha[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[i, :].T - labelMat[j] * (alpha[j] - alphaJold) * dataMatrix[i, :] * dataMatrix[j, :].T)
                b2 = (b - Ej - labelMat[i] * (alpha[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T - labelMat[j] * (alpha[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T)
                if 0 < alpha[i] and C > alpha[j]:
                    b = b1
                elif 0 < alpha[j] and C >alpha[j]:
                    b = b2
                else:
                    b = (b1+b2)/2
                alphaPairsChanged += 1
                print "iter %d i :%d, pairs changed %d" % (iter, i, alphaPairsChanged)
        if alphaPairsChanged == 0:
            iter += 1
        else:
            iter = 0
        print "iteration number: %d" % iter
    return b, alpha

if __name__ == "__main__":
    dataMat, labelMat = loadDataSet("testSet.txt")
    print shape(dataMat)
    print labelMat
    b, alpha = smoSimple(dataMat, labelMat, 0.6, 0.001, 40)
    print b, alpha[alpha>0]