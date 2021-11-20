import pandas as pd
import numpy as np
import csv

Teams = ['Valencia', 'Celta', 'Villarreal', 'Espanol', 'Malaga', 'Barcelona', 'Sociedad', 'Getafe', 'Sevilla', 'Girona',
         'Alaves', 'Leganes', 'Las Palmas', 'Ath Madrid', 'Ath Bilbao', 'La Coruna', 'Levante', 'Betis', 'Eibar',
         'Real Madrid']


def tup_add(t1, t2):
    x = t1[0] + t2[0]
    y = t1[1] + t2[1]
    return x, y


def calc_points(score):
    if score[4] > score[5]:
        return [[3, 0], [0, 0]]
    elif score[5] == score[4]:
        return [[1, 1], [1, 1]]
    else:
        return [[0, 0], [0, 3]]


if __name__ == '__main__':

    points = []     # points[0] = home points, points[1] = away points
    for idx in range(20):
        points.append([0, 0])
    header = ['HomeTeam', 'AwayTeam', 'Team1 Total Points', 'Team2 Total Points',
              'Team1 Home Points', 'Team1 Away Points',
              'Team2 Home Points', 'Team2 Away Points']
    table = pd.read_csv('dataSet/season-1718_csv.csv')
    games_attr = np.array(table)

    with open(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\team_points_before_game.csv',
              'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for game in games_attr:
            home_idx = Teams.index(game[2])
            away_idx = Teams.index(game[3])
            game_points = calc_points(game)
            points[home_idx] = tup_add(points[home_idx], game_points[0])
            points[away_idx] = tup_add(points[away_idx], game_points[1])
            # print(points)
            writer.writerow({'HomeTeam': game[2], 'AwayTeam': game[3], 'Team1 Home Points': points[home_idx][0],
                             'Team1 Total Points': points[home_idx][0]+points[home_idx][1],
                             'Team2 Total Points': points[away_idx][0]+points[away_idx][1],
                             'Team1 Away Points': points[home_idx][1], 'Team2 Home Points': points[away_idx][0],
                             'Team2 Away Points': points[away_idx][1]})
