import pandas as pd
import numpy as np
import csv

Teams = ['Valencia', 'Celta', 'Villarreal', 'Espanol', 'Malaga', 'Barcelona', 'Sociedad', 'Getafe', 'Sevilla', 'Girona',
         'Alaves', 'Leganes', 'Las Palmas', 'Ath Madrid', 'Ath Bilbao', 'La Coruna', 'Levante', 'Betis', 'Eibar',
         'Real Madrid']


def tup_add(t1, t2):
    x = t1[0] + t2[0]
    y = t1[1] + t2[1]
    return [x, y]


def calc_points(game_res, home, away):
    if game_res[4] > game_res[5]:
        home[0] += 3
    elif game_res[5] == game_res[4]:
        home[0] += 1
        away[1] += 1
    else:
        away[1] += 3


def calc_goals(game_res, home_scored, away_scored, home_conceded, away_conceded):
    new_home_scored = home_scored[0]+game_res[4]
    new_away_scored = away_scored[1]+game_res[5]

    new_home_conceded = home_conceded[0] + game_res[5]
    new_away_conceded = away_conceded[1] + game_res[4]

    home_scored[0], away_scored[1] = new_home_scored, new_away_scored
    home_conceded[0], away_conceded[1] = new_home_conceded, new_away_conceded


if __name__ == '__main__':

    points = []     # points[0] = home points, points[1] = away points
    goals_scored = []
    goals_conceded = []
    for idx in range(20):
        points.append([0, 0])
        goals_scored.append([0, 0])
        goals_conceded.append([0, 0])

    header = ['HomeTeam', 'AwayTeam', 'Team1 Total Points', 'Team2 Total Points',
              'Team1 Home Points', 'Team1 Away Points',
              'Team2 Home Points', 'Team2 Away Points',
              'Team1 Total Goals', 'Team2 Total Goals',
              'Team1 Home Goals', 'Team1 Away Goals',
              'Team2 Home Goals', 'Team2 Away Goals',
              'Team1 Home Goals Conceded', 'Team1 Away Goals Conceded',
              'Team2 Home Goals Conceded', 'Team2 Away Goals Conceded'
              ]

    table = pd.read_csv('dataSet/season-1718_csv.csv')
    games_attr = np.array(table)

    with open(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\team_points_before_game.csv',
              'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for game in games_attr:
            home_idx = Teams.index(game[2])
            away_idx = Teams.index(game[3])
            calc_points(game, points[home_idx], points[away_idx])
            calc_goals(game, goals_scored[home_idx], goals_scored[away_idx],
                       goals_conceded[home_idx], goals_conceded[away_idx])
            # print(points)
            writer.writerow({'HomeTeam': game[2], 'AwayTeam': game[3],
                             'Team1 Home Points': points[home_idx][0],
                             'Team1 Total Points': points[home_idx][0]+points[home_idx][1],
                             'Team2 Total Points': points[away_idx][0]+points[away_idx][1],
                             'Team1 Away Points': points[home_idx][1],
                             'Team2 Home Points': points[away_idx][0],
                             'Team2 Away Points': points[away_idx][1],
                             'Team1 Total Goals': goals_scored[home_idx][0]+goals_scored[home_idx][1],
                             'Team2 Total Goals': goals_scored[away_idx][0]+goals_scored[away_idx][1],
                             'Team1 Home Goals': goals_scored[home_idx][0],
                             'Team1 Away Goals': goals_scored[home_idx][1],
                             'Team2 Home Goals': goals_scored[away_idx][0],
                             'Team2 Away Goals': goals_scored[away_idx][1],
                             'Team1 Home Goals Conceded': goals_conceded[home_idx][0],
                             'Team1 Away Goals Conceded': goals_conceded[home_idx][1],
                             'Team2 Home Goals Conceded': goals_conceded[away_idx][0],
                             'Team2 Away Goals Conceded': goals_conceded[away_idx][1]})
