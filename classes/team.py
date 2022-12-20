class Team:
    # maximum team Points in a league is 114 point,
    # the sometimes we need to create a dummy team that
    # always hold the postion with index 0 in the teams array,
    # therefore we give it a higher points than every team
    def __init__(self, teamId=0, name=0, laLigaTitles=0, championsLeagueTitles=0,
                 europaLeagueTitles=0, marketValue=0, stadium="", rank=0, teamPoints=200):
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
