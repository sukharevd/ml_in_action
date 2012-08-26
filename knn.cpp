// Usage: $ g++ -O3 -larmadillo -o knn knn.cpp
#include <armadillo>
#include <map>
#include <assert.h>

using arma::rowvec;
using arma::ucolvec;
using arma::mat;

/*
 * Classifies inX sample using k-nearest-neighbours algorithm.
 * dataSet is the training set;
 * labels is column vector with classes that corresponds to examples from training set;
 * k is the number of nearest neighbours that will vote;
 */
int knn(rowvec inX, mat dataSet, ucolvec labels, unsigned k)
{
    using arma::uword;
    using arma::umat;
    assert(dataSet.n_rows >= k);
    assert(dataSet.n_cols == inX.n_cols);
    assert(dataSet.n_rows == labels.n_rows);

    mat distances = repmat(inX, dataSet.n_rows, 1) - dataSet;
    distances = sqrt(sum(square(distances), 1));
    umat sortedDistIndicies = sort_index(distances);
    std::map<uword, int> classCount;
    int maxVotes = -1;
    int maxClass = -1;
    for (unsigned i = 0; i < k; ++i) {
        uword label = labels[sortedDistIndicies[i]];
        if (!classCount.count(label))
            classCount.insert(std::make_pair(label, 0));
        classCount.at(label) += 1;
        if (classCount.at(label) > maxVotes) {
            maxVotes = classCount.at(label);
            maxClass = label;
        }
    }
//    std::map<uword, int>::iterator it;
//    for (it = classCount.begin(); it != classCount.end(); ++it) {
//        cout << it->first << ": " << it->second << endl;
//    }
    assert(maxClass != -1);
    return maxClass;
}

#include <iostream>
#include <time.h>
#include "normalizer.h"

using namespace::std;
using arma::endr;
using arma::randu;
using arma::colvec;

int main()
{
    cout << ">> TEST DATA SET (k=3)" << endl;
    rowvec inX = randu<rowvec>(4);
    mat dataSet = randu<mat>(4, 4);
    ucolvec labels;
    labels << 1 << endr << 3 << endr << 2 << endr << 3 << endr;
    inX.print("inX");
    dataSet.print("dataSet:");
    labels.print("labels:");
    cout << "answer: " << knn(inX, dataSet, labels, 3) << endl << endl;

    cout << ">> RAND DATA SET (k=10)" << endl;
    srand ( time(NULL) );
    inX = randu<rowvec>(100);
    dataSet = randu<mat>(1000000, 100);
    labels = arma::conv_to<ucolvec>::from(4 * randu<colvec>(1000000));
    cout << "0s: " << count(labels.begin(), labels.end(), 0) << endl;
    cout << "1s: " << count(labels.begin(), labels.end(), 1) << endl;
    cout << "2s: " << count(labels.begin(), labels.end(), 2) << endl;
    cout << "3s: " << count(labels.begin(), labels.end(), 3) << endl;
    cout << "answer: " << knn(inX, dataSet, labels, 10) << endl << endl;

    cout << ">> FILE-BASED DATA SET (k=10)" << endl;
    mat data;
    data.load("datingTestSet2.txt");
    dataSet = data.submat(0, 0, data.n_rows-1, data.n_cols-2);
    Normalizer <double> normalizer;
    dataSet = normalizer.normalize(dataSet);
    labels = arma::conv_to<ucolvec>::from(data.submat(0, data.n_cols-1, data.n_rows-1, data.n_cols-1));
    rowvec inX1, inX2, inX3;
    inX1 << 58732 << 2.454285 << 0.222380 << endr;
    inX2 << 6121 << 8.339588 << 1.443357 << endr;
    inX3 << 36800 << 12.45 << 0.64 << endr;
    cout << "example from the 1st class:" << inX1 << "answer: " << knn(normalizer.normalize(inX1), dataSet, labels, 10) << endl << endl;
    cout << "example from the 2nd class:" << inX2 << "answer: " << knn(normalizer.normalize(inX2), dataSet, labels, 10) << endl << endl;
    cout << "example from the 3rd class:" << inX3 << "answer: " << knn(normalizer.normalize(inX3), dataSet, labels, 10) << endl << endl;
    return 0;
}

