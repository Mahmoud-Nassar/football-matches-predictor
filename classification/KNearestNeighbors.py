from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from helperFunctionsAndVariables.globalVariables import \
    csvProcessedDataReadPath, attributes, classificationField, generalizationFactor
from helperFunctionsAndVariables.helperFunctions import createGraph


class KNNClassifier:
    def __init__(self, n_neighbors=5, testSize=None):
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        X = df[attributes]
        y = df[classificationField]
        y = np.ravel(y)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=testSize)
        self.Classifier = KNeighborsClassifier(n_neighbors=n_neighbors,
                                               weights="distance",
                                               leaf_size=20
                                               )
        self.y_pred = []

    def train(self):
        self.y_train = np.ravel(self.y_train)
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
    def knnBasicClassification():
        """this function applies a simple and very basic classification
             according to the default classification given
             in the class KNeighborsClassifier"""
        precisionSum = 0
        for i in range(0, generalizationFactor):
            classifier = KNNClassifier()
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
                classifier = KNNClassifier(5, testSize=size)
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / generalizationFactor
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        createGraph(sizes, precisions, "test size (percentage of the data set)",
                     "precision in %", "results\\KNN\\"
                                       "KNN test size experiment.jpg", "KNN")
        return [sizes[maxIndex], precisions[maxIndex]]

    @staticmethod
    def experimentOnNNeighbors(neighbors):
        precisions = []
        for n in neighbors:
            precisionSum = 0
            for i in range(0, generalizationFactor):
                classifier = KNNClassifier(n_neighbors=n)
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / generalizationFactor
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        createGraph(neighbors, precisions, "number of neighbors",
                     "precision in %", "results\\KNN\\KNN number of neighbors "
                                       "experiment.jpg", "KNN")
        return [neighbors[maxIndex], precisions[maxIndex]]

    @staticmethod
    def getBestPrecision(basic, nNeighborsExperiment, testSizeExperiment):
        precisionSum = 0
        for i in range(0, generalizationFactor):
            classifier = \
                KNNClassifier(n_neighbors=nNeighborsExperiment[0],
                              testSize=testSizeExperiment[0])
            classifier.train()
            classifier.predict()
            precisionSum += classifier.getPrecision()
        best_precision = precisionSum / generalizationFactor
        if nNeighborsExperiment[1] > best_precision:
            best_precision = nNeighborsExperiment[1]
        if testSizeExperiment[1] > best_precision:
            best_precision = testSizeExperiment[1]
        if basic > best_precision:
            best_precision = basic
        return best_precision
