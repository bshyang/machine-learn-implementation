# -*- coding: UTF-8 -*-

from numpy import *
import operator
import matplotlib
import matplotlib.pylab as plt

def dataPlot(datingDataMat,datingLabels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.scatter(datingDataMat[:,1], datingDataMat[:,2])
    ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2],
        15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

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

def file2matrix(filename):
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numbersOfLines = len(arrayOfLines)
    returnMat = zeros((numbersOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split("\t")
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)#col
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges, minVals

def datingClassTest(dataPath):
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix(dataPath)
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m], 3)
        print "the classifier came back with : %d, the real answer is : %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1
    print "the total error rate is : %f" % (errorCount/float(numTestVecs))

def classifyPerson():
    resultList = ["not at all", "in small doses", "in large doses"]
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per years?"))
    iceCream = float(raw_input("liters of ice cream consumed per years?"))
    datingDataMat, datingLabels = file2matrix("./data/datingTestSet2.txt")
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals)/ranges, normMat, datingLabels,3)
    print "you will probably like this person: ", resultList[classifierResult-1]

if __name__ =="__main__":
    group, labels = createDataSet()
    result = classify0([0,0],group,labels,3)
    print result

    dataPath = "./data/datingTestSet2.txt"
    datingDataMat, datingLabels = file2matrix(dataPath)
    print len(datingDataMat), len(datingLabels)

    #dataPlot(datingDataMat, datingLabels)
    #normDataSet, ranges, minVals = autoNorm(datingDataMat)
    #print ranges, minVals
    datingClassTest(dataPath)
    classifyPerson()