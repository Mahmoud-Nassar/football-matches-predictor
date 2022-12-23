import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from classes.League import attributes
from classes.League import classificationField
from classifcation.helperFunctions import csvProccessedDataReadPath


class DTClassifier:
    def __init__(self):
        df = pd.read_csv(csvProccessedDataReadPath + 'processedGames.csv')
        X = df[attributes]
        y = df[classificationField]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2)
        self.Classifier = DecisionTreeClassifier()
        self.y_pred = []

    def __init__(self, maxDepth=None, testSize=0.2):
        df = pd.read_csv(csvProccessedDataReadPath + 'processedGames.csv')
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


def decisionTreeBasicClassification():
    """this function applies a simple and very basic classification
     according to the default classification given in the class sklearn.tree"""
    precisionSum = 0
    for i in range(0, 10):
        classifier = DTClassifier()
        classifier.train()
        classifier.predict()
        precisionSum += classifier.getPrecision()
    print("precision : {:.2f}%".format(precisionSum / 10))


def decisionTreeChangeTestSizeClassification(TestSize):
    """this function applies the decision tree with test size 0.3
        of the total examples given"""
    precisionSum = 0
    for i in range(0, 10):
        classifier = DTClassifier(None, testSize=TestSize)
        classifier.train()
        classifier.predict()
        precisionSum += classifier.getPrecision()
    print("precision : {:.2f}%".format(precisionSum / 10))


def decisionTreeChangeMaxDepth(maxDepth):
    """   this function applies the decision tree with maximum
    depth = parameter maxDepth """
    precisionSum = 0
    for i in range(0, 10):
        classifier = DTClassifier(maxDepth)
        classifier.train()
        classifier.predict()
        precisionSum += classifier.getPrecision()
    print("precision : {:.2f}%".format(precisionSum / 10))
