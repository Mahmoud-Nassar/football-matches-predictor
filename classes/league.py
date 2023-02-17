import numpy as np
import csv
import os
from classes.Team import Team
from classification.helperFunctions import dataSetPath, csvWritePath

attributes = ["team1 market value",
              "team2 market value", "audience", "team1 table position",
              "team2 table position",
              "team1 league titles", "team2 league titles",
              "team1 champions league titles", "team2 champions league titles",
              "team1 europa league titles", "team2 europa league titles",
              "team1 Rank", "team2 Rank"]
# attributes = ["team1 ID", "team2 ID",  "audience",
#               "team1 table position", "team2 table position",
#               "team1 league titles", "team2 league titles",
#               "team1 Rank", "team2 Rank"]
classificationField = ["result"]


class League:
    def __init__(self, csvTeamsPath, csvGamesPath, csvWritePath):
        self.teams = []
        self.games = []
        self.insertTeamsInfo(csvTeamsPath)
        self.RunLeagueAndProcessData(csvGamesPath, csvWritePath)

    def insertTeamsInfo(self, csvTeamsPath):
        teams = np.genfromtxt(csvTeamsPath, delimiter=',', names=True, dtype=None, encoding=None)
        self.teams.append(Team())
        for team in teams:
            self.teams.append(Team(team[0], team[1], team[2],
                                   team[3], team[4], processMarketValue(team[5]), team[7], team[8], 0))

    def RunLeagueAndProcessData(self, csvGamesPath, csvWritePath):
        games = np.genfromtxt(csvGamesPath, delimiter=',', names=True, dtype=None, encoding=None)
        # creating the matches CSV file
        csvFile = []  # [attributes + classificationField]
        # now generate the match attributes for every match,
        # in the league and insert into csvFile
        for gameLine in games:
            processedGameLine = self.processGameAttributes(gameLine)
            csvFile.append(processedGameLine)
            self.UpdateGameInfoIntoLeague(self.getTeamByName(gameLine[1]).teamId,
                                          self.getTeamByName(gameLine[2]).teamId,
                                          processedGameLine[13])
        ########################################################################
        # # Open a file for writing train objects
        # with open(csvWritePath+'processedGamesTrain.csv', 'w', newline='') as csvProcessedGamesTrainFile:
        #     writer = csv.writer(csvProcessedGamesTrainFile, delimiter=',')
        #     writer.writerow(csvFile[0])
        #     writer.writerows(csvFile[1:301])
        # # Open a file for writing test objects
        # with open(csvWritePath+'processedGamesTest.csv', 'w', newline='') as csvProcessedGamesTestFile:
        #     writer2 = csv.writer(csvProcessedGamesTestFile, delimiter=',')
        #     writer2.writerow(csvFile[0])
        #     writer2.writerows(csvFile[301:381])
        ####################################################################
        # Open a file for writing train objects
        with open(csvWritePath + 'processedGames.csv', 'a', newline='') as \
                csvProcessedGamesTrainFile:
            writer = csv.writer(csvProcessedGamesTrainFile, delimiter=',')
            writer.writerows(csvFile)

    def UpdateGameInfoIntoLeague(self, teamId1, teamId2, result):
        if result == 1:
            self.updateTeamGameWinner(teamId1)
            self.updateTeamGameLoser(teamId2)
        elif result == 2:
            self.updateTeamGameWinner(teamId2)
            self.updateTeamGameLoser(teamId1)
        else:
            self.updateTeamGameDraw(teamId1)
            self.updateTeamGameDraw(teamId2)
        self.updateTeamsPosInTable()

    def updateTeamsPosInTable(self):
        self.teams = sorted(self.teams, key=lambda team: team.teamPoints, reverse=True)

    def updateTeamGameWinner(self, teamId):
        i = self.getTeamIndexById(teamId)
        self.teams[i].matchPlayed += 1
        self.teams[i].teamPoints += 3
        self.teams[i].lastFiveGamesResult = updateTeamHistory(self.teams[i].lastFiveGamesResult, 'W')

    def updateTeamGameLoser(self, teamId):
        i = self.getTeamIndexById(teamId)
        self.teams[i].matchPlayed += 1
        self.teams[i].lastFiveGamesResult = updateTeamHistory(self.teams[i].lastFiveGamesResult, 'L')

    def updateTeamGameDraw(self, teamId):
        i = self.getTeamIndexById(teamId)
        self.teams[i].matchPlayed += 1
        self.teams[i].teamPoints += 1
        self.teams[i].lastFiveGamesResult = updateTeamHistory(self.teams[i].lastFiveGamesResult, 'D')

    def getTeamIndexById(self, teamId):
        for i in range(0, len(self.teams)):
            if self.teams[i].teamId == teamId:
                return i
        return 0

    def processGameAttributes(self, gameLine):
        team1 = self.getTeamByName(gameLine[1])
        team2 = self.getTeamByName(gameLine[2])
        # dateTime = processDateAndTime(gameLine[0])
        processedGameLine = [self.getMarketValue(team1.teamId),
                             self.getMarketValue(team2.teamId),
                             extract_numeric_value(gameLine[32]) / 1000,
                             self.getTeamPositionById(team1.teamId), self.getTeamPositionById(team2.teamId),
                             team1.laLigaTitles, team2.laLigaTitles, team1.championsLeagueTitles,
                             team2.championsLeagueTitles, team1.europaLeagueTitles, team2.europaLeagueTitles,
                             team1.rank, team2.rank,
                             getResult(gameLine)]
        return processedGameLine

    def getTeamPositionById(self, teamId):
        team = self.getTeamById(teamId)
        if team.matchPlayed == 0:
            return 10
        for i in range(1, len(self.teams)):
            if self.teams[i].teamId == teamId:
                return i
        return 10

    def getHomeTeam(self, gameLine, team1Id, team2Id):
        stadium = gameLine[33]
        for team in self.teams:
            if team.stadium == stadium:
                if team.teamId == team1Id:
                    return 1
                elif team.teamId == team2Id:
                    return 2

    def updateGameInfo(self, game):
        team1 = self.getTeamById(game.team1Id)
        team2 = self.getTeamById(game.team2Id)
        if game.result == 1:
            team1.teamPoints += 3
            insertGameToHistory(team1, 'W')
            insertGameToHistory(team2, 'L')
        elif game.result == 2:
            team2.teamPoints += 3
            insertGameToHistory(team1, 'L')
            insertGameToHistory(team2, 'W')
        else:
            team1.teamPoints += 1
            team2.teamPoints += 1
            insertGameToHistory(team1, 'D')
            insertGameToHistory(team2, 'D')

    def getTeamById(self, teamId):
        for team in self.teams:
            if team.teamId == teamId:
                return team

    def getTeamByName(self, teamName):
        for team in self.teams:
            if teamName == team.name:
                return team
        return Team()

    def getMarketValue(self, teamId):
        team = self.getTeamById(teamId)
        return team.marketValue


