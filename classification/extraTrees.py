import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split, KFold
from helperFunctionsAndVariables.globalVariables import \
    csvProcessedDataReadPath, attributes, classificationField, \
    generalizationFactor, kFoldNumSplits, weightMap
from helperFunctionsAndVariables.helperFunctions import createGraph


class ETClassifier:
    def __init__(self, maxDepth, testSize=None):
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        self.X = df[attributes]
        self.y = df[classificationField]
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.X, self.y, test_size=testSize)
        self.Classifier = \
            ExtraTreesClassifier(n_estimators=100, max_depth=10, class_weight=weightMap,
                                 min_samples_leaf=7, criterion="entropy", bootstrap=True)
        self.y_pred = []

    def train(self):
        self.Classifier.fit(self.X_train, self.y_train)

    def predict(self):
        self.y_pred = self.Classifier.predict(self.X_test)
        self.y_pred = self.y_pred.reshape(-1, 1)

    def getPrecision(self):
        i = 0
        wrong = 0
        for (index, row) in self.y_test.iterrows():
            predValue = int(self.y_pred[i])
            realValue = int(row.values)
            if predValue != realValue:
                wrong += 1
            i += 1
        precision = (len(self.y_pred) - wrong) / len(self.y_pred)
        return precision * 100

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
            classifier = ETClassifier(None, None)
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
                classifier = ETClassifier(None, testSize=size)
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

