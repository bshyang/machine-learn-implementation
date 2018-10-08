# -*- coding: utf-8 -*-

import os, sys
import numpy

def loadDataSet(fileName):
    #加载数据
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        #每一行就是一组数据
        curLine = line.strip().split("\t")
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):
    #欧式距离计算公式
    return numpy.sqrt(numpy.sum(numpy.power(vecA - vecB, 2)))

def randCent(dataSet, k):
    #随机产生k个聚类中心
    #聚类中心，是介于最大值和最小值之间产生k个聚类中心
    #随机数，乘以数值范围
    n = numpy.shape(dataSet)[1]
    centroids = numpy.mat(numpy.zeros((k,n)))
    for j in range(n):
        minJ = numpy.min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * numpy.random.rand(k, 1)
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    n = numpy.shape(dataSet)[0]
    clusterAssment = numpy.mat(numpy.zeros((n,2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(n):
            minDist = numpy.inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist**2
        print centroids
        #更新聚类中心的函数
        for cent in range(k):
            #nonzero 是取非零元素的位置，的函数。
            #这里的目的是更新聚类中心
            ptsInClust = dataSet[numpy.nonzero(clusterAssment[:,0].A == cent)[0]]
            centroids[cent,:] = numpy.mean(ptsInClust, axis=0)
    return centroids, clusterAssment

def biKmeans(dataSet, k, distMeas=distEclud):
    #样本数量
    m = numpy.shape(dataSet)[0]
    #提前空置容器
    clustAssment = numpy.mat(numpy.zeros((m,2)))
    centroid0 = numpy.mean(dataSet, axis=0).tolist()[0]
    centList = [centroid0]
    for j in range(m):
        #距离计算
        clustAssment[j,1] = distMeas(numpy.mat(centroid0), dataSet[j, :])**2
    while (len(centList) < k):
        lowestSSE = numpy.inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[numpy.nonzero(clustAssment[:, 0].A == i)[0], :]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:, 1])
            sseNotSplit = sum(clustAssment[numpy.nonzero(clustAssment[:, 0].A != i)[0], 1])
            print "sseSplit, and NotSplit: ", sseSplit, sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[numpy.nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClustAss[numpy.nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        print "the bestCentToSplit is :", bestCentToSplit
        print "the len of bestClustAss is :", len(bestClustAss)
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]
        centList.append(bestNewCents[1, :].tolist()[0])
        clustAssment[numpy.nonzero(clustAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss
    return numpy.mat(centList), clustAssment

if __name__ == "__main__":
    #dataMat = loadDataSet("testSet.txt")
    #print len(dataMat)
    #print dataMat
    #print distEclud(dataMat[0][0], dataMat[0][1])
    #print numpy.shape(dataMat)
    #myCentroids, clustAssing = kMeans(numpy.mat(dataMat), 4)
    #print myCentroids
    #print clustAssing
    dataMat2 = loadDataSet("testSet2.txt")
    Centroids, clustAssment = biKmeans(numpy.mat(dataMat2), 3)
    print Centroids