import pandas as pd
import csv

from classes.League import processData
from classification.decisionTree import DTClassifier as dt
from classification.KNearestNeighbors import KNNClassifier as knn
from classification.RandomForest import RFClassifier as rf
from classification.SVM import SVMClassifier as svm
from classification.extraTrees import ETClassifier as et
from helperFunctionsAndVariables.globalVariables import attributes, \
    classificationField, csvExamplesToClassifyPath, csvProcessedDataReadPath
from scrapping.fetchFunctions import cleanLinks

testSizeArray = [0.15, 0.2, 0.25, 0.3, 0.4]


def getMaxPrecision(precisionsArray):
    maxPrecision = 0
    for precisions in precisionsArray:
        if precisions > maxPrecision:
            maxPrecision = precisions
    return maxPrecision


if __name__ == '__main__':

    processData()

    # #################################################
    """
    WARNING : RUNNING THE CODE BELOW WILL OVERWRITE THE RESULTS FILE.
    WARNING : THE SVM EXPERIMENTS TAKE A SIGNIFICANTLY LONGER TIME THAN OTHERS.
    """
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
        [5, 10, 20, 41, 63], [7, 13, 15, 23, 41])
    print("        -maximum depth and min leaf samples experiment: "
          "the best max depth and "
          "minimum leaf samples\n          is ({},{})"
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er22[0]), er22[1], er22[2]))

    er2_3 = dt.experimentOnFeatureSubset([[],
                                          ["history points difference"],
                                          ["market value difference"],
                                          ["audience"],
                                          ["table position difference"],
                                          ["league titles difference"],
                                          ["champions league titles difference"],
                                          ["europa league difference"],
                                          ["Rank difference"]
                                          ],
                                         "one feature exclusion")

    er2_4 = dt.experimentOnFeatureSubset([[],
                                          ["market value difference",
                                           "audience",
                                           "Rank difference"],

                                          ["market value difference",
                                           "Rank difference"],

                                          ["history points difference",
                                           "table position difference"],

                                          ["league titles difference",
                                           "champions league titles difference",
                                           "europa league difference"],
                                          ],
                                         "multiple features exclusion")

    # er2_4 = dt.experimentOnFeatureSubset([[],
    #                                       ["market value difference",
    #                                        "audience",
    #                                        "Rank difference"]
    #                                       ],
    #                                      "legacy features exclusion")
    #
    # er2_5 = dt.experimentOnFeatureSubset([[],
    #                                       ["league titles difference",
    #                                        "champions league titles difference",
    #                                        "europa league difference"]
    #                                       ],
    #                                      "past achievements features exclusion")
    #
    # er2_6 = dt.experimentOnFeatureSubset([[],
    #                                       ["history points difference",
    #                                        "table position difference"]
    #                                       ],
    #                                      "history features exclusion")
    #
    # er2_7 = dt.experimentOnFeatureSubset([[],
    #                                       ["market value difference",
    #                                        "Rank difference"]
    #                                       ],
    #                                      "players related features exclusion")

    # print("    -best precision considering all experiments results: {:.2f}%"
    #       .format(dt.getBestPrecision(er0, er2, er1)))
    #################################################################
    ###################### KNN  #####################################

    # print("KNN: ")
    #
    # er5 = knn.knnBasicClassification()
    # print("        -basic classification precision: {:.2f}%"
    #       .format(er5))
    #
    # er3 = knn.experimentOnTestSize(testSizeArray)
    # print("        -test size experiment: best test size is {}% of the data "
    #       ",and it`s resulted precision is: {:.2f}%"
    #       .format(int(er3[0] * 100), er3[1]))
    #
    # er4 = knn.experimentOnNNeighbors([11, 21, 31, 41, 51, 61, 71, 81, 91, 101])
    # print("        -number of nearst neighbors experiment: the best "
    #       "number of neighbors is {}"
    #       ",and it`s \n         resulted precision is: {:.2f}%"
    #       .format(int(er4[0]), er4[1]))
    #
    # print("    -best precision considering all experiments results: {:.2f}%"
    #       .format(knn.getBestPrecision(er5, er4, er3)))
    # #################################################################
    # ####################### Random Forest  #####################################
    # print("Random Forest: ")
    #
    # er6 = rf.randomForestBasicClassification()
    # print("        -basic classification precision: {:.2f}%"
    #       .format(er6))
    #
    # er7 = rf.experimentOnTestSize(testSizeArray)
    # print("        -test size experiment: best test size is {}% of the data "
    #       ",and it`s resulted precision is: {:.2f}%"
    #       .format(int(er7[0] * 100), er7[1]))
    #
    # er8 = rf.experimentOnMaxDepth([5, 20, 30, 41, 52, 63])
    # print("        -maximum depth experiment: the best max depth is {}"
    #       ",and it`s resulted precision is: {:.2f}%"
    #       .format(int(er8[0]), er8[1]))
    #
    # er9 = rf.experimentOnNEstimators([5, 20, 30, 41, 52, 63])
    # print("        -number of estimators experiment: the best number estimators is {}"
    #       ",and it`s resulted \n        precision is: {:.2f}%"
    #       .format(int(er9[0]), er9[1]))
    # ##################################################################
    # #######################   SVM   #####################################
    # print("SVM: ")
    #
    # er10 = svm.svmBasicClassification()
    # print("        -basic classification precision: {:.2f}%"
    #       .format(er10))
    #
    # er11 = svm.experimentOnTestSize(testSizeArray)
    # print("        -test size experiment: best test size is {}% of the data "
    #       ",and it`s resulted precision is: {:.2f}%"
    #       .format(int(er11[0] * 100), er11[1]))
    #
    # # er12 = svm.experimentOnCAndKernel([0.1, 0.2, 10, 20],
    # #                                   ["linear", "poly", "rbf", "sigmoid"])
    # # print("        -C value and kernels experiment: "
    # #       "the best C value and "
    # #       "kernel \n          is ({},{})"
    # #       ",and it`s resulted precision is: {:.2f}%"
    # #       .format(int(er12[0]), er12[1], int(er12[2])))
    # #################################################################
    # #######################   Extra Trees   #####################################
    # print("Extra Trees: ")
    #
    # er13 = et.extraTreesBasicClassification()
    # print("        -basic classification precision: {:.2f}%"
    #       .format(er13))
    #
    # er14 = et.experimentOnTestSize(testSizeArray)
    # print("        -test size experiment: best test size is {}% of the data "
    #       ",and it`s resulted precision is: {:.2f}%"
    #       .format(int(er14[0] * 100), er14[1]))
    #
    # er15 = et.experimentOnDepthAndNEstimators(
    #     [5, 10, 20, 41, 63], [7, 13, 17, 25, 41])
    # print("        -maximum depth and number of estimators experiment: "
    #       "the best max depth and "
    #       "number of estimators\n          is ({},{})"
    #       ",and it`s resulted precision is: {:.2f}%"
    #       .format(int(er15[0]), er15[1], er15[2]))

    maxPrecision = getMaxPrecision([er0, er2[1], er22[2], er2_3[1], er2_4[1]
                                      #,er5, er4[1],
                                    # er6, er8[1], er9[1],
                                    # er10,  # er12[2],
                                    # er13, er15[2]
                                   ])

    bestClassifier = None
    attributeExcluded = []

    if maxPrecision == er0:
        bestClassifier = dt()
    if maxPrecision == er2[1]:
        bestClassifier = dt(maxDepth=er2[0])
    if maxPrecision == er22[2]:
        bestClassifier = dt(maxDepth=er22[0], minSamplesLeaf=er22[1])
    if maxPrecision == er2_3[1]:
        attributeExcluded = er2_3[0]
        bestClassifier = dt(maxDepth=4, minSamplesLeaf=7, featureExcluded=attributeExcluded)
    if maxPrecision == er2_4[1]:
        attributeExcluded = er2_4[0]
        bestClassifier = dt(maxDepth=4, minSamplesLeaf=7, featureExcluded=attributeExcluded)

    # if maxPrecision == er5:
    #     bestClassifier = knn()
    # if maxPrecision == er4[1]:
    #     bestClassifier = knn(n_neighbors=er4[0])
    #
    # if maxPrecision == er6:
    #     bestClassifier = rf()
    # if maxPrecision == er8[1]:
    #     bestClassifier = rf(maxDepth=er8[0])
    # if maxPrecision == er9[1]:
    #     bestClassifier = rf(n_estimators=er9[0])
    #
    # if maxPrecision == er10:
    #     bestClassifier = svm()
    # if maxPrecision == er12[2]:
    #     bestClassifier = svm(C=er12[0], kernel=er12[1])
    #
    # if maxPrecision == er13:
    #     bestClassifier = et()
    # if maxPrecision == er15[2]:
    #     bestClassifier = et(maxDepth=er15[0], n_estimators=er15[1])

    dft = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')
    bestClassifier.X_train = dft[set(attributes) - set(attributeExcluded)]
    bestClassifier.y_train = dft[classificationField]
    bestClassifier.train()

    dfr = pd.read_csv(csvExamplesToClassifyPath + 'input.csv')
    bestClassifier.X_test = dfr[set(attributes) - set(attributeExcluded)]
    bestClassifier.predict()
    with open(csvExamplesToClassifyPath + 'output.csv', 'w', newline='') as \
            writeFile:
        writer = csv.writer(writeFile)
        # writer.writerow(['prediction'])
        for prediction in bestClassifier.y_pred.tolist():
            writer.writerow(str(prediction[0]))
