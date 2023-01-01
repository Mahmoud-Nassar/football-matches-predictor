import requests
from bs4 import BeautifulSoup


def get_fifa_rating(player_name):
    # Set the URL of the website that provides the FIFA ratings
    url = "https://www.fifaindex.com/players/"

    # Use the requests library to send a GET request to the website
    response = requests.get(url)

    # Check the status code of the response to make sure the request was successful
    if response.status_code == 200:
        # Use the BeautifulSoup library to parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table that contains the list of players
        table = soup.find('table', {'id': 'players'})

        # Check if the table element was found
        if table:
            # Find all the rows in the table
            rows = table.find_all('tr')

            # Iterate over each row in the table
            for row in rows:
                # Find the name and rating cells in the row
                name_cell = row.find('a', {'class': 'players'})
                rating_cell = row.find('td', {'class': 'rating'})

                # Check if the name of the player matches the player we are looking for
                if name_cell and name_cell.text.strip() == player_name:
                    # Return the rating of the player's FIFA card
                    return rating_cell.text.strip()
    else:
        # If the request was unsuccessful, return an error message
        return "Error retrieving FIFA ratings"


