from classes.League import processData
from classification.decisionTree import DTClassifier as dt
from classification.KNearestNeighbors import KNNClassifier as knn

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

    er4 = knn.experimentOnNNeighbors([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    print("        -number of nearst neighbors experiment: the best "
          "number of neighbors is {}"
          ",and it`s \n         resulted precision is: {:.2f}%"
          .format(int(er4[0]), er4[1]))

    print("    -best precision considering all experiments results: {:.2f}%"
          .format(knn.getBestPrecision(er5, er4, er3)))
