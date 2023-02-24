# import csv
# import numpy as np
#
#
# def extractPlayers():
#     games = np.genfromtxt('dataSet\season_17_18\games\\games.csv'
#                           , delimiter=',', names=True, dtype=None, encoding=None)
#     csvFile = [["player", "team"]]
#     for game in games:
#         for i in range(1, 3):
#             team = game[i]
#             for j in range(4, 15):
#                 csvFile.append([getPlayerName(game[j + ((i - 1) * 14)]), team])
#     csvFile = remove_duplicates(csvFile)
#     with open('dataSet\season_17_18\players\\' + 'players.csv',
#               'w', newline='') as playersFiles:
#         writer = csv.writer(playersFiles, delimiter=',')
#         writer.writerows(csvFile)
#
#
# def remove_duplicates(arr):
#     result = []
#     for sub_arr in arr:
#         if sub_arr not in result:
#             result.append(sub_arr)
#     return result
#
#
# def getPlayerName(playerName):
#     i = 0
#     result = ""
#     length = len(playerName)
#     while playerName[i] != ')' and playerName[i] != ' ' and i < length - 1:
#         result += playerName[i]
#         i += 1
#     return result
