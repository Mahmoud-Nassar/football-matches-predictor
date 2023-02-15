from classes.League import League
from classification.decisionTree import DTClassifier as dt
from classification.KNearestNeighbors import KNNClassifier as knn
from scrapping.PlayerRank import get_fifa_rating
from classes.Player import extractPlayers

csvTeamsPath = "dataSet\season_17_18\\teams\\teams.csv"
csvGamesPath = "dataSet\season_17_18\games\\games.csv"
csvWritePath = "dataSet\\"

if __name__ == '__main__':
    ##################################################################
    ####################### DECISION-TREE  ###########################
    # process data
    league = League(csvTeamsPath, csvGamesPath, csvWritePath)

    print("Decision Tree: ")
    print("        -basic classification precision: {:.2f}%"
          .format(dt.decisionTreeBasicClassification()))

    er1 = dt.experimentOnTestSize([0.1, 0.2, 0.3, 0.4])
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er1[0] * 100), er1[1]))

    er2 = dt.experimentOnMaxDepth([2, 3, 4, 5])
    print("        -maximum depth experiment: the best max depth is {}"
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er2[0]), er2[1]))

    print("    -best precision considering all experiments results: {:.2f}%"
          .format(dt.getBestPrecision(er2[0], er1[0])))
    ##################################################################
    ####################### KNN  #####################################
    # process data
    league = League(csvTeamsPath, csvGamesPath, csvWritePath)
    print("KNN: ")
    print("        -basic classification precision: {:.2f}%"
          .format(knn.knnBasicClassification()))

    er3 = knn.experimentOnTestSize([0.1, 0.2, 0.3, 0.4])
    print("        -test size experiment: best test size is {}% of the data "
          ",and it`s resulted precision is: {:.2f}%"
          .format(int(er3[0] * 100), er3[1]))

    er4 = knn.experimentOnNNeighbors([3, 4, 5, 6])
    print("        -number of nearst neighbors experiment: the best "
          "number of neighbors is {}"
          ",and it`s \n         resulted precision is: {:.2f}%"
          .format(int(er4[0]), er4[1]))

    print("    -best precision considering all experiments results: {:.2f}%"
          .format(dt.getBestPrecision(er4[0], er3[0])))
