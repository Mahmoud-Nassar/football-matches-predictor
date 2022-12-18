# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from classes.League import League

csvTeamsPath = "dataSet\season_17_18\\teams.csv"
csvGamesPath = "dataSet\season_17_18\games\\games.csv"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    league = League(csvTeamsPath, csvGamesPath)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
