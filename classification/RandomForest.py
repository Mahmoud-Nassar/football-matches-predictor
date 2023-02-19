from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from helperFunctionsAndVariables.globalVariables import \
    csvProcessedDataReadPath, attributes, classificationField, \
    generalizationFactor, kFoldNumSplits, weightMap
from helperFunctionsAndVariables.helperFunctions import create_graph


class RFClassifier:
    def __init__(self, n_estimators=100, testSize=None, maxDepth=None):
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        X = df[attributes]
        y = df[classificationField]
        y = np.ravel(y)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=testSize)
        self.Classifier = RandomForestClassifier(n_estimators=n_estimators,
                                                 criterion='entropy',
                                                 class_weight=weightMap
                                                 )
        self.y_pred = []

    def train(self):
        self.Classifier.fit(self.X_train, self.y_train)

    def predict(self):
        self.y_pred = self.Classifier.predict(self.X_test)

    def getPrecision(self):
        return (self.Classifier.score(self.X_test, self.y_test)) * 100

    def analyze(self):
        wrong = 0
        for i in range(len(self.y_test)):
            if self.y_pred[i] != self.y_test.values[i]:
                print("wrong line number {}: expected {} got {}".
                      format(i + 2, self.y_test.values[i], self.y_pred[i]))
                wrong += 1
        print("total wrong classifications : {}/{}".format(wrong, len(self.y_pred)))

    @staticmethod
    def randomForestBasicClassification():
        """this function applies a simple and very basic classification
             according to the default classification given
             in the class RandomForestClassifier"""
        precisionSum = 0
        for i in range(0, generalizationFactor):
            classifier = RFClassifier()
            classifier.train()
            classifier.predict()
            precisionSum += classifier.getPrecision()
        return precisionSum / generalizationFactor

    @staticmethod
    def experimentOnTestSize(sizes):
        """ @:param sizes : a list that contains the test sizes
        parentage(from all the data) which the experiment will be done on
        check and @:returns in returnedValue[0] a list of percentages the
        indicates the precisions of the given sizes for each size,also @:returns
        in returnedValue[1] one of the sizes that maximize the precision
         """
        precisions = []
        for size in sizes:
            precisionSum = 0
            for i in range(0, generalizationFactor):
                classifier = RFClassifier(100, testSize=size)
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / generalizationFactor
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        create_graph(sizes, precisions, "test size (percentage of the data set)",
                     "precision in %",
                     "results\\random forest\\random forest test size experiment.jpg")
        return [sizes[maxIndex], precisions[maxIndex]]

    @staticmethod
    def experimentOnMaxDepth(depths):
        """ @:param depths : a list that contains the depths
        which the experiment will be done on, checks and @:returns
        in returnedValue[0] a list of precisions of the given depths
        for each depth,also @:returns in returnedValue[1] one of the
         depths that maximize the precision
         """
        kf = KFold(n_splits=kFoldNumSplits, shuffle=True, random_state=15161098)
        precisions = []
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        X = df[attributes]
        y = df[classificationField]
        y = np.ravel(y)
        for depth in depths:
            precisionSum = 0
            for train_indexes, test_indexes in kf.split(X):
                classifier = RFClassifier(maxDepth=depth)
                classifier.X_train = X.iloc[train_indexes]
                classifier.y_train = y[train_indexes]
                classifier.X_test = X.iloc[test_indexes]
                classifier.y_test = y[test_indexes]
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / kFoldNumSplits
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        create_graph(depths, precisions, "tree maximum depth",
                     "precision in %",
                     "results\\random forest\\random forest max depth experiment.jpg")
        return [depths[maxIndex], precisions[maxIndex]]

    @staticmethod
    def experimentOnNEstimators(nEstimatorsArray):
        kf = KFold(n_splits=kFoldNumSplits, shuffle=True, random_state=15161098)
        precisions = []
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        X = df[attributes]
        y = df[classificationField]
        y = np.ravel(y)
        for nEstimators in nEstimatorsArray:
            precisionSum = 0
            for train_indexes, test_indexes in kf.split(X):
                classifier = RFClassifier(n_estimators=nEstimators)
                classifier.X_train = X.iloc[train_indexes]
                classifier.y_train = y[train_indexes]
                classifier.X_test = X.iloc[test_indexes]
                classifier.y_test = y[test_indexes]
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / kFoldNumSplits
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        create_graph(nEstimatorsArray, precisions, "number of estimators",
                     "precision in %",
                     "results\\random forest\\random forest estimators number experiment.jpg")
        return [nEstimatorsArray[maxIndex], precisions[maxIndex]]
