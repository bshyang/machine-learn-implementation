# -*- coding: UTF-8 -*-

from numpy import *
import operator

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
    print "the dataSet size is : ",dataSet.shape
    dataSetSize = dataSet.shape[0]
    #copy the data to dataSetSize times ,so can to make a diff function
    diffMat = tile(inX, (dataSetSize,1)) -dataSet
    print "the diffMat value is :",diffMat
    sqDiffMat =diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    #先做差，再平方，再做和，再开方，这就是欧式距离。
    sortedDistIndicies = distances.argsort()# which function will return the array indix by des;
    print "distance is :",distances
    print "indicies is :",sortedDistIndicies
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        #get function is to get the value of the key ,if not exsit the key ,return the default numbers;
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortdClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortdClassCount[0][0]

if __name__ =="__main__":
    group, labels = createDataSet()
    result = classify0([0,0],group,labels,3)
    print result