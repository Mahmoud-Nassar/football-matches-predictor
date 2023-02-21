import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split, KFold
from helperFunctionsAndVariables.globalVariables import \
    csvProcessedDataReadPath, attributes, classificationField, \
    generalizationFactor, kFoldNumSplits, weightMap
from helperFunctionsAndVariables.helperFunctions import createGraph, \
    createMultipleFunctionGraph, createMultipleFunctionTable


class ETClassifier:
    def __init__(self, n_estimators=100, maxDepth=10, testSize=None):
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        self.X = df[attributes]
        self.y = df[classificationField]
        self.y = np.ravel(self.y)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.X, self.y, test_size=testSize)
        self.Classifier = \
            ExtraTreesClassifier(n_estimators=n_estimators, max_depth=maxDepth,
                                 class_weight=weightMap, min_samples_leaf=7,
                                 criterion="entropy", bootstrap=True)
        self.y_pred = []

    def train(self):
        self.Classifier.fit(self.X_train, self.y_train)

    def predict(self):
        self.y_pred = self.Classifier.predict(self.X_test)
        self.y_pred = self.y_pred.reshape(-1, 1)

    def getPrecision(self):
        return (self.Classifier.score(self.X_test, self.y_test)) * 100

    def analyze(self):
        i = 0
        wrong = 0
        for (index, row) in self.y_test.iterrows():
            predValue = int(self.y_pred[i])
            realValue = int(row.values)
            if predValue != realValue:
                print("wrong line number {}: expected {} got {}".
                      format(index + 2, realValue, predValue))
                wrong += 1
            i += 1
        print("total wrong classifications : {}/{}".format(wrong, len(self.y_pred)))

    @staticmethod
    def extraTreesBasicClassification():
        precisionSum = 0
        for i in range(0, generalizationFactor):
            classifier = ETClassifier()
            classifier.train()
            classifier.predict()
            precisionSum += classifier.getPrecision()
        return precisionSum / generalizationFactor

    @staticmethod
    def experimentOnTestSize(sizes):
        precisions = []
        for size in sizes:
            precisionSum = 0
            for i in range(0, generalizationFactor):
                classifier = ETClassifier(testSize=size)
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / generalizationFactor
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        createGraph(sizes, precisions, "test size (percentage of the data set)",
                    "precision in %", "results\\extra trees\\extra trees"
                                      " test size experiment.jpg", "Extra Trees")
        return [sizes[maxIndex], precisions[maxIndex]]

    @staticmethod
    def experimentOnDepthAndNEstimators(depths, numberEstimatorsArray):
        """ @:param depths : a list that contains the depths
        which the experiment will be done on, checks and @:returns
        in returnedValue[0] a list of precisions of the given depths
        for each depth,also @:returns in returnedValue[1] one of the
         depths that maximize the precision
         """
        kf = KFold(n_splits=kFoldNumSplits, shuffle=True, random_state=15161098)
        precisions = np.empty((len(numberEstimatorsArray), len(depths)))
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        X = df[attributes]
        y = df[classificationField]
        y = np.ravel(y)
        for i, nEstimators in enumerate(numberEstimatorsArray):
            for j, depth in enumerate(depths):
                precisionSum = 0
                for train_indexes, test_indexes in kf.split(X):
                    classifier = ETClassifier(n_estimators=nEstimators, maxDepth=depth)
                    classifier.X_train = X.iloc[train_indexes]
                    classifier.y_train = y[train_indexes]
                    classifier.X_test = X.iloc[test_indexes]
                    classifier.y_test = y[test_indexes]
                    classifier.train()
                    classifier.predict()
                    precisionSum += classifier.getPrecision()
                precision = precisionSum / kFoldNumSplits
                precisions[i, j] = precision
        maxIndex = np.unravel_index(np.argmax(precisions), precisions.shape)
        createMultipleFunctionGraph(depths, precisions, "number of\nestimators",
                                    [str(i) for i in numberEstimatorsArray],
                                    " tree maximum depth",
                                    "precision in %",
                                    "results\\extra trees\\extra trees maximum "
                                    "depth and estimators number experiment",
                                    "extra trees maximum depth and estimators"
                                    " number experiment")
        createMultipleFunctionTable(depths, precisions, "number of\nestimators",
                                    [str(i) for i in numberEstimatorsArray],
                                    " tree maximum depth",
                                    "precision in %",
                                    "results\\extra trees\\extra trees maximum "
                                    "depth and estimators number experiment",
                                    "extra trees maximum depth and estimators"
                                    " number experiment")
        return [depths[maxIndex[1]], numberEstimatorsArray[maxIndex[0]],
                precisions[maxIndex]]
