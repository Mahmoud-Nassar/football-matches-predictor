from classes.League import League
from classifcation.decisionTree import decisionTreeBasicClassification
from classifcation.decisionTree import decisionTreeChangeTestSizeClassification
from classifcation.KNearestNeighbors import kNearestNeighborsClassification

csvTeamsPath = "dataSet\season_17_18\\teams\\teams.csv"
csvGamesPath = "dataSet\season_17_18\games\\games.csv"
csvWritePath = "dataSet\\"

if __name__ == '__main__':
    league = League(csvTeamsPath, csvGamesPath, csvWritePath)
    # decisionTreeBasicClassification()
    decisionTreeChangeTestSizeClassification()
