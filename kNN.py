__author__ = 'dmitriy'

from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
       voteIlabel = labels[sortedDistIndicies[i]]
       classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

# normValue = (value - min) / (max - min)
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet / tile(ranges, (m,1))
    return normDataSet, ranges, minVals

def datingClassTest():
    hoRating = 0.1
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normDataMat, ranges, minVals = autoNorm(datingDataMat)
    m = normDataMat.shape[0]
    errorCount = 0
    fringe = int(hoRating * m)
    for i in range(fringe):
        result = classify0(normDataMat[i, : ], normDataMat[fringe:m, : ], datingLabels[fringe:m], 3)
        if result != datingLabels[i]:
            errorCount += 1
    return float(errorCount) / fringe

print 'Error rate is %f' % datingClassTest()

def classifyPerson():
    gamingTimeSpent = float(raw_input("Percentage of spent playing video games: "))
    freqFlierMiles = float(raw_input("Frequent flier miles earned per year: "))
    iceCreamLiters = float(raw_input("Liters of ice cream consumed per year: "))
    inArray = array([gamingTimeSpent, freqFlierMiles, iceCreamLiters])
    datingDataMatrix, datingLabels = file2matrix('datingTestSet2.txt')
    normDataMatrix, ranges, minVals = autoNorm(datingDataMatrix)
    inArray = (inArray - minVals) / ranges
    m = normDataMatrix.shape[0]
    resultClass = classify0(inArray, normDataMatrix, datingLabels, 10)
    labels = ('not at all', 'in small doses', 'in large doses')
    print("You will like person ", labels[resultClass])
