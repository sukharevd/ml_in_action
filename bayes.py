from math import log
#from numpy import *

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

def createVocabularyLis(dataSet):
    vocabularySet = set([])
    for document in dataSet:
        vocabularySet = vocabularySet | set(document)
    return list(vocabularySet)

def wordsSetToVector(words, vocabularyList):
    vector = [0] * len(vocabularyList)
    for word in words:
        if (word in vocabularyList):
            vector[vocabularyList.index(word)] = 1
        else:
            print('Word %s is not in vocabulary list' % word)
    return vector

def trainNaiveBayesClassifier(dataSet, categories):
    documentsNumber = len(dataSet)
    wordsNumber = len(dataSet[0])
    pAbusive = sum(categories) / float(documentsNumber)
    p0Number, p1Number = [1.0] * (wordsNumber), [1.0](wordsNumber)
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
    
def classifyNaiveBayes(inVector, dataSet, categories):
    p0Vector, p1Vector, pAbusive = trainNaiveBayesClassifier(dataSet, categories)
    p1 = sum(p1Vector * inVector) + log(1 - pAbusive)
    p0 = sum(p0Vector * inVector) + log(pAbusive)
    if p1 > p0:
        return 1
    else:
        return 0


    
trainNaiveBayesClassifier([[1]], [1])