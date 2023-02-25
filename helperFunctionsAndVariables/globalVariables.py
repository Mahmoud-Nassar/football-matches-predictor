csvTeamsPath = "dataSet\season_17_18\\teams\\teams.csv"
dataSetPath = "dataSet\\"
csvGamesPath = "dataSet\season_17_18\games\\games.csv"
csvWritePath = "dataSet\\"
csvProcessedDataReadPath = "dataSet\\"
csvExamplesToClassifyPath = "classifier\\"
generalizationFactor = 2
kFoldNumSplits = 10
weightMap = {1: 1, 2: 1}

attributes = [
    "team1 history points", "team2 history points",
    "team1 market value", "team2 market value",
    "audience",
    "team1 table position", "team2 table position",
    "team1 league titles", "team2 league titles",
    "team1 champions league titles", "team2 champions league titles",
    "team1 europa league titles", "team2 europa league titles",
    "team1 Rank", "team2 Rank"
]
classificationField = ["result"]
