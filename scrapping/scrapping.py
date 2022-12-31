# import requests
# import csv
# from bs4 import BeautifulSoup
#
#
# def scrap():
#     # Make a request to the website
#     url = 'https://www.flashscore.com/match/<match_id>/'
#     response = requests.get(url)
#
#     # Parse the HTML content
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # Extract the data from the page
#     # date = soup.find('div', class_='date').text
#     time = soup.find('div', class_='time').text
#     field = soup.find('div', class_='stadium').text
#     home_team = soup.find('div', class_='team home').text
#     away_team = soup.find('div', class_='team away').text
#     result = soup.find('div', class_='scoreboard').text
#     attendance = soup.find('div', class_='attendance').text
#     place = soup.find('div', class_='venue').text
#     round_number = soup.find('div', class_='round').text
#
#     # Find the table containing the lineup data
#     table = soup.find('table', class_='lineups')
#
#     # Extract the player data from the table
#     home_team_players = []
#     away_team_players = []
#
#     # Iterate over the rows of the table
#     for row in table.find_all('tr'):
#         cells = row.find_all('td')
#         if cells:
#             # Extract the data from the cells
#             player_name = cells[1].text
#             player_position = cells[2].text
#
#             # Determine which team the player belongs to
#             if cells[0].has_attr('class') and 'home' in cells[0]['class']:
#                 home_team_players.append((player_name, player_position))
#             elif cells[0].has_attr('class') and 'away' in cells[0]['class']:
#                 away_team_players.append((player_name, player_position))
#
#     # Write the data to a CSV file
#     with open('matches.csv', 'a', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow([date, time, home_team, away_team, result, *[p[0] for p in home_team_players],
#                          *[p[0] for p in away_team_players], attendance, place, round_number])
