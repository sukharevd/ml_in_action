// normalizer.h
#ifndef NORMALIZER_H
#define NORMALIZER_H

#include <armadillo>
#include <iostream>

using arma::Row;
using arma::Mat;

template <class T> class Normalizer
{
private:
    Row<T> ranges;
    Row<T> minValues;
    Row<T> maxValues;

public:
    Row<T> getRanges();
    Row<T> getMinValues();
    Row<T> getMaxValues();

    Mat<T> normalize(Mat<T> dataSet);
    Row<T> normalize(Row<T> example);
};


template<class T> Row<T> Normalizer<T>::getRanges()
{
    return ranges;
}

template<class T> Row<T> Normalizer<T>::getMinValues()
{
    return minValues;
}

template<class T> Row<T> Normalizer<T>::getMaxValues()
{
    return maxValues;
}

template<class T> arma::Mat<T> Normalizer<T>::normalize(arma::Mat<T> dataSet)
{
    minValues = arma::min(dataSet);
    maxValues = arma::max(dataSet);
    ranges = maxValues - minValues;
    arma::uword m = dataSet.n_rows;
    arma::Mat<T> normDataSet = dataSet - repmat(minValues, m, 1);
    normDataSet = normDataSet / repmat(ranges, m, 1);
    return normDataSet;
}

template<class T> arma::Row<T> Normalizer<T>::normalize(arma::Row<T> example)
{
    return (example - minValues) / ranges;
}

#endif // NORMALIZER_H
