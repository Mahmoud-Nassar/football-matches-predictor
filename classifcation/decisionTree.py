import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from classes.League import attributes
from classes.League import classificationField
from classifcation.helperFunctions import csvProcessedDataReadPath
from classifcation.helperFunctions import create_graph


class DTClassifier:
    def __init__(self, maxDepth, testSize=0.2):
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        X = df[attributes]
        y = df[classificationField]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=testSize)
        self.Classifier = DecisionTreeClassifier(max_depth=maxDepth)
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
            # attributesValues = X_test.iloc[i]
            predValue = int(self.y_pred[i])
            realValue = int(row.values)
            if predValue != realValue:
                wrong += 1
            i += 1
        precision = (len(self.y_pred) - wrong) / len(self.y_pred)
        return precision * 100

    def analyze(self):
        # Iterate over the rows of the DataFrame
        i = 0
        wrong = 0
        for (index, row) in self.y_test.iterrows():
            # attributesValues = X_test.iloc[i]
            predValue = int(self.y_pred[i])
            realValue = int(row.values)
            if predValue != realValue:
                print("wrong line number {}: expected {} got {}".
                      format(index + 2, realValue, predValue))
                wrong += 1
            i += 1
        print("total wrong classifications : {}/{}".format(wrong, len(self.y_pred)))

    @staticmethod
    def decisionTreeBasicClassification():
        """this function applies a simple and very basic classification
             according to the default classification given in the class sklearn.tree"""
        precisionSum = 0
        for i in range(0, 10):
            classifier = DTClassifier(None, None)
            classifier.train()
            classifier.predict()
            precisionSum += classifier.getPrecision()
        return precisionSum / 10

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
            for i in range(0, 5):
                classifier = DTClassifier(None, testSize=size)
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / 5
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        create_graph(sizes, precisions, "test size (percentage of the data set)",
                     "precision in %", "results\\test size experiment.jpg")
        return [sizes[maxIndex], precisions[maxIndex]]

    @staticmethod
    def experimentOnMaxDepth(depths):
        """ @:param depths : a list that contains the depths
        which the experiment will be done on, checks and @:returns
        in returnedValue[0] a list of precisions of the given depths
        for each depth,also @:returns in returnedValue[1] one of the
         depths that maximize the precision
         """
        precisions = []
        for maxDepth in depths:
            precisionSum = 0
            for i in range(0, 5):
                classifier = DTClassifier(None, maxDepth)
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / 5
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        create_graph(depths, precisions, " tree maximum depth",
                     "precision in %", "results\\tree depths experiment.jpg")
        return [depths[maxIndex], precisions[maxIndex]]

    @staticmethod
    def getBestPrecision(maxDepth, testSize):
        precisionSum = 0
        for i in range(0, 5):
            classifier = DTClassifier(maxDepth=maxDepth, testSize=testSize)
            classifier.train()
            classifier.predict()
            precisionSum += classifier.getPrecision()
        precision = precisionSum / 5
        return precision

    # @staticmethod
    # def experimentOnAttributeImportance():
    #     """ @:param depths : a list that contains the depths
    #     which the experiment will be done on, checks and @:returns
    #     in returnedValue[0] a list of precisions of the given depths
    #     for each depth,also @:returns in returnedValue[1] one of the
    #      depths that maximize the precision
    #      """
    #     # importanceMap = dict.fromkeys(attributes, 1)
    #     importanceMap = {'0': 1, '1': 2, '2': '1'}
    #     precisionSum = 0
    #     for i in range(0, 5):
    #         classifier = DTClassifier(importanceMap, None)
    #         classifier.train()
    #         classifier.predict()
    #         precisionSum += classifier.getPrecision()
    #     precision = precisionSum / 5
    #     return precision
