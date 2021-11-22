import pandas as pd
import numpy as np

Teams = ['Valencia', 'Celta', 'Villarreal', 'Espanol', 'Malaga', 'Barcelona', 'Sociedad', 'Getafe', 'Sevilla', 'Girona',
         'Alaves', 'Leganes', 'Las Palmas', 'Ath Madrid', 'Ath Bilbao', 'La Coruna', 'Levante', 'Betis', 'Eibar',
         'Real Madrid']

Header = ['Name', 'Nationality', 'National_Position', 'National_Kit', 'Club', 'Club_Position', 'Club_Kit',
          'Club_Joining', 'Contract_Expiry', 'Rating', 'Height', 'Weight', 'Preffered_Foot', 'Birth_Date', 'Age',
          'Preffered_Position', 'Work_Rate', 'Weak_foot', 'Skill_Moves', 'Ball_Control', 'Dribbling',
          'Marking', 'Sliding_Tackle', 'Standing_Tackle', 'Aggression', 'Reactions', 'Attacking_Position',
          'Interceptions', 'Vision', 'Composure', 'Crossing', 'Short_Pass', 'Long_Pass', 'Acceleration', 'Speed',
          'Stamina', 'Strength', 'Balance', 'Agility', 'Jumping', 'Heading', 'Shot_Power', 'Finishing', 'Long_Shots',
          'Curve', 'Freekick_Accuracy', 'Penalties', 'Volleys', 'GK_Positioning', 'GK_Diving', 'GK_Kicking',
          'GK_Handling', 'GK_Reflexes'
          ]


def team_file_generator():
    players_table = pd.read_csv('dataSet/fifa17_player_data.csv')
    players_att = np.array(players_table)
    for team in Teams:
        team_file = open(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\players_'+team+'.csv', 'w', newline='',
                         encoding="utf-8")
        t_players_idx = [idx for idx, x in enumerate(players_att) if x[4] == team]
        players = [players_att[p] for p in t_players_idx]
        team = pd.DataFrame(players)
        team.to_csv(team_file, header=Header)
        team_file.close()


if __name__ == '__main__':
    team_file_generator()
    print("GENERATING TEAM'S PLAYERS FILES DONE")

