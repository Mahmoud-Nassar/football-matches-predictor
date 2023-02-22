from classes.League import processData
from classification.decisionTree import DTClassifier as dt
from classification.KNearestNeighbors import KNNClassifier as knn
from classification.RandomForest import RFClassifier as rf
from classification.SVM import SVMClassifier
from classification.extraTrees import ETClassifier as et
from scrapping.fetchFunctions import cleanLinks

testSizeArray = [0.15, 0.2, 0.25, 0.3, 0.4]

if __name__ == '__main__':
    # cleanLinks()
    processData()

    # #################################################
    # classifier = dt()
    # classifier.train()
    # classifier.predict()
    # classifier.analyze()
    # #################################################
    # #
    ##################################################################
    ###################### DECISION-TREE  ###########################
    print("Decision Tree: ")

    er0 = dt.decisionTreeBasicClassification()
    print("        -basic classification precision: {:.2f}%"
          .format(er0))

    er1 = dt.experimentOnTestSize(testSizeArray)
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er1[0] * 100), er1[1]))

    er2 = dt.experimentOnMaxDepth([5, 10, 20, 30, 41, 52, 63])
    print("        -maximum depth experiment: the best max depth is {}"
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er2[0]), er2[1]))

    er22 = dt.experimentOnDepthAndMinSamplesLeaf(
        [5, 10, 20, 30, 41, 52, 63], [7, 13, 15, 23, 41])
    print("        -maximum depth and min leaf samples experiment: "
          "the best max depth and "
          "minimum leaf samples\n          is ({},{})"
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er22[0]), er22[1], er22[2]))

    print("    -best precision considering all experiments results: {:.2f}%"
          .format(dt.getBestPrecision(er0, er2, er1)))
    ##################################################################
    ####################### KNN  #####################################
    print("KNN: ")

    er5 = knn.knnBasicClassification()
    print("        -basic classification precision: {:.2f}%"
          .format(er5))

    er3 = knn.experimentOnTestSize(testSizeArray)
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

    er7 = rf.experimentOnTestSize(testSizeArray)
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er7[0] * 100), er7[1]))

    er8 = rf.experimentOnMaxDepth([5, 20, 30, 41, 52, 63])
    print("        -maximum depth experiment: the best max depth is {}"
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er8[0]), er8[1]))

    er9 = rf.experimentOnNEstimators([5, 20, 30, 41, 52, 63])
    print("        -number of estimators experiment: the best number estimators is {}"
          ",and it`s resulted \n        precision is: {:.2f}%"
          .format(int(er9[0]), er9[1]))
    ##################################################################
    #######################   SVM   #####################################
    print("SVM: ")

    er10 = SVMClassifier.svmBasicClassification()
    print("        -basic classification precision: {:.2f}%"
          .format(er10))

    er11 = SVMClassifier.experimentOnTestSize(testSizeArray)
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er11[0] * 100), er11[1]))

    # , 20, 30, 50, 70
    # , "poly", "rbf", "sigmoid"
    er12 = SVMClassifier.experimentOnCAndKernel([0.1, 0.2, 10, 20 ],
                                                ["linear", "poly", "rbf", "sigmoid"])
    print("        -C value and kernels experiment: "
          "the best C value and "
          "kernel \n          is ({},{})"
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er12[0]), er12[1], int(er12[2])))
    ##################################################################
    #######################   Extra Trees   #####################################
    print("Extra Trees: ")

    er13 = et.extraTreesBasicClassification()
    print("        -basic classification precision: {:.2f}%"
          .format(er13))

    er14 = et.experimentOnTestSize(testSizeArray)
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er14[0] * 100), er14[1]))

    er15 = et.experimentOnDepthAndNEstimators(
        [5, 10, 20, 30, 41, 52, 63], [7, 13, 15, 23, 41])
    print("        -maximum depth and number of estimators experiment: "
          "the best max depth and "
          "number of estimators\n          is ({},{})"
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er15[0]), er15[1], er15[2]))
