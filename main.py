from classes.League import League
import classifcation.decisionTree as DT

csvTeamsPath = "dataSet\season_17_18\\teams\\teams.csv"
csvGamesPath = "dataSet\season_17_18\games\\games.csv"
csvWritePath = "dataSet\\"

if __name__ == '__main__':
    league = League(csvTeamsPath, csvGamesPath, csvWritePath)
    DT.decisionTreeBasicClassification()
    DT.decisionTreeChangeTestSizeClassification(0.3)
    DT.decisionTreeChangeMaxDepth(2)
