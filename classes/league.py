import pandas as pd


class league:
    def __init__(self,csvTeamsPath):
        teams = pd.read_csv(csvTeamsPath)
        teamsNum= len(teams)
        for i in [0,teamsNum-1]:
            self.teams= []

