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
    "history points difference",
    "market value difference",
    "audience",
    "table position difference",
    "league titles difference",
    "champions league titles difference",
    "europa league titles difference",
    "Rank difference"
]
classificationField = ["result"]
