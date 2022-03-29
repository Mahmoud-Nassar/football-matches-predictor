from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
import time
import os

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

MonthsMarketValue = ['2017-09-01', '2017-10-01', '2017-11-01', '2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01',
                     '2018-05-01', '2018-06-01']


def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = session.get(url)
    # return the soup
    return bs(html.content, "html.parser")


def get_all_tables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table")


def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        # if th.text.strip() == 'name':
        #     continue
        headers.append(th.text.strip())
    return headers


def get_table_rows(table, header):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                if len(td.text.strip()) > 0:
                    cells.append(td.text.strip())
                else:
                    cells.append('-')
        if len(cells) == len(header):
            rows.append(cells)
            print(rows)
        else:


            print(len(header), len(cells))
            print('be aware cells != header fields')

    return rows


def save_as_csv(table_name, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")


def lineup_table_rows(team, rows, team_name):
    for player in team:
        cells = []
        for i in range(len(player)):
            cells.append(player[i].strip())
        cells.append(team_name)
        rows.append(cells)
    return rows


def fetch_game_lineup(url, year):
    # get the soup
    soup = get_soup(url)

    # tables = soup.find_all("table")[:1]
    tables = soup.find_all('article')[5].select('.col-xs-12.col-sm-6')
    print(f"[+] Found a total of {len(tables)} tables.")

    team1_name = tables[0].select_one('.color-fondo').text
    team2_name = tables[1].select_one('.color-fondo').text

    table_name = team1_name.strip()+"_"+team2_name.strip()

    team1 = [(col[0].text, col[1].text) for row in tables[0].select('tr')[1:12] for col in [row.select('td')]] + \
            [(col[0].text, col[1].text) for row in tables[0].select('tr')[13:] for col in [row.select('td')] if col[2].text != '']

    team2 = [(col[0].text, col[1].text) for row in tables[1].select('tr')[1:12] for col in [row.select('td')]] + \
            [(col[0].text, col[1].text) for row in tables[1].select('tr')[13:] for col in [row.select('td')] if
             col[2].text != '']

    header = ['player_num', 'player_name', 'team']
    # iterate over all tables
    rows = []
    home_rows = lineup_table_rows(team1, rows, team1_name.strip())
    away_rows = lineup_table_rows(team2, home_rows, team2_name.strip())
    total_rows = away_rows
    csv_dir = r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\la_liga_{}_games'.format(str(year))
    csv_path = r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\la_liga_{}_games\{}'.format(str(year), table_name)
    print(csv_path)
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    save_as_csv(csv_path, header, total_rows)

def fetch_data(url, year):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    # tables = get_all_tables(soup)

    # tables = soup.find_all("table")[:1]
    tables = soup.find_all('article')[5].select('.col-xs-12.col-sm-6')
    print(f"[+] Found a total of {len(tables)} tables.")

    team1_name = tables[0].select_one('.color-fondo').text
    team2_name = tables[1].select_one('.color-fondo').text

    team1 = [(col[0].text, col[1].text) for row in tables[0].select('tr')[1:12] for col in [row.select('td')]] + \
            [(col[0].text, col[1].text) for row in tables[0].select('tr')[13:] for col in [row.select('td')] if col[2].text != '']

    team2 = [(col[0].text, col[1].text) for row in tables[1].select('tr')[1:12] for col in [row.select('td')]] + \
            [(col[0].text, col[1].text) for row in tables[1].select('tr')[13:] for col in [row.select('td')] if
             col[2].text != '']


def fetch_games(url, y):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    return str(tables[0])


def main(url, idx):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    # tables = get_all_tables(soup)
    tables = soup.find_all("table", {"class": "items"})[:1]
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        # get all the rows of the table
        rows = get_table_rows(table, headers)
        # save table as csv file

        table_name = f"MV-{MonthsMarketValue[idx][5:7]}"
        print(f"[+] Saving {table_name}")
        if MonthsMarketValue[idx][2:4] == '17':
            save_as_csv(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\LaLiga-Teams-'+table_name+'-17', headers, rows)
        else:
            save_as_csv(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\LaLiga-Teams-' + table_name+'-18', headers, rows)


def team_market_value_url_reader(year):
    try:
        u = r'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/plus/?saison_id=2020'
        fetch_data(u, year)
    except IndexError:
        print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
        exit(1)


def disciplinary_record_per_year(y):
    try:
        u = r'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/plus/?saison_id=2020'
        fetch_data(u, y)
    except IndexError:
        print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
        exit(1)

def get_linesup_data(urls_list):
    x = 0
    for url in urls_list:
        x += 1
        match_lineup = fetch_data(url, x)

def league_all_match_days(y, base_url):
    try:
        u = r'https://m.football-lineups.com/tourn/La-Liga-2020--2021/fixture'
        table_url = fetch_games(u, y)
        match_day_url_lst = create_list_of_urls(table_url, base_url)
        # get_linesup_data(match_day_url_lst)
        return match_day_url_lst
    except IndexError:
        print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
        exit(1)


def get_table_args_from_url(url):
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)


def create_list_of_urls(url, base_url):
    matchday_lineup_lst = []
    for match_url in re.finditer('<td class="td_resul">', url):
        resul_field = str(url[match_url.start()+len('<td class="td_resul">'):])
        url_prefix_idx = resul_field.find('<a href=')
        url_suffix_idx = resul_field[url_prefix_idx:].find('>')
        url_matchday = base_url + resul_field[url_prefix_idx+len('<a href="'): url_suffix_idx-1]
        matchday_lineup_lst.append(url_matchday)
    return matchday_lineup_lst


if __name__ == '__main__':
    # league_all_match_days(2020)
    urls_list =league_all_match_days('2020_2021', "https://m.football-lineups.com/")
    print(urls_list[0])
    time.sleep(3)
    for url in urls_list:
        fetch_game_lineup(url, '2020_2021')
        time.sleep(3)

