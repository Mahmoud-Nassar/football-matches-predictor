import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.svm import SVC
from helperFunctionsAndVariables.globalVariables import \
    csvProcessedDataReadPath, attributes, classificationField, \
    generalizationFactor, kFoldNumSplits, weightMap
from helperFunctionsAndVariables.helperFunctions import createGraph


class SVMClassifier:
    def __init__(self, kernel='rbf', testSize=None):
        df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
        self.X = df[attributes]
        self.y = df[classificationField]
        self.y = np.ravel(self.y)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.X, self.y, test_size=testSize)
        self.Classifier = \
            SVC(kernel=kernel, C=1, class_weight=weightMap,
                probability=True)

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
    def svmBasicClassification():
        precisionSum = 0
        for i in range(0, generalizationFactor):
            classifier = SVMClassifier()
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
                classifier = SVMClassifier(testSize=size)
                classifier.train()
                classifier.predict()
                precisionSum += classifier.getPrecision()
            precision = precisionSum / generalizationFactor
            precisions.append(precision)
        maxIndex = np.argmax(precisions)
        createGraph(sizes, precisions, "test size (percentage of the data set)",
                     "precision in %", "results\\svm\\"
                                       "svm test size experiment.jpg", "SVM")
        return [sizes[maxIndex], precisions[maxIndex]]
