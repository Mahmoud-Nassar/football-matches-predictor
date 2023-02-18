class Team:
    # maximum team Points in a league is 114 point,
    # the sometimes we need to create a dummy team that
    # always hold the postion with index 0 in the teams array,
    # therefore we give it a higher points than every team
    def __init__(self, teamId=0, name=0, laLigaTitles=0,
                 championsLeagueTitles=0, europaLeagueTitles=0,
                 marketValue=0, stadium="", rank=0, teamPoints=200):
        self.teamId = teamId
        self.name = name
        self.laLigaTitles = laLigaTitles
        self.championsLeagueTitles = championsLeagueTitles
        self.europaLeagueTitles = europaLeagueTitles
        self.marketValue = marketValue
        self.matchPlayed = 0
        self.stadium = stadium
        self.teamPoints = teamPoints
        self.lastFiveGamesResult = ['D', 'D', 'D', 'D', 'D']  # W=win ; L=lose ; D=Draw
        self.rank = rank

    def getTeamHistoryPoints(self):
        points = 0

        if self.lastFiveGamesResult[0] == 'W':
            points += 4
        if self.lastFiveGamesResult[0] == 'D':
            points += 2
        if self.lastFiveGamesResult[0] == 'L':
            points -= 3

        if self.lastFiveGamesResult[1] == 'W':
            points += 3
        if self.lastFiveGamesResult[1] == 'D':
            points += 1
        if self.lastFiveGamesResult[1] == 'L':
            points -= 2

        if self.lastFiveGamesResult[2] == 'W':
            points += 3
        if self.lastFiveGamesResult[2] == 'D':
            points += 1
        if self.lastFiveGamesResult[2] == 'L':
            points -= 2

        if self.lastFiveGamesResult[3] == 'W':
            points += 2
        # no need to add or reduce points if the result was draw in this match
        if self.lastFiveGamesResult[3] == 'L':
            points -= 1

        if self.lastFiveGamesResult[3] == 'W':
            points += 1
        # no need to add or reduce points if the result was draw in this match
        if self.lastFiveGamesResult[3] == 'L':
            points -= 1

        # normalization
        # points += 10
        # points /= 2

        return points
