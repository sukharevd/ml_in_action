#!/usr/bin/python

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

# Returns the elements with length equals to one from each subset of dataSet.
# In other words returns all unique elements
# For instance:
#   input=[[1,2],[3,2]]
#   createC1(input) is [frozenset(1),frozenset(2),frozenset(3)]
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)

# Returns the element of Ck if its support achives specified min threshold
# minSupport in accordance with dataSet D 
# D is dataSet in the form of set
# Ck is the elements with the same length
# minSupport is minimum threshold
def scanD(D, Ck, minSupport):
    ssCnt = {}    # wtf? what is it?
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can] = 1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0:
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

dataSet = loadDataSet()
C1 = createC1(dataSet)
D = map(set, dataSet)
L1, suppData0 = scanD(D, C1, 0.5)
print 'Data set: %s' % dataSet
print 'C1: %s' % C1
print 'L1: %s' % L1
print 'Support Data (the 1st level): %s' % suppData0

L, suppData = apriori(dataSet, 0.5)
print 'Result L: %s' % L
print 'Result Support: %s' % suppData
