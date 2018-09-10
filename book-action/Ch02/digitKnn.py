# -*- coding: UTF-8 -*-

from numpy import *
import os
import operator

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename, 'r')
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i + j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir("./data/trainingDigits")
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split(".")[0]
        classNumStr = int(fileStr.split("_")[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector("./data/trainingDigits/%s" % fileNameStr)
    testFileList = os.listdir("./data/testDigits")
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split(".")[0]
        classNumStr = int(fileStr.split("_")[0])
        vectorUnderTest = img2vector("./data/testDigits/%s" % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat,hwLabels,3)
        print "the classifier came back with : %d, the real answer is :%d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr):
            errorCount += 1
    print "\n the total number of error is : %d" % errorCount
    print "\n the total error rate is : %f " % (errorCount/float(mTest))


def classify0(inX, dataSet, labels, k):
    """
    kNN classify to make a data to the label
    :param inX: the purpose data to class
    :param dataSet: train data
    :param labels: train data label
    :param k: k nn the k value
    :return: the most near distance is the label
    """
    #print "the dataSet size is : ",dataSet.shape
    dataSetSize = dataSet.shape[0]
    #copy the data to dataSetSize times ,so can to make a diff function
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    #print "the diffMat value is :",diffMat
    sqDiffMat =diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    #先做差，再平方，再做和，再开方，这就是欧式距离。
    sortedDistIndicies = distances.argsort()# which function will return the array indix by des;
    #print "distance is :",distances
    #print "indicies is :",sortedDistIndicies
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        #get function is to get the value of the key ,if not exsit the key ,return the default numbers;
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortdClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortdClassCount[0][0]

handwritingClassTest()