# def processDateAndTime(dateAndTime):
#     i = 0
#     date = ""
#     time = ""
#     # The format of the string date
#     date_format = '%d.%m.%Y'
#     while dateAndTime[i] != " ":
#         date += dateAndTime[i]
#         i += 1
#     i += 1
#     while i < len(dateAndTime):
#         time += dateAndTime[i]
#         i += 1
#     return [date, time]


def extract_numeric_value(s: str, default: float = 0.0) -> float:
    """Extracts the numeric value from a string and returns it as a float."""
    s = ''.join(c for c in s if c.isnumeric() or c == '.')
    if not s:
        return default
    return float(s)


def updateTeamHistory(gamesHistory, char):
    gamesHistory.insert(0, char)
    gamesHistory.pop()
    return gamesHistory


def processMarketValue(marketValueString):
    marketValueNum = ""
    i = 0
    while (marketValueString[i] != 'm') & (marketValueString[i] != 'b'):
        marketValueNum += marketValueString[i]
        i += 1
    marketValueNum = float(marketValueNum)
    # because the numbers in this matter is really big -> divide every number in million
    if marketValueString[i] == 'b':
        marketValueNum *= 1000
    return marketValueNum


def getResult(game):
    result = game[3]
    team1GoalsStr = ""
    team2GoalsStr = ""
    i = 0
    while result[i] != '-':
        team1GoalsStr += result[i]
        i += 1
    i += 1
    while result[i] != 'F':
        team2GoalsStr += result[i]
        i += 1
    team1Goals = int(team1GoalsStr)
    team2Goals = int(team2GoalsStr)
    if team1Goals > team2Goals:
        return 1
    elif team2Goals > team1Goals:
        return 2
    else:
        return 0


def insertGameToHistory(team, result):
    for i in [0, 3]:
        team.lastFiveGamesResult[i] = team.lastFiveGamesResult[i + 1]
    team.lastFiveGamesResult[4] = result


def processData():
    # league = League(csvTeamsPath, csvGamesPath, csvWritePath)
    with open(csvWritePath + 'processedGames.csv', 'w', newline='') as \
            csvProcessedGamesTrainFile:
        writer = csv.writer(csvProcessedGamesTrainFile, delimiter=',')
        writer.writerows([attributes + classificationField])
    for season in os.listdir(dataSetPath):
        seasonFolderPath = os.path.join(dataSetPath, season)
        if os.path.isdir(seasonFolderPath):
            league = League(seasonFolderPath + "\\teams\\teams.csv",
                            seasonFolderPath + "\games\\games.csv", csvWritePath)
