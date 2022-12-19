class Team:
    def __init__(self, teamId=0, name=0, laLigaTitles=0, championsLeagueTitles=0,
                 europaLeagueTitles=0, marketValue=0, stadium="", rank=0):
        self.teamId = teamId
        self.name = name
        self.laLigaTitles = laLigaTitles
        self.championsLeagueTitles = championsLeagueTitles
        self.europaLeagueTitles = europaLeagueTitles
        self.marketValue = marketValue
        self.matchPlayed = 0
        self.stadium = stadium
        self.teamPoints = 0
        self.lastFiveGamesResult = ['D', 'D', 'D', 'D', 'D']  # W=win ; L=lose ; D=Draw
        self.rank = rank
