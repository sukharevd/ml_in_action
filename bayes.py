#!/usr/bin/python

from math import log
from numpy import *
from operator import *

# p(a|b) = \frac{p(a and b)}{p(b)}
# p(a|b) = \frac{p(b|a)p(a)}{p(b)}
# p(c_i|w) = \frac{p(w_1|c_i)p(w_2|c_i)...p(w_n|c_i)p(c_i)}{p(w)}

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

def createVocabularyList(dataSet):
    vocabularySet = set([])
    for document in dataSet:
        vocabularySet = vocabularySet | set(document)
    return list(vocabularySet)

def wordsSetToVector(words, vocabularyList):
    vector = [0] * len(vocabularyList)
    for word in words:
        if (word in vocabularyList):
            vector[vocabularyList.index(word)] += 1
#        else:
#            print('Word %s is not in vocabulary list' % word)
    return vector

def trainNaiveBayesClassifier(dataSet, categories):
    documentsNumber = len(dataSet)
    wordsNumber = len(dataSet[0])
    pAbusive = sum(categories) / float(documentsNumber)
    p0Number, p1Number = ones(wordsNumber), ones(wordsNumber)
    p0Sum, p1Sum = 2.0, 2.0
    for i in range(documentsNumber):
        if categories[i] == 1:
            p1Number += dataSet[i];
            p1Sum +=sum(dataSet[i])
        else:
            p0Number += dataSet[i];
            p0Sum +=sum(dataSet[i])
    p0Vector = log(p0Number / p0Sum)
    p1Vector = log(p1Number / p1Sum)
    return p0Vector, p1Vector, pAbusive
    
def classifyNaiveBayes(inVector, p0Vector, p1Vector, pAbusive):
    p1 = sum(p1Vector * inVector) + log(1 - pAbusive)
    p0 = sum(p0Vector * inVector) + log(pAbusive)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNaiveBayes():
    postsList, classesList = loadDataSet()
    myVocabList = createVocabularyList(postsList)
    trainDataSet = []
    for document in postsList:
        trainDataSet.append(wordsSetToVector(document, myVocabList))
    p0V, p1V, pA = trainNaiveBayesClassifier(trainDataSet,array(classesList))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(wordsSetToVector(testEntry, myVocabList))
    print(testEntry, ' classified as: ',classifyNaiveBayes(thisDoc, p0V, p1V, pA))
    testEntry = ['stupid', 'garbage']
    thisDoc = array(wordsSetToVector(testEntry, myVocabList))
    print(testEntry, ' classified as: ',classifyNaiveBayes(thisDoc, p0V, p1V, pA))

# SPAM FILTERING
def parseText(text):
    import re
    tokens = re.split(r'\W*', text)
    return [token.lower() for token in tokens if len(token) > 2]

def spamTest():
    documents = []; classes = []; fullText = []
    for i in range(1, 26):
        words = parseText(open('email/spam/%d.txt' % i).read())
        documents.append(words)
        fullText.extend(words)
        classes.append(1)
        words = parseText(open('email/ham/%d.txt' % i).read())
        documents.append(words)
        fullText.extend(words)
        classes.append(0)
    vocabulary = createVocabularyList(documents)
    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIdx = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIdx])
        del(trainingSet[randIdx])
    trainingMatrix = []; trainingClasses = []
    for docIdx in trainingSet:
        trainingMatrix.append(wordsSetToVector(documents[docIdx], vocabulary))
        trainingClasses.append(classes[docIdx])
    p0V, p1V, pSpam = trainNaiveBayesClassifier(array(trainingMatrix), array(trainingClasses))
    errorCount = 0
    for docIdx in testSet:
        wordVector = wordsSetToVector(documents[docIdx], vocabulary)
        if classifyNaiveBayes(array(wordVector), p0V, p1V, pSpam) != classes[docIdx]:
            errorCount += 1
    print 'Spam classification. The error rate is: %s' % (float(errorCount) / len(testSet))


# PERSONAL ADS (RSS FEEDS)
def calculateTheMostFrequent(vocabulary, fullText):
    import operator
    frequencyDict = {}
    for token in vocabulary:
        frequencyDict[token] = fullText.count(token)
    sortedFrequencies = sorted(frequencyDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedFrequencies[:30]

def localWords(feed1, feed0):
    import feedparser
    documents = []; classes = []; fullText = []
    minLength = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLength):
        words = parseText(feed1['entries'][i]['summary'])
        documents.append(words)
        fullText.extend(words)
        classes.append(1)
        words = parseText(feed0['entries'][i]['summary'])
        documents.append(words)
        fullText.extend(words)
        classes.append(0)
    vocabulary = createVocabularyList(documents)
    top30Words = calculateTheMostFrequent(vocabulary, fullText)
    print 'Top words are:\n%s' % [entry[0] for entry in top30Words]
    for pairW in top30Words:
        if pairW[0] in vocabulary: vocabulary.remove(pairW[0])
    trainingSet = range(2*minLength); testSet = []
    for i in range(20):
        randIdx = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIdx])
        del(trainingSet[randIdx])
    trainingMatrix = []; trainingClasses = []
    for docIdx in trainingSet:
        trainingMatrix.append(wordsSetToVector(documents[docIdx], vocabulary))
        trainingClasses.append(classes[docIdx])
    p0V, p1V, pFirstCity = trainNaiveBayesClassifier(array(trainingMatrix), array(trainingClasses))
    errorCount = 0
    for docIdx in testSet:
        words = wordsSetToVector(documents[docIdx], vocabulary)
        if classifyNaiveBayes(array(words), p0V, p1V, pFirstCity) != classes[docIdx]:
            errorCount += 1
    print 'Personal ads. Error rate is: %s' % (float(errorCount) / len(testSet))
    return vocabulary, p0V, p1V

def getTopWords(ny, sf):
    import operator
    vocabulary, p0V, p1V = localWords(ny, sf)
    print 'p0: %s' % p0V
    print 'p1: %s' % p1V
    topNY, topSF = [], []
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabulary[i], p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabulary[i], p1V[i]))
    sortedSF = sorted(topSF, key = lambda pair: pair[1], reverse=True)
    print '===========  SF  ============'
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key = lambda pair: pair[1], reverse=True)
    print '===========  NY  ============'
    for item in sortedNY:
        print item[0]
     

trainNaiveBayesClassifier([[1]], [1])
testingNaiveBayes()
spamTest()

import feedparser
ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
localWords(ny, sf)
localWords(ny, sf)
getTopWords(ny, sf)
