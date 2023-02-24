import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, KFold
from helperFunctionsAndVariables.globalVariables import \
    csvProcessedDataReadPath, attributes, classificationField, \
    generalizationFactor, kFoldNumSplits, weightMap
from helperFunctionsAndVariables.helperFunctions import \
    createGraph, createMultipleFunctionGraph, createMultipleFunctionTable


class DTClassifier:
    def __init__(self, maxDepth=None, minSamplesLeaf=7, testSize=None):
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        self.X = df[attributes]
        self.y = df[classificationField]
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.X, self.y, test_size=testSize)
        self.Classifier = \
            DecisionTreeClassifier(max_depth=maxDepth, splitter="best",
                                   class_weight=weightMap,
                                   min_samples_leaf=minSamplesLeaf,
                                   criterion="entropy")
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
        for i in range(0, generalizationFactor):
            classifier = DTClassifier(maxDepth=None)
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
                classifier = DTClassifier(None, testSize=size)
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / generalizationFactor
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        createGraph(sizes, precisions, "test size (percentage of the data set)",
                    "precision in %",
                    "results\\decision tree\\"
                    "decision tree test size experiment.jpg", "Decision Tree")
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
        for depth in depths:
            precisionSum = 0
            for train_indexes, test_indexes in kf.split(X):
                classifier = DTClassifier(maxDepth=depth)
                classifier.X_train = X.iloc[train_indexes]
                classifier.y_train = y.iloc[train_indexes]
                classifier.X_test = X.iloc[test_indexes]
                classifier.y_test = y.iloc[test_indexes]
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / kFoldNumSplits
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        createGraph(depths, precisions, " tree maximum depth", "precision in %",
                    "results\\decision tree\\decision tree max "
                    "depth experiment.jpg", "Decision Tree")
        return [depths[maxIndex], precisions[maxIndex]]

    @staticmethod
    def experimentOnDepthAndMinSamplesLeaf(depths, minSamplesLeafArray):
        """ @:param depths : a list that contains the depths
        which the experiment will be done on, checks and @:returns
        in returnedValue[0] a list of precisions of the given depths
        for each depth,also @:returns in returnedValue[1] one of the
         depths that maximize the precision
         """
        kf = KFold(n_splits=kFoldNumSplits, shuffle=True, random_state=15161098)
        precisions = np.empty((len(minSamplesLeafArray), len(depths)))
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        X = df[attributes]
        y = df[classificationField]
        for i, minSamplesLeaf in enumerate(minSamplesLeafArray):
            for j, depth in enumerate(depths):
                precisionSum = 0
                for train_indexes, test_indexes in kf.split(X):
                    classifier = DTClassifier(maxDepth=depth,
                                              minSamplesLeaf=minSamplesLeaf)
                    classifier.X_train = X.iloc[train_indexes]
                    classifier.y_train = y.iloc[train_indexes]
                    classifier.X_test = X.iloc[test_indexes]
                    classifier.y_test = y.iloc[test_indexes]
                    classifier.train()
                    classifier.predict()
                    precisionSum += classifier.getPrecision()
                precision = precisionSum / kFoldNumSplits
                precisions[i, j] = precision
        maxIndex = np.unravel_index(np.argmax(precisions), precisions.shape)
        createMultipleFunctionGraph(depths, precisions, "min samples\nfor leaf",
                                    [str(i) for i in minSamplesLeafArray],
                                    " tree maximum depth",
                                    "precision in %",
                                    "results\\decision tree\\decision tree maximum "
                                    "depth and min samples per leaf experiment",
                                    "decision tree maximum depth and min samples "
                                    "per leaf experiment")
        createMultipleFunctionTable(depths, precisions, "min samples\nfor leaf",
                                    [str(i) for i in minSamplesLeafArray],
                                    " tree maximum depth",
                                    "precision in %",
                                    "results\\decision tree\\decision tree maximum "
                                    "depth and min samples per leaf experiment",
                                    "decision tree maximum depth and min samples "
                                    "per leaf experiment")
        return [depths[maxIndex[1]], minSamplesLeafArray[maxIndex[0]],
                precisions[maxIndex]]

    """ TODO: may need to update this function """

    @staticmethod
    def getBestPrecision(basic, maxDepthExperiment, testSizeExperiment):
        precisionSum = 0
        for i in range(0, generalizationFactor):
            classifier = DTClassifier(maxDepth=maxDepthExperiment[0],
                                      testSize=testSizeExperiment[0])
            classifier.train()
            classifier.predict()
            precisionSum += classifier.getPrecision()
        best_precision = precisionSum / generalizationFactor
        if maxDepthExperiment[1] > best_precision:
            best_precision = maxDepthExperiment[1]
        if testSizeExperiment[1] > best_precision:
            best_precision = testSizeExperiment[1]
        if basic > best_precision:
            best_precision = basic
        return best_precision