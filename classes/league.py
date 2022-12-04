import pandas as pd
import numpy as np
from classes.Team import Team
from classes.Game import Game


class League:
    def __init__(self, csvTeamsPath, csvGamesPath):
        self.teams = []
        self.games = []
        self.insertTeams(csvTeamsPath)
        self.insertLeague(csvGamesPath)

    def insertTeams(self, csvTeamsPath):
        teams = np.genfromtxt(csvTeamsPath, delimiter=',', names=True, dtype=None, encoding=None)
        self.teams.append(Team())
        for team in teams:
            self.teams.append(Team(team[0], team[1], team[2],
                                   team[3], team[4], processMarketValue(team[5])))

    def insertLeague(self, csvGamesPath):
        games = np.genfromtxt(csvGamesPath, delimiter=',', names=True, dtype=None, encoding=None)
        # creating the matches CSV file
        csvFile = [[]]
        headLines = ["date - time", "team1", "team2", "team1 market value",
                     "team2 market value", "result"]
        csvFile[0] = headLines
        i = 0
        # now generate the match attributes for ever match,
        # in the league and insert into csvFile
        for gameLine in games:
            csvFile[i] += self.insertGameAttributes(gameLine)
            i += 1

    def insertGameAttributes(self, gameLine):
        team1Id = self.getTeamIdByName(gameLine[1])
        team2Id = self.getTeamIdByName(gameLine[2])
        gameLine = [gameLine[0], gameLine[1], gameLine[2],self.getMarketValue(team1Id),
                    self.getMarketValue(team2Id),
                    getResult(gameLine)]

    def insertGameInfo(self, game):
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
            if team.id == teamId:
                return team

    def getTeamIdByName(self, teamName):
        for team in self.teams:
            if teamName == team.name:
                return team.id

    def getMarketValue(self, teamId):
        team = self.getTeamById(teamId)
        return processMarketValue(team.marketValue)


def processMarketValue(marketValueString):
    marketValueNum = ""
    i = 0
    while (marketValueString[i] != 'm') & (marketValueString[i] != 'b'):
        marketValueNum += marketValueString[i]
    marketValueNum = int(marketValueNum)
    # because the numbers in this matter is really big -> divide every number in million
    if marketValueString[i] == 'b':
        marketValueNum *= 1000
    return marketValueNum


def getResult(game):
    result = game[3]
    team1GoalsStr = []
    team2GoalsStr = []
    i = 0
    while result[i] != '-':
        team1GoalsStr += result[i]
    i += 1
    while result[i] != 'F':
        team2GoalsStr += result[i]
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
