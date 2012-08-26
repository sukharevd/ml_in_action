#!/usr/bin/python

from numpy import *
from math import log
import operator

dataSet = [ [ 1, 1, 'yes' ], [ 1, 1, 'yes' ], [ 1, 0, 'no' ], [ 0, 1, 'no' ], [ 0, 1, 'no' ] ]
featureNames = ['no surfacing', 'flippers']

# H = \sum\limits_{i=1}^n {p_i \log_2 p_i}
# p = number of times i value has been seen
def entropy(dataSet):
    p_i = {}
    for example in dataSet:
        label = example[-1]
        if label not in p_i:
            p_i[label] = 0
        p_i[label] += 1
    entropy1 = 0.0
    for label in p_i.keys():
        p_i[label] /= float(len(dataSet))
        entropy1 -= p_i[label] * log(p_i[label], 2)
    return entropy1

def splitDataSet(dataSet, axis, value):
    splitedDataSet = []
    for example in dataSet:
        if example[axis] == value:
            splitedExample = example[:axis]
            splitedExample.extend(example[axis+1:])
            splitedDataSet.append(splitedExample)
    return splitedDataSet

def chooseBestFeatureToSplit(dataSet):
    baseEntropy = entropy(dataSet)
    n = len(dataSet[0]) - 1
    bestInfoGain, bestFeature = 0.0, -1
    for axis in range(n):
        newEntropy = 0.0
        values = [example[axis] for example in dataSet]
        uniqueValues = set(values)
        for value in uniqueValues:
            splitedDataSet = splitDataSet(dataSet, axis, value)
            valueProbability = len(splitedDataSet) / len(dataSet) 
            newEntropy += entropy(splitedDataSet) * valueProbability
        infoGain = baseEntropy - newEntropy
        if bestInfoGain < infoGain:
            bestInfoGain = infoGain
            bestFeature = axis
    return bestFeature

def domination(values):
    votes = {}
    for value in values:
        if value not in votes.keys(): votes[value] = 0
        votes[value] += 1
    sortedVotes = sorted(votes.iteritems(), key = operator.itemgetter(1), reverse = True)
    return sortedVotes[0][0]

def buildTree(dataSet, featureNames):
    n = len(dataSet[0]) - 1
    if n == 0:
        return domination([example[-1] for example in dataSet])
    labels = [example[-1] for example in dataSet]
    if labels.count(labels[0]) == len(labels):
        return labels[0]

    axis = chooseBestFeatureToSplit(dataSet)
    featureName = featureNames[axis]
    featureNamesClone = featureNames[:]
    del(featureNamesClone[axis])
    tree = {featureName: {}}
    values = [example[axis] for example in dataSet]
    uniqueValues = set(values)
    for uniqueValue in uniqueValues:
        splitedDataSet = splitDataSet(dataSet, axis, uniqueValue)
        tree[featureName][uniqueValue] = buildTree(splitedDataSet, featureNamesClone)
#       tree[axis][uniqueValue] = buildTree(splitedDataSet, featureNames[:])
    return tree

def classify(tree, featureNames, example):
    rootFeatureName = tree.keys()[0]
    rootFeature = featureNames.index(rootFeatureName)
    value = example[rootFeature]
    node = tree[rootFeatureName][value]
    if type(node).__name__ == 'dict':
        return classify(node, featureNames, example)
    else:
        return node

tree = buildTree(dataSet, featureNames)
print 'Entropy of data set: %s' % entropy(dataSet)
print 'Decision tree: %s' % tree
#print 'Classification: %s' % classify(tree, featureNames, [1,0])
#print 'Classification: %s' % classify(tree, featureNames, [1,1])

