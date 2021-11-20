import pandas as pd
import numpy as np

if __name__ == '__main__':

    header = ['HomeTeam', 'AwayTeam']
    table = pd.read_csv('dataSet/season-1718_csv.csv')
    games_attr = np.array(table)
    # t = pd.DataFrame(games, columns=header)
    # print(t)
    # t.to_csv(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\check.csv')



