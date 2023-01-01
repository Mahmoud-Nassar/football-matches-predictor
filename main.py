from classes.League import League
from classifcation.decisionTree import DTClassifier as dt
from scrapping.PlayerRank import get_fifa_rating

csvTeamsPath = "dataSet\season_17_18\\teams\\teams.csv"
csvGamesPath = "dataSet\season_17_18\games\\games.csv"
csvWritePath = "dataSet\\"

if __name__ == '__main__':
    # # process data
    # league = League(csvTeamsPath, csvGamesPath, csvWritePath)
    #
    # print("Decision Tree: ")
    # print("    basic classification precision: {:.2f}%"
    #       .format(dt.decisionTreeBasicClassification()))
    #
    # er1 = dt.experimentOnTestSize([0.1, 0.2, 0.3, 0.4])
    # print("    test size experiment: best test size is {}% of the data "
    #       ",and it`s resulted precision is: {:.2f}%"
    #       .format(int(er1[0] * 100), er1[1]))
    #
    # er2 = dt.experimentOnMaxDepth([2, 3, 4, 5])
    # print("    maximum depth experiment: the best max depth is {}"
    #       ",and it`s resulted precision is: {:.2f}%"
    #       .format(int(er2[0]), er2[1]))
    #
    # print(" best precision using all the experiments result: {:.2f}%"
    #       .format(dt.getBestPrecision(er2[0], er1[0])))
    print(get_fifa_rating("Bergara M."))
