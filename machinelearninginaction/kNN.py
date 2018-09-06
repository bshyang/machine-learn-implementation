#!/usr/bin/python
# -*- coding:utf-8 -*-

from numpy import *
import operator
from os import listdir

def classify0(inX, dataSet, labels, k):
	#calculation of data volume "shape"
	dataSetSize = dataSet.shape[0]
	"""
	This code segment is to calculate the euclidean distance with each dataSet sample,
	"""
	#To copy the inX to dataSetSize partion and to make a difference
	diffMat = tile(inX, (dataSetSize,1)) - dataSet
  	sqDiffMat = diffMat**2
  	sqDistances = sqDiffMat.sum(axis=1)
	distances = sqDistances**0.5
	
	#function argsort return a index list of sort each element in distance by descending order 
	sortedDistIndicies = distances.argsort()
	#the for loop want to get the near distance k sample and the count of each class by label and distance list
	classCount={}
	for i in range(k):
		voteIlabel = labels[sortedDistIndicies[i]]
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
 	 	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
	#return the nearest neighbor sample label as the sample label.
	return sortedClassCount[0][0]

def createDataSet():
	#create a dataSet and label for test program
	group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels = ['A','A','B','B']
	return group, labels

if __name__ == "__main__":
	#test
	group, labels =  createDataSet()
	result = classify0([0,0],group,labels,3)
	print result
