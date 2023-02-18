from classes.League import processData
from classification.decisionTree import DTClassifier as dt
from classification.KNearestNeighbors import KNNClassifier as knn
from classification.RandomForest import RFClassifier as rf
# from helperFunctionsAndVariables.fetchFunctions import cleanLinks


if __name__ == '__main__':

    processData()

    # #################################################
    # classifier = dt(None, None)
    # classifier.train()
    # classifier.predict()
    # classifier.analyze()
    # #################################################
    #
    ##################################################################
    ####################### DECISION-TREE  ###########################
    print("Decision Tree: ")

    er0 = dt.decisionTreeBasicClassification()
    print("        -basic classification precision: {:.2f}%"
          .format(er0))

    er1 = dt.experimentOnTestSize([0.1, 0.2, 0.3, 0.4])
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er1[0] * 100), er1[1]))

    er2 = dt.experimentOnMaxDepth([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
    print("        -maximum depth experiment: the best max depth is {}"
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er2[0]), er2[1]))

    print("    -best precision considering all experiments results: {:.2f}%"
          .format(dt.getBestPrecision(er0, er2, er1)))
    ##################################################################
    ####################### KNN  #####################################
    print("KNN: ")

    er5 = knn.knnBasicClassification()
    print("        -basic classification precision: {:.2f}%"
          .format(er5))

    er3 = knn.experimentOnTestSize([0.1, 0.2, 0.3, 0.4])
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er3[0] * 100), er3[1]))

    er4 = knn.experimentOnNNeighbors([11, 21, 31, 41, 51, 61, 71, 81, 91, 101])
    print("        -number of nearst neighbors experiment: the best "
          "number of neighbors is {}"
          ",and it`s \n         resulted precision is: {:.2f}%"
          .format(int(er4[0]), er4[1]))

    print("    -best precision considering all experiments results: {:.2f}%"
          .format(knn.getBestPrecision(er5, er4, er3)))
    ##################################################################
    ####################### Random Forest  #####################################
    print("Random Forest: ")

    er6 = rf.randomForestBasicClassification()
    print("        -basic classification precision: {:.2f}%"
          .format(er6))

    er7 = rf.experimentOnTestSize([0.1, 0.2, 0.3, 0.4])
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er7[0] * 100), er7[1]))